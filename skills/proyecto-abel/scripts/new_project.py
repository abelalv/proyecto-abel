#!/usr/bin/env python3
"""Scaffolder del estándar de proyectos ``proyecto-abel``.

Genera un proyecto conforme al skill ``proyecto-abel`` copiando las
plantillas de ``assets/templates`` y sustituyendo sus marcadores. Usa solo la
biblioteca estándar de Python, por lo que no requiere ``uv`` para ejecutarse.

Ejemplo::

    python3 scripts/new_project.py \\
        --name "Mi Proyecto" \\
        --path ./mi-proyecto \\
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

import tomllib

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"

# Árboles de plantillas: (carpeta en assets/templates, destino relativo).
TREES: list[tuple[str, str]] = [
    ("base", "."),
    ("github", ".github"),
    ("agents", "."),
    ("sciml", "."),
]

# Marcadores de bloque condicional reconocidos.
DEFAULT_PYTHON = "3.13"

FLAGS = ("PACKAGE", "TYPES", "GITHUB", "AGENTS", "ARCHIFY", "SCIML")

# Fix (proyecto-abel): the body may NOT contain another opening tag, so the regex always
# resolves the innermost block first. The original non-greedy ``(.*?)`` paired an outer
# ``{{#if}}`` with the first inner ``{{/if}}`` and silently ate content.
_BODY = r"((?:(?!\{\{#(?:if|unless)\s).)*?)"
IF_RE = re.compile(r"\{\{#if\s+([A-Z_]+)\}\}" + _BODY + r"\{\{/if\}\}", re.DOTALL)
UNLESS_RE = re.compile(r"\{\{#unless\s+([A-Z_]+)\}\}" + _BODY + r"\{\{/unless\}\}", re.DOTALL)
LEFTOVER_RE = re.compile(r"\{\{[#/](?:if|unless)\b")
VAR_RE = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def slugify(name: str, sep: str = "-") -> str:
    """Convierte ``Nombre Proyecto`` en ``nombre-proyecto`` (o snake_case)."""
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", sep, value)
    value = re.sub(re.escape(sep) + r"{2,}", sep, value).strip(sep)
    return value or "proyecto"


def git_config(key: str) -> str | None:
    """Lee una clave de ``git config`` (p. ej. ``user.name``). ``None`` si no existe."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    value = result.stdout.strip()
    return value or None


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

    text = VAR_RE.sub(_sub, text)
    if LEFTOVER_RE.search(text):
        missing.add("<bloque condicional sin cerrar / unclosed conditional block>")
    # Fix (proyecto-abel): conditional blocks at the end of a file used to leave extra blank
    # lines, which made pre-commit's end-of-file-fixer fail on a freshly generated project.
    if text.endswith("\n"):
        text = text.rstrip("\n") + "\n"
    return text


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
        if source_name == "sciml" and not flags["SCIML"]:
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


