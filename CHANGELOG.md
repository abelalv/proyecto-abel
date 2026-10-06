# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

## [1.3.0] — 2026-10-06

### Added / Añadido
- `references/examples.md`: 10 copy-paste scenarios with prompts in EN/ES, CLI commands and real output (research package, paper, course workshop, existing repo, dry run, Colab, constitution decision, Git identity, Archify, daily loop) plus prompt-writing tips.
- README "Examples" table; SKILL.md links the guide.
- Tests run every documented example command (15) so the guide cannot drift from the code.

### Fixed / Corregido
- `--minimal --sciml` now keeps `notebooks/`, `data/`, `figures/`. (ISSUES #11)
- Completing an existing repository now follows its `pyproject.toml` (Python version, `ty`) and prints the `uv add` commands and `[tool.*]` tables needed to make `make check` pass. (#12)

## [1.2.0] — 2026-10-05

### Fixed / Corregido
- Invocation template in SKILL.md still said `@jan-project-standard`; now `@proyecto-abel`.
- Constitution/contributing templates described `.github/`, CI and agent files even when they were not generated. (ISSUES #10)
- Constitution reference used examples from an unrelated finance project; replaced with SciML examples (SI units, seeds, PINN decisions).

### Added / Añadido
- Test suite (`tests/`, 17 tests): renderer, every scaffolder mode, audit, no-overwrite, identity script, SKILL.md frontmatter and links, and an end-to-end check (`uv sync` + `make check` + pre-commit) on a generated project.
- Root `Makefile` (`make test`, `make test-slow`, `make lint`) and GitHub Actions on Python 3.11 and 3.13.
- SciML and Claude Code layers documented everywhere: rule 11 (scientific reproducibility), Colab exception to the uv rule, `nbstripout` and `make notebooks` in references, conditional SciML sections in the generated constitution.
- `docs/workflow.html`: standalone bilingual page that opens in any browser.

### Changed / Cambiado
- Workflow diagrams moved to `skills/proyecto-abel/references/workflow.md` so they ship with the installed skill.
- Upstream credit kept only in LICENSE, README credits, CHANGELOG, ISSUES and SKILL.md metadata.

## [1.1.0] — 2026-10-04 · proyecto-abel (fork)

Forked from `hamsomp3/jan_skills_repository` @ `0ea4dad` (`jan-project-standard` v1.0).

### Fixed / Corregido
- `--no-git` was parsed as `--no-github` (argparse abbreviations) → `.github/` silently dropped. (ISSUES #1)
- README template: unclosed `{{#if ARCHIFY}}` + non-nesting regex removed the "Estructura del repositorio" section. (#2)
- `--git` now defaults to on, as documented; `--no-git` exists. (#3)
- Rendered files end with a single newline; first `pre-commit run` passes. (#4)
- Generated `CONSTITUTION.md` no longer hardcodes the upstream author's folder. (#5)
- Docs: Python ≥ 3.11 requirement, broken cross-reference, `cd <path>` message. (#6–#9)

### Added / Añadido
- `--sciml/--no-sciml` (default on): `notebooks/`, `data/`, `figures/` (bilingual READMEs), `nbstripout` hook, `notebooks` dependency group, `make notebooks`, research `.gitignore` rules.
- `CLAUDE.md` template (imports `AGENTS.md`).
- `references/colab.md`: Colab/GPU conventions.
- `docs/workflow.md`: bilingual Mermaid workflow diagrams.
- `ISSUES.md`: organized audit of upstream issues.

### Changed / Cambiado
- Skill renamed `jan-project-standard` → `proyecto-abel`; bilingual SKILL.md header and description.
- Git identity Perfil A is now Abel's (Ubuntu); Linux documented for Perfil B.
