# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

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