def audit_project(
    target_root: Path,
    variables: dict[str, str],
    flags: dict[str, bool],
    missing: set[str],
) -> list[tuple[str, str]]:
    """Compara el proyecto existente con el estándar **sin escribir nada**.

    Devuelve filas ``(estado, ruta)`` con estado ``FALTA``, ``DIFIERE`` o ``OK``.
    Es la base del modo ``--audit`` (mejorar sin destruir).
    """
    rows: list[tuple[str, str]] = []

    for source_name, dest_rel in TREES:
        if source_name == "github" and not flags["GITHUB"]:
            continue
        if source_name == "agents" and not flags["AGENTS"]:
            continue
        if source_name == "sciml" and not flags["SCIML"]:
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
            rel_display = str(dest.relative_to(target_root))

            if not dest.exists():
                rows.append(("FALTA", rel_display))
                continue
            try:
                raw = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                rows.append(("OK", rel_display))
                continue
            rendered = render(raw, variables, flags, missing)
            existing = dest.read_text(encoding="utf-8", errors="replace")
            rows.append(("OK" if existing == rendered else "DIFIERE", rel_display))

    package = variables["PACKAGE_NAME"]
    code_paths = (
        [f"src/{package}/__init__.py", "tests"] if flags["PACKAGE"] else ["main.py", "tests"]
    )
    for rel_display in code_paths:
        rows.append(("OK" if (target_root / rel_display).exists() else "FALTA", rel_display))

    return rows


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

    # Identidad derivada del entorno del desarrollador (no del autor de la skill).
    owner = args.owner or git_config("github.user") or "<usuario>"
    author = args.author or git_config("user.name") or "<Tu Nombre>"
    email = args.email or git_config("user.email") or "<tu-correo>"

    repo_url = f"https://github.com/{owner}/{slug}"
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": slug,
        "PACKAGE_NAME": package,
        "DESCRIPTION": args.description or f"{project_name}.",
        "OWNER": owner,
        "REPO": slug,
        "REPO_URL": repo_url,
        "SSH_URL": f"git@{'github.com'}:{owner}/{slug}.git",
        "AUTHOR": author,
        "AUTHOR_EMAIL": email,
        "PYTHON_VERSION": args.python_version,
        "PYTHON_VERSION_NO_DOT": args.python_version.replace(".", ""),
        "YEAR": str(today.year),
        "DATE": today.isoformat(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera un proyecto conforme al estándar proyecto-abel.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Fix (proyecto-abel): with abbreviations on, the documented '--no-git' was silently
        # read as '--no-github' and dropped the whole .github/ folder.
        allow_abbrev=False,
    )
    parser.add_argument("--name", help="Nombre legible del proyecto (salvo en modo --audit).")
    parser.add_argument("--path", default=".", help="Carpeta destino (por defecto: '.').")
    parser.add_argument("--repo", help="Nombre del repo en GitHub (por defecto: slug del nombre).")
    parser.add_argument(
        "--owner",
        help="Cuenta/organización de GitHub (por defecto: 'git config github.user' o '<usuario>').",
    )
    parser.add_argument(
        "--package", help="Nombre del paquete Python (por defecto: snake_case del nombre)."
    )
    parser.add_argument("--description", help="Descripción de una línea del proyecto.")
    parser.add_argument(
        "--author",
        help="Autoría (por defecto: 'git config user.name' o '<Tu Nombre>').",
    )
    parser.add_argument(
        "--email",
        help="Correo de autoría (por defecto: 'git config user.email' o '<tu-correo>').",
    )
    parser.add_argument(
        "--python-version",
        default=None,
        help=(
            "Versión de Python (por defecto: la de un pyproject.toml existente o "
            f"{DEFAULT_PYTHON})."
        ),
    )

    parser.add_argument(
        "--app", action="store_true", help="Proyecto de aplicación (sin paquete src-layout)."
    )
    parser.add_argument("--no-types", action="store_true", help="Omite 'ty' (tipado estático).")
    parser.add_argument("--no-github", action="store_true", help="No genera '.github/'.")
    parser.add_argument(
        "--no-agents", action="store_true", help="No genera AGENTS.md, CLAUDE.md ni .opencode/."
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Solo lo esencial (equivale a --no-github --no-agents --no-sciml).",
    )
    parser.add_argument(
        "--archify",
        action="store_true",
        help="Incluye la sección de arquitectura (Archify) en el README.",
    )
    parser.add_argument(
        "--sciml",
        action=argparse.BooleanOptionalAction,
        default=None,
        help=(
            "Estructura de investigación SciML: notebooks/, data/, figures/, nbstripout "
            "(por defecto: sí; --no-sciml la omite)."
        ),
    )

    # Fix (proyecto-abel): the docs promised git init by default and a '--no-git' flag, but
    # '--git' was store_true (default off) and '--no-git' did not exist.
    parser.add_argument(
        "--git",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Inicializa el repositorio git en la rama main (por defecto: sí; --no-git lo omite).",
    )
    parser.add_argument(
        "--sync", action="store_true", help="Ejecuta 'uv sync' y 'uv run pre-commit install'."
    )
    parser.add_argument("--force", action="store_true", help="Sobrescribe archivos existentes.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Muestra qué haría sin escribir nada."
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Solo audita un proyecto existente: reporta FALTA/DIFIERE/OK sin escribir nada.",
    )
    return parser


