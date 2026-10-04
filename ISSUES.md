# Issues found in upstream / Problemas encontrados en el original

Audit of [`hamsomp3/jan_skills_repository`](https://github.com/hamsomp3/jan_skills_repository)
at commit `0ea4dad` (skill `jan-project-standard` v1.0), done on 2026-10-04 by running the
scripts and the generated projects. Every item below is **fixed in `proyecto-abel` v1.1.0**
and can be reported upstream as an issue.

Auditoría del repositorio original (commit `0ea4dad`) ejecutando los scripts y los proyectos
generados. Todos los puntos están **corregidos en `proyecto-abel` v1.1.0** y pueden
reportarse al autor original.

**Severity / Severidad:** 🔴 high — breaks output silently · 🟠 medium — behavior differs from docs · 🟡 low — cosmetic or docs

| # | Sev. | Area | Issue (EN) | Problema (ES) | Fix |
|---|:----:|------|-----------|---------------|-----|
| 1 | 🔴 | `scripts/new_project.py` | The documented `--no-git` flag does not exist. `argparse` abbreviation matching reads it as `--no-github`, so `.github/` (CI, templates, Dependabot) is silently dropped. | El flag documentado `--no-git` no existe; `argparse` lo interpreta como `--no-github` y omite `.github/` sin aviso. | `allow_abbrev=False`; real `--git/--no-git` flag. |
| 2 | 🔴 | `templates/base/README.md` + renderer | The `{{#if ARCHIFY}}` block has no closing `{{/if}}`, and the regex `(.*?)` is not nesting-aware. Without `--archify`, the README loses the **"Estructura del repositorio"** heading; with `--archify`, a literal `{{#if PACKAGE}}` is left in the README. | Al bloque `{{#if ARCHIFY}}` le falta su `{{/if}}` y la regex no respeta anidamiento. Sin `--archify` desaparece la sección "Estructura del repositorio"; con `--archify` queda un `{{#if PACKAGE}}` literal. | Closing tag added; innermost-first regex; warning for unclosed blocks. |
| 3 | 🟠 | `scripts/new_project.py` | Docs say git is initialized by default, but `--git` is `store_true` (off by default). | La documentación dice que git se inicializa por defecto, pero `--git` está apagado por defecto. | `BooleanOptionalAction`, default on; skips if `.git/` exists. |
| 4 | 🟠 | renderer / `pyproject.toml` | Conditional blocks at end of file leave extra blank lines; `end-of-file-fixer` fails the very first `pre-commit run` on a fresh project. | Los bloques condicionales al final dejan líneas en blanco extra; el primer `pre-commit` falla en un proyecto recién creado. | Rendered files end with exactly one newline. |
| 5 | 🟠 | `templates/base/CONSTITUTION.md` | Every generated constitution hardcodes the author's personal folder `~/Desktop/Repositorios/personal/` as "the" Git identity path, even for other users. | Toda constitución generada fija la carpeta personal del autor como ruta de identidad Git, incluso para otros usuarios. | Generic wording pointing to §11. |
| 6 | 🟡 | `SKILL.md` frontmatter | `compatibility` says "Python 3", but the scaffolder imports `tomllib` (Python ≥ 3.11). | Dice "Python 3", pero el script usa `tomllib` (requiere ≥ 3.11). | Says 3.11+. |
| 7 | 🟡 | `references/github.md` | Points to `references/agent-context.md` for Git identity; the right file is `references/git-identity.md`. | Remite a `agent-context.md` para la identidad Git; el correcto es `git-identity.md`. | Link fixed. |
| 8 | 🟡 | `scripts/new_project.py` | With `--archify`, the "next steps" message prints a literal `cd <path>` instead of the real path. | Con `--archify`, los "siguientes pasos" muestran `cd <path>` literal. | Uses the real path. |
| 9 | 🟡 | `scripts/setup_git_identity.py` | Same abbreviation risk as #1 (prefix flags accepted silently). | Mismo riesgo de abreviaturas que el #1. | `allow_abbrev=False`. |

## Design limitations (not bugs) / Limitaciones de diseño (no son errores)

These are trade-offs of the upstream design, addressed in the fork by **adding** options, not
by changing the upstream rules.

| Limitation (EN) | Limitación (ES) | How `proyecto-abel` handles it |
|-----------------|-----------------|--------------------------------|
| No place for notebooks, data or figures; the docs push `.ipynb → .py`. | No hay lugar para notebooks, datos ni figuras. | `--sciml` (default): `notebooks/`, `data/`, `figures/`, `nbstripout`, `make notebooks`. |
| "Only uv" conflicts with Google Colab's preinstalled CUDA PyTorch/JAX. | "Solo uv" choca con el PyTorch/JAX con CUDA de Colab. | Documented exception in `references/colab.md`: `pip install -e . --no-deps` inside Colab only. |
| Agent context targets OpenCode (`.opencode/`, `tgrep`); no `CLAUDE.md`. | El contexto de agentes apunta a OpenCode; no hay `CLAUDE.md`. | `CLAUDE.md` that imports `AGENTS.md` plus research rules (seeds, units, don't touch data). |
| Full GitHub governance is heavy for a single-author paper repo. | La gobernanza completa es pesada para un repo de un solo autor. | `--minimal` documented as the paper-repo option. |
| Generated files are Spanish-only. | Los archivos generados son solo en español. | New SciML files are bilingual; full `--lang en` is on the roadmap. |

## Roadmap

- [ ] `--lang en|es` to render all templates in either language.
- [ ] `CITATION.cff` template (needed for Zenodo DOI and journal code availability statements).
- [ ] Optional `reproduce` Makefile target that regenerates every figure in `figures/`.
- [ ] Open issues #1–#9 upstream (draft text: one issue per row above).
