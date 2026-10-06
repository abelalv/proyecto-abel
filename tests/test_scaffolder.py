"""Tests for the proyecto-abel skill: scaffolder, audit, identity script and SKILL.md.

Run with:  make test        (fast, standard library + pytest only)
           make test-slow   (also runs uv sync + make check inside a generated project)
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "proyecto-abel"
NEW_PROJECT = SKILL / "scripts" / "new_project.py"
IDENTITY = SKILL / "scripts" / "setup_git_identity.py"
LEFTOVER = re.compile(r"\{\{[#/]?[A-Z_]")  # any unrendered marker or block tag


def run(script: Path, *args: str, cwd: Path | None = None, env: dict | None = None):
    """Runs a skill script with the current interpreter and returns the CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def scaffold(tmp_path: Path, *extra: str, name: str = "Test Project") -> Path:
    """Generates a project in tmp_path/proj and fails the test if the script fails."""
    target = tmp_path / "proj"
    result = run(NEW_PROJECT, "--name", name, "--path", str(target), *extra)
    assert result.returncode == 0, result.stderr + result.stdout
    return target


def text_files(root: Path):
    """Yields generated text files, skipping git internals and virtualenvs."""
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts and ".venv" not in path.parts:
            try:
                yield path, path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue


def load_module():
    """Imports new_project.py as a module to unit-test the renderer."""
    spec = importlib.util.spec_from_file_location("new_project", NEW_PROJECT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- renderer


def test_render_resolves_nested_blocks_innermost_first():
    # Arrange
    mod = load_module()
    tpl = "A{{#if X}}B{{#if Y}}C{{/if}}D{{/if}}E{{#unless X}}F{{/unless}}"
    missing: set[str] = set()

    # Act
    both = mod.render(tpl, {}, {"X": True, "Y": True}, missing)
    outer_only = mod.render(tpl, {}, {"X": True, "Y": False}, missing)
    none = mod.render(tpl, {}, {"X": False, "Y": True}, missing)

    # Assert
    assert both == "ABCDE"
    assert outer_only == "ABDE"
    assert none == "AEF"
    assert not missing


def test_render_warns_on_unclosed_block_and_normalizes_final_newline():
    mod = load_module()
    missing: set[str] = set()
    out = mod.render("x{{#if X}}y\n\n\n", {}, {"X": True}, missing)
    assert out.endswith("y\n") and not out.endswith("\n\n")
    assert missing, "an unclosed block must be reported"


# --------------------------------------------------------------------------- scaffolder


def test_default_project_has_full_standard(tmp_path):
    proj = scaffold(tmp_path)
    for rel in [
        ".git",
        ".github/workflows/ci.yml",
        "AGENTS.md",
        "CLAUDE.md",
        "CONSTITUTION.md",
        "notebooks/README.md",
        "data/README.md",
        "figures/README.md",
        "src/test_project/__init__.py",
        "tests/test_smoke.py",
    ]:
        assert (proj / rel).exists(), f"missing {rel}"
    pyproject = (proj / "pyproject.toml").read_text()
    assert "nbstripout" in pyproject and "notebooks = [" in pyproject
    assert "nbstripout" in (proj / ".pre-commit-config.yaml").read_text()


def test_no_unrendered_markers_and_single_final_newline(tmp_path):
    for i, flags in enumerate(([], ["--archify"], ["--app", "--minimal"], ["--no-types"])):
        proj = scaffold(tmp_path / str(i), *flags, "--no-git")
        for path, text in text_files(proj):
            if path.name == "ci.yml":  # GitHub Actions uses ${{ ... }} legitimately
                text = text.replace("${{", "")
            assert not LEFTOVER.search(text), f"{flags}: marker left in {path.name}"
            if text:
                assert text.endswith("\n") and not text.endswith("\n\n"), path.name


def test_readme_keeps_structure_section_with_and_without_archify(tmp_path):
    plain = scaffold(tmp_path / "a", "--no-git")
    archi = scaffold(tmp_path / "b", "--archify", "--no-git")
    assert "## 📂 Estructura del repositorio" in (plain / "README.md").read_text()
    readme_b = (archi / "README.md").read_text()
    assert "## 📂 Estructura del repositorio" in readme_b
    assert "## 🗺️ Arquitectura del proyecto" in readme_b


def test_no_git_skips_git_but_keeps_github(tmp_path):
    proj = scaffold(tmp_path, "--no-git")
    assert not (proj / ".git").exists()
    assert (proj / ".github").is_dir()


def test_abbreviated_flags_are_rejected(tmp_path):
    result = run(NEW_PROJECT, "--name", "X", "--path", str(tmp_path / "x"), "--no-gi")
    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr


def test_minimal_mode_drops_optional_layers(tmp_path):
    proj = scaffold(tmp_path, "--minimal", "--no-git")
    for rel in [".github", "AGENTS.md", "CLAUDE.md", ".opencode", "notebooks"]:
        assert not (proj / rel).exists(), f"{rel} should not exist in --minimal"
    constitution = (proj / "CONSTITUTION.md").read_text()
    assert ".github/" not in constitution and "AGENTS.md" not in constitution


def test_app_mode_creates_main(tmp_path):
    proj = scaffold(tmp_path, "--app", "--no-sciml", "--no-git")
    assert (proj / "main.py").exists() and not (proj / "src").exists()
    assert "[build-system]" not in (proj / "pyproject.toml").read_text()


def test_existing_files_are_never_overwritten_without_force(tmp_path):
    proj = scaffold(tmp_path, "--no-git")
    (proj / "README.md").write_text("mine\n")
    again = run(NEW_PROJECT, "--name", "Test Project", "--path", str(proj))
    assert again.returncode == 0
    assert (proj / "README.md").read_text() == "mine\n"


def test_dry_run_writes_nothing(tmp_path):
    target = tmp_path / "dry"
    result = run(NEW_PROJECT, "--name", "Dry", "--path", str(target), "--dry-run")
    assert result.returncode == 0
    assert not target.exists() or not any(target.iterdir())


def test_audit_reports_all_ok_on_fresh_project(tmp_path):
    proj = scaffold(tmp_path)
    result = run(NEW_PROJECT, "--path", str(proj), "--audit")
    assert result.returncode == 0
    assert "DIFIERE: 0" in result.stdout and "FALTA: 0" in result.stdout


def test_minimal_with_explicit_sciml_keeps_research_folders(tmp_path):
    proj = scaffold(tmp_path, "--minimal", "--sciml", "--no-git")
    for rel in ["notebooks", "data", "figures"]:
        assert (proj / rel).is_dir(), f"--minimal --sciml must keep {rel}/"
    assert not (proj / ".github").exists()


def test_completing_existing_project_follows_its_pyproject(tmp_path):
    # Arrange: a legacy repo with its own README, pyproject (Python 3.12, no ty) and notebooks
    repo = tmp_path / "legacy"
    (repo / "notebooks").mkdir(parents=True)
    (repo / "README.md").write_text("# Mi repo viejo\n")
    (repo / "requirements.txt").write_text("numpy\n")
    (repo / "pyproject.toml").write_text(
        '[project]\nname = "uhi-bogota"\nversion = "0.1.0"\n'
        'requires-python = ">=3.12"\ndependencies = []\n'
    )

    # Act
    done = run(NEW_PROJECT, "--path", str(repo), "--name", "UHI Bogota",
               "--description", "Isla de calor.", "--app", "--no-github", "--no-git")  # fmt: skip
    audit = run(NEW_PROJECT, "--path", str(repo), "--audit")

    # Assert: user files kept, generated files agree with the kept pyproject
    assert done.returncode == 0, done.stderr
    assert (repo / "README.md").read_text() == "# Mi repo viejo\n"
    assert (repo / ".python-version").read_text().strip() == "3.12"
    assert "typecheck:" not in (repo / "Makefile").read_text()
    assert "uv add --dev pre-commit pytest ruff" in done.stdout
    assert "uv add -r requirements.txt" in done.stdout
    assert "[tool.pytest.ini_options]" in done.stdout
    assert "DIFIERE: 2" in audit.stdout and "FALTA: 0" in audit.stdout


def example_commands() -> list[str]:
    """CLI lines from the examples guide and the README (backslash continuations joined)."""
    commands = []
    for doc in (SKILL / "references" / "examples.md", ROOT / "README.md"):
        blocks = re.findall(r"```bash\n(.*?)```", doc.read_text(encoding="utf-8"), re.S)
        for block in blocks:
            for line in block.replace("\\\n", " ").splitlines():
                line = line.split("  #")[0].strip()
                if line.startswith("python3 $S/"):
                    commands.append(line)
    return commands


@pytest.mark.parametrize("command", example_commands())
def test_every_documented_example_command_runs(tmp_path, command):
    # Each example runs in a fresh folder with a throwaway HOME (identity examples)
    env = {**os.environ, "HOME": str(tmp_path), "S": str(SKILL / "scripts")}
    env["PATH"] = f"{Path(sys.executable).parent}:{env['PATH']}"
    work = tmp_path / "work"
    work.mkdir()
    result = subprocess.run(
        ["bash", "-c", command], cwd=work, env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, f"{command}\n{result.stdout}\n{result.stderr}"
    assert "marcadores sin resolver" not in result.stdout


def test_examples_guide_has_at_least_ten_commands():
    assert len(example_commands()) >= 10


# --------------------------------------------------------------------------- identity


def test_identity_print_mode_writes_nothing(tmp_path):
    env = {**os.environ, "HOME": str(tmp_path)}
    result = run(
        IDENTITY,
        "--name", "Ana Pérez",
        "--email", "ana@example.com",
        "--key", "~/.ssh/id_ed25519",
        "--dir", "~/Repos",
        "--platform", "linux",
        "--print",
        env=env,
    )  # fmt: skip
    assert result.returncode == 0, result.stderr
    assert "includeIf" in result.stdout and "ana@example.com" in result.stdout
    assert not (tmp_path / ".gitconfig").exists()


# --------------------------------------------------------------------------- SKILL.md


def test_skill_frontmatter_is_valid():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    front = text.split("---", 2)[1]
    name = re.search(r"^name:\s*(\S+)\s*$", front, re.M).group(1)
    desc = re.search(r'^description:\s*"(.*)"\s*$', front, re.M).group(1)
    assert name == SKILL.name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64
    assert 0 < len(desc) <= 1024


def test_skill_has_no_leftover_upstream_name():
    offenders = []
    for path, text in text_files(SKILL):
        for line in text.splitlines():
            if "jan-project-standard" in line and "based-on:" not in line:
                offenders.append(f"{path.relative_to(SKILL)}: {line.strip()}")
    assert not offenders, "\n".join(offenders)


def test_all_reference_links_in_skill_md_exist():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for rel in set(re.findall(r"\]\(((?:references|scripts|assets)/[^)#]+)\)", text)):
        assert (SKILL / rel).exists(), f"broken link in SKILL.md: {rel}"


# --------------------------------------------------------------------------- slow


@pytest.mark.skipif(
    not os.environ.get("RUN_SLOW") or shutil.which("uv") is None,
    reason="set RUN_SLOW=1 (needs uv and network)",
)
def test_generated_project_passes_its_own_checks(tmp_path):
    proj = scaffold(tmp_path, name="Slow Check")
    # The generated project pins its own Python in .python-version; don't inherit the
    # interpreter the test suite runs on (setup-uv exports UV_PYTHON in CI).
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "UV_PYTHON")}
    for cmd in (["uv", "sync", "-q"], ["make", "check"]):
        result = subprocess.run(cmd, cwd=proj, env=env, capture_output=True, text=True)
        assert result.returncode == 0, f"{cmd}\n{result.stdout}\n{result.stderr}"
    subprocess.run(["git", "add", "-A"], cwd=proj, check=True)
    hooks = subprocess.run(
        ["uv", "run", "pre-commit", "run", "--all-files"],
        cwd=proj, env=env, capture_output=True, text=True,
    )  # fmt: skip
    assert hooks.returncode == 0, hooks.stdout