def read_pyproject(target_root: Path) -> dict:
    """Returns the parsed ``pyproject.toml`` of an existing project (``{}`` if absent/invalid)."""
    pyproject = target_root / "pyproject.toml"
    if not pyproject.exists():
        return {}
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def pyproject_python(data: dict) -> str | None:
    """Extracts ``X.Y`` from ``project.requires-python`` (``None`` if not declared)."""
    project = data.get("project", {})
    raw = str(project.get("requires-python") or "") if isinstance(project, dict) else ""
    match = re.search(r"(\d+\.\d+)", raw)
    return match.group(1) if match else None


def pyproject_has_ty(data: dict) -> bool:
    """True if ``ty`` is configured or listed in the ``dev`` dependency group."""
    tool = data.get("tool", {})
    groups = data.get("dependency-groups", {})
    dev = groups.get("dev") if isinstance(groups, dict) else None
    has_ty = isinstance(tool, dict) and bool(tool.get("ty"))
    if isinstance(dev, list):
        has_ty = has_ty or any(re.match(r"ty\b", str(item)) for item in dev)
    return has_ty


def infer_audit_context(target_root: Path, args: argparse.Namespace) -> dict[str, bool]:
    """Rellena ``args`` y deriva las banderas leyendo el proyecto existente.

    Permite auditar con precisión un proyecto ya creado sin volver a pasar todos
    los flags originales: el contexto se "captura" del propio repositorio.
    """
    data = read_pyproject(target_root)
    project = data.get("project", {})
    if isinstance(project, dict):
        if not args.repo and project.get("name"):
            args.repo = str(project["name"])
        if not args.description and project.get("description"):
            args.description = str(project["description"])
        authors = project.get("authors") or []
        if authors and isinstance(authors[0], dict):
            args.author = args.author or authors[0].get("name")
            args.email = args.email or authors[0].get("email")
        urls = project.get("urls") or {}
        url = str(urls.get("Repository") or urls.get("Homepage") or "")
        match = re.search(r"github\.com[:/]+([^/]+)/([^/]+?)(?:\.git)?/?$", url)
        if match:
            args.owner = args.owner or match.group(1)
            args.repo = args.repo or match.group(2)
        if args.python_version is None:
            args.python_version = pyproject_python(data)

    if not args.name:
        constitution = target_root / "CONSTITUTION.md"
        if constitution.exists():
            match = re.search(
                r"^#\s*CONSTITUTION\s*[—:-]\s*(.+?)\s*$",
                constitution.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
            if match:
                args.name = match.group(1)

    if not args.description:
        # Fix (proyecto-abel): recover the description from the constitution so files that
        # embed it (AGENTS.md, CONSTITUTION.md) are not reported as DIFIERE by mistake.
        constitution = target_root / "CONSTITUTION.md"
        if constitution.exists():
            match = re.search(
                r"^\|\s*\*\*Descripción\*\*\s*\|\s*(.+?)\s*\|\s*$",
                constitution.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
            if match and "<!--" not in match.group(1):
                args.description = match.group(1)

    if not args.package:
        src = target_root / "src"
        if src.is_dir():
            packages = [
                child.name
                for child in src.iterdir()
                if child.is_dir() and (child / "__init__.py").exists()
            ]
            if packages:
                args.package = packages[0]

    has_ty = pyproject_has_ty(data)

    readme = target_root / "README.md"
    readme_text = (
        readme.read_text(encoding="utf-8", errors="replace").lower() if readme.exists() else ""
    )

    return {
        "PACKAGE": ("build-system" in data) or (target_root / "src").is_dir(),
        "TYPES": has_ty,
        "GITHUB": (target_root / ".github").is_dir(),
        "AGENTS": (target_root / "AGENTS.md").exists(),
        "ARCHIFY": ("archify" in readme_text)
        or (target_root / "docs" / "arquitectura.html").exists(),
        "SCIML": (target_root / "notebooks").is_dir(),
    }


def run_audit(
    target_root: Path,
    variables: dict[str, str],
    flags: dict[str, bool],
    missing: set[str],
) -> int:
    """Imprime la auditoría del estándar sobre un proyecto existente (sin escribir)."""
    if not target_root.exists():
        print(f"\n✖ La carpeta no existe: {target_root}")
        return 1

    print(f"\n▶ Auditoría del estándar: {target_root}")
    rows = audit_project(target_root, variables, flags, missing)
    order = {"FALTA": 0, "DIFIERE": 1, "OK": 2}
    symbol = {"FALTA": "✖", "DIFIERE": "≠", "OK": "✓"}
    for status, rel in sorted(rows, key=lambda r: (order[r[0]], r[1])):
        print(f"  {symbol[status]} {status:<7} {rel}")

    counts = {status: sum(1 for r in rows if r[0] == status) for status in order}
    print("\n── Resumen ───────────────────────────────────────────────")
    print(f"  ✓ OK: {counts['OK']} · ≠ DIFIERE: {counts['DIFIERE']} · ✖ FALTA: {counts['FALTA']}")
    print("\n  Modo NO destructivo:")
    print("   · FALTA   -> se puede añadir con el scaffolder (omite lo existente).")
    print("   · DIFIERE -> ya existe y NO coincide: puede ser personalización legítima.")
    print("                 Revísalo y fusiona a mano; NUNCA uses --force a ciegas.")
    if missing:
        print(f"  ⚠ marcadores sin resolver: {', '.join(sorted(missing))}")
    print()
    return 0


def print_pyproject_merge(
    target_root: Path, flags: dict[str, bool], data: dict, variables: dict[str, str]
) -> None:
    """Prints what to run/paste so a kept pyproject.toml matches the standard."""
    groups = data.get("dependency-groups", {})
    dev = " ".join(str(d) for d in (groups.get("dev") or [])) if isinstance(groups, dict) else ""
    wanted = [pkg for pkg in ("pre-commit", "pytest", "ruff") if pkg not in dev]
    print("\n── pyproject.toml existente (no se modificó) ─────────────")
    print("  Alinea las dependencias con el estándar / Align it with the standard:")
    if wanted:
        print(f"    uv add --dev {' '.join(wanted)}")
    if flags["SCIML"] and not (isinstance(groups, dict) and "notebooks" in groups):
        print("    uv add --group notebooks ipykernel nbstripout")
    if (target_root / "requirements.txt").exists():
        print("    uv add -r requirements.txt && rm requirements.txt")
    if not flags["TYPES"]:
        print("  (ty no está en tu pyproject: se omitió. Para activarlo: uv add --dev ty)")

    # Tool tables the Makefile and tests rely on; print the missing ones ready to paste.
    tool = data.get("tool", {}) if isinstance(data.get("tool"), dict) else {}
    template = (TEMPLATES_DIR / "base" / "pyproject.toml").read_text(encoding="utf-8")
    rendered = render(template, variables, flags, set())
    tail = rendered[rendered.index("[tool.ruff]") :]
    blocks = re.split(r"\n(?=\[tool\.)", tail)
    needed = [b.strip() for b in blocks if b.split("]")[0].strip("[").split(".")[1] not in tool]
    if needed:
        print("  Añade al final de pyproject.toml / Append to pyproject.toml:\n")
        for block in needed:
            for line in block.splitlines():
                print(f"    {line}")
            print()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.name and not args.audit:
        parser.error("--name es obligatorio (salvo en el modo --audit).")

    if args.minimal:
        args.no_github = True
        args.no_agents = True
    # Fix (proyecto-abel): '--minimal --sciml' used to drop SciML anyway. An explicit
    # --sciml/--no-sciml now always wins; otherwise SciML is on except in --minimal.
    if args.sciml is None:
        args.sciml = not args.minimal

    flags = {
        "PACKAGE": not args.app,
        "TYPES": not args.no_types,
        "GITHUB": not args.no_github,
        "AGENTS": not args.no_agents,
        "ARCHIFY": args.archify,
        "SCIML": args.sciml,
    }

    target_root = Path(args.path).expanduser().resolve()
    existing = read_pyproject(target_root)
    keep_pyproject = bool(existing) and not args.force and not args.audit

    if args.audit:
        for key, value in infer_audit_context(target_root, args).items():
            flags[key] = value
    elif keep_pyproject:
        # Fix (proyecto-abel): when completing a project whose pyproject.toml is kept, the
        # generated files must agree with it (Python version, ty), or `make check` breaks.
        if args.python_version is None:
            args.python_version = pyproject_python(existing)
        if flags["TYPES"] and not pyproject_has_ty(existing):
            flags["TYPES"] = False

    if args.python_version is None:
        args.python_version = DEFAULT_PYTHON

    if not args.name:
        args.name = target_root.name

    variables = build_variables(args)
    missing: set[str] = set()
    stats = {"created": 0, "overwritten": 0, "skipped": 0}

    if args.audit:
        return run_audit(target_root, variables, flags, missing)

    print(f"\n▶ Proyecto: {variables['PROJECT_NAME']}")
    print(f"  Destino : {target_root}")
    print(f"  Repo    : {variables['OWNER']}/{variables['REPO']}")
    print(
        f"  Modo    : {'app' if args.app else 'paquete (src-layout)'}"
        f" · types={'sí' if flags['TYPES'] else 'no'}"
        f" · github={'sí' if flags['GITHUB'] else 'no'}"
        f" · agents={'sí' if flags['AGENTS'] else 'no'}"
        f" · archify={'sí' if flags['ARCHIFY'] else 'no'}"
        f" · sciml={'sí' if flags['SCIML'] else 'no'}"
        f" · git={'sí' if args.git else 'no'}"
    )
    if args.dry_run:
        print("  (dry-run: no se escribirá nada)")

    if target_root.exists() and any(target_root.iterdir()) and not args.force:
        print("\n⚠ La carpeta destino ya tiene contenido. No se sobrescribirá ningún")
        print("  archivo existente (se omitirán). Usa --force si de verdad deseas reemplazar.")

    target_root.mkdir(parents=True, exist_ok=True)

    copy_templates(target_root, variables, flags, args.force, args.dry_run, missing, stats)
    create_package(target_root, variables, flags, args.force, args.dry_run, stats)

    if args.git and not (target_root / ".git").exists():
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

    if keep_pyproject:
        print_pyproject_merge(target_root, flags, existing, variables)

    print("\n── Siguientes pasos ──────────────────────────────────────")
    print("  1. Completa las secciones marcadas de CONSTITUTION.md.")
    print("  2. Revisa README.md (badges, descripción, estructura).")
    if flags["ARCHIFY"]:
        print("  3. Arquitectura: npx skills add tt-a1i/archify -g  (ver references/archify.md)")
        print("     y genera docs/arquitectura.json + docs/arquitectura.html.")
        print(f"  4. cd {args.path} && uv sync && uv run pre-commit install")
        print("  5. make check")
        print(f"  6. git remote add origin {variables['SSH_URL']} && git push -u origin main")
    else:
        print(f"  3. cd {args.path} && uv sync && uv run pre-commit install")
        print("  4. make check")
        print(f"  5. git remote add origin {variables['SSH_URL']} && git push -u origin main")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
