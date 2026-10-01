#!/usr/bin/env python3
"""Scaffolder del estándar de proyectos de Jan Polanco Velasco.

Genera un proyecto conforme al skill ``jan-project-standard`` copiando las
plantillas de ``assets/templates`` y sustituyendo sus marcadores. Usa solo la
biblioteca estándar de Python, por lo que no requiere ``uv`` para ejecutarse.

Ejemplo::

    python3 scripts/new_project.py \\
        --name "Mi Proyecto" \\
        --path ./mi-proyecto \\
        --owner hamsomp3 \\
        --description "Descripción breve del proyecto." \\
        --git

Los archivos existentes **no** se sobrescriben salvo que se pase ``--force``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"

# Árboles de plantillas: (carpeta en assets/templates, destino relativo).
TREES: list[tuple[str, str]] = [
    ("base", "."),
    ("github", ".github"),
    ("agents", "."),
]

# Marcadores de bloque condicional reconocidos.
FLAGS = ("PACKAGE", "TYPES", "GITHUB", "AGENTS")

IF_RE = re.compile(r"\{\{#if\s+([A-Z_]+)\}\}(.*?)\{\{/if\}\}", re.DOTALL)
UNLESS_RE = re.compile(r"\{\{#unless\s+([A-Z_]+)\}\}(.*?)\{\{/unless\}\}", re.DOTALL)
VAR_RE = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def slugify(name: str, sep: str = "-") -> str:
    """Convierte ``Nombre Proyecto`` en ``nombre-proyecto`` (o snake_case)."""
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", sep, value)
    value = re.sub(re.escape(sep) + r"{2,}", sep, value).strip(sep)
    return value or "proyecto"


def render(text: str, variables: dict[str, str], flags: dict[str, bool], missing: set[str]) -> str:
    """Aplica bloques condicionales y sustitución de variables."""
    previous = None
    while previous != text:
        previous = text
        text = IF_RE.sub(lambda m: m.group(2) if flags.get(m.group(1), False) else "", text)
        text = UNLESS_RE.sub(lambda m: "" if flags.get(m.group(1), False) else m.group(2), text)

    def _sub(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in variables:
            return str(variables[key])
        missing.add(key)
        return match.group(0)

    return VAR_RE.sub(_sub, text)


def write_text(target: Path, content: str, force: bool, dry_run: bool) -> str:
    """Escribe un archivo. Devuelve ``created``, ``overwritten`` o ``skipped``."""
    existed = target.exists()
    if existed and not force:
        return "skipped"
    if dry_run:
        return "overwritten" if existed else "created"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return "overwritten" if existed else "created"


def copy_templates(
    target_root: Path,
    variables: dict[str, str],
    flags: dict[str, bool],
    force: bool,
    dry_run: bool,
    missing: set[str],
    stats: dict[str, int],
) -> None:
    for source_name, dest_rel in TREES:
        if source_name == "github" and not flags["GITHUB"]:
            continue
        if source_name == "agents" and not flags["AGENTS"]:
            continue

        source_root = TEMPLATES_DIR / source_name
        if not source_root.is_dir():
            continue

        for path in sorted(source_root.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(source_root)
            dest = target_root / dest_rel / rel
            dest = Path(*[p for p in dest.parts if p not in ("", ".")])

            try:
                raw = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                if dest.exists() and not force:
                    stats["skipped"] += 1
                    continue
                if not dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, dest)
                stats["created"] += 1
                continue

            content = render(raw, variables, flags, missing)
            result = write_text(dest, content, force, dry_run)
            stats[result] += 1
            if result == "skipped":
                print(f"  · omitido (ya existe): {dest.relative_to(target_root)}")


def create_package(
    target_root: Path,
    variables: dict[str, str],
    flags: dict[str, bool],
    force: bool,
    dry_run: bool,
    stats: dict[str, int],
) -> None:
    package = variables["PACKAGE_NAME"]

    if flags["PACKAGE"]:
        init = f'"""{variables["PROJECT_NAME"]} — paquete principal."""\n\n__version__ = "0.1.0"\n'
        py_typed = ""
        files = {
            target_root / "src" / package / "__init__.py": init,
            target_root / "src" / package / "py.typed": py_typed,
            target_root / "tests" / "test_smoke.py": (
                f'"""{variables["PROJECT_NAME"]} — prueba de humo."""\n\n'
                "from __future__ import annotations\n\n"
                f"import {package}\n\n\n"
                "def test_el_paquete_expone_una_version() -> None:\n"
                "    # Arrange / Act\n"
                f'    version = getattr({package}, "__version__", None)\n\n'
                "    # Assert\n"
                "    assert version is not None\n"
                "    assert isinstance(version, str)\n"
            ),
        }
    else:
        project_name = variables["PROJECT_NAME"]
        main = (
            f'"""{project_name} — punto de entrada."""\n\n'
            "from __future__ import annotations\n\n\n"
            "def main() -> None:\n"
            f'    """Ejecuta {project_name}."""\n'
            f'    print("Hola desde {project_name}")\n\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n"
        )
        files = {
            target_root / "main.py": main,
            target_root / "tests" / "test_main.py": (
                f'"""{variables["PROJECT_NAME"]} — prueba de humo."""\n\n'
                "from __future__ import annotations\n\n"
                "import main\n\n\n"
                "def test_main_es_invocable() -> None:\n"
                "    # Arrange / Act / Assert\n"
                "    assert callable(main.main)\n"
            ),
        }

    for target, content in files.items():
        result = write_text(target, content, force, dry_run)
        stats[result] += 1


def run_git(target_root: Path, dry_run: bool) -> None:
    if dry_run:
        print("\n[git] (dry-run) se inicializaría el repositorio en la rama main.")
        return
    try:
        subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=target_root,
            check=True,
            capture_output=True,
            text=True,
        )
        print("\n[git] repositorio inicializado en la rama 'main'.")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"\n[git] no se pudo inicializar el repositorio: {exc}")


def run_sync(target_root: Path, dry_run: bool) -> None:
    if dry_run:
        print("[sync] (dry-run) se ejecutaría 'uv sync' y 'uv run pre-commit install'.")
        return
    for cmd in (["uv", "sync"], ["uv", "run", "pre-commit", "install"]):
        try:
            subprocess.run(cmd, cwd=target_root, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            print(f"[sync] falló '{' '.join(cmd)}': {exc}")
            return


def build_variables(args: argparse.Namespace) -> dict[str, str]:
    project_name = args.name.strip()
    slug = (args.repo or slugify(project_name)).strip()
    package = args.package or slugify(project_name, "_")
    if args.repo:
        slug = slugify(args.repo)
    today = dt.date.today()
    repo_url = f"https://github.com/{args.owner}/{slug}"
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": slug,
        "PACKAGE_NAME": package,
        "DESCRIPTION": args.description or f"{project_name}.",
        "OWNER": args.owner,
        "REPO": slug,
        "REPO_URL": repo_url,
        "SSH_URL": f"git@{'github.com'}:{args.owner}/{slug}.git",
        "AUTHOR": args.author,
        "AUTHOR_EMAIL": args.email,
        "PYTHON_VERSION": args.python_version,
        "PYTHON_VERSION_NO_DOT": args.python_version.replace(".", ""),
        "YEAR": str(today.year),
        "DATE": today.isoformat(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera un proyecto conforme al estándar jan-project-standard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--name", required=True, help="Nombre legible del proyecto.")
    parser.add_argument("--path", default=".", help="Carpeta destino (por defecto: '.').")
    parser.add_argument("--repo", help="Nombre del repo en GitHub (por defecto: slug del nombre).")
    parser.add_argument("--owner", default="hamsomp3", help="Cuenta/organización de GitHub.")
    parser.add_argument(
        "--package", help="Nombre del paquete Python (por defecto: snake_case del nombre)."
    )
    parser.add_argument("--description", help="Descripción de una línea del proyecto.")
    parser.add_argument("--author", default="Jan Polanco V.", help="Autoría.")
    parser.add_argument("--email", default="hamsomp3@gmail.com", help="Correo de autoría.")
    parser.add_argument(
        "--python-version", default="3.13", help="Versión de Python (por defecto: 3.13)."
    )

    parser.add_argument(
        "--app", action="store_true", help="Proyecto de aplicación (sin paquete src-layout)."
    )
    parser.add_argument("--no-types", action="store_true", help="Omite 'ty' (tipado estático).")
    parser.add_argument("--no-github", action="store_true", help="No genera '.github/'.")
    parser.add_argument(
        "--no-agents", action="store_true", help="No genera 'AGENTS.md' ni '.opencode/'."
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Solo lo esencial (equivale a --no-github --no-agents).",
    )

    parser.add_argument(
        "--git", action="store_true", help="Inicializa el repositorio git (rama main)."
    )
    parser.add_argument(
        "--sync", action="store_true", help="Ejecuta 'uv sync' y 'uv run pre-commit install'."
    )
    parser.add_argument("--force", action="store_true", help="Sobrescribe archivos existentes.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Muestra qué haría sin escribir nada."
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.minimal:
        args.no_github = True
        args.no_agents = True

    flags = {
        "PACKAGE": not args.app,
        "TYPES": not args.no_types,
        "GITHUB": not args.no_github,
        "AGENTS": not args.no_agents,
    }

    variables = build_variables(args)
    target_root = Path(args.path).expanduser().resolve()
    missing: set[str] = set()
    stats = {"created": 0, "overwritten": 0, "skipped": 0}

    print(f"\n▶ Proyecto: {variables['PROJECT_NAME']}")
    print(f"  Destino : {target_root}")
    print(f"  Repo    : {variables['OWNER']}/{variables['REPO']}")
    print(
        f"  Modo    : {'app' if args.app else 'paquete (src-layout)'}"
        f" · types={'sí' if flags['TYPES'] else 'no'}"
        f" · github={'sí' if flags['GITHUB'] else 'no'}"
        f" · agents={'sí' if flags['AGENTS'] else 'no'}"
    )
    if args.dry_run:
        print("  (dry-run: no se escribirá nada)")

    if target_root.exists() and any(target_root.iterdir()) and not args.force:
        print("\n⚠ La carpeta destino ya tiene contenido. No se sobrescribirá ningún")
        print("  archivo existente (se omitirán). Usa --force si de verdad deseas reemplazar.")

    target_root.mkdir(parents=True, exist_ok=True)

    copy_templates(target_root, variables, flags, args.force, args.dry_run, missing, stats)
    create_package(target_root, variables, flags, args.force, args.dry_run, stats)

    if args.git:
        run_git(target_root, args.dry_run)
    if args.sync:
        run_sync(target_root, args.dry_run)

    print("\n── Resultado ─────────────────────────────────────────────")
    print(
        f"  creados: {stats['created']}"
        f" · sobrescritos: {stats['overwritten']}"
        f" · omitidos: {stats['skipped']}"
    )
    if missing:
        print(f"  ⚠ marcadores sin resolver: {', '.join(sorted(missing))}")

    print("\n── Siguientes pasos ──────────────────────────────────────")
    print("  1. Completa las secciones marcadas de CONSTITUTION.md.")
    print("  2. Revisa README.md (badges, descripción, estructura).")
    print(f"  3. cd {args.path} && uv sync && uv run pre-commit install")
    print("  4. make check")
    print(f"  5. git remote add origin {variables['SSH_URL']} && git push -u origin main")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
