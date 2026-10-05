# proyecto-abel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-standard-3776AB.svg)](https://agentskills.io)
[![Fork of](https://img.shields.io/badge/fork%20of-jan__skills__repository-lightgrey.svg)](https://github.com/hamsomp3/jan_skills_repository)

**EN** — An [Agent Skill](https://agentskills.io) that scaffolds, audits and standardizes
Python research and teaching repositories: `uv` + Ruff + pre-commit + pytest + Makefile,
`CONSTITUTION.md` as the single source of truth, a Scientific ML layer (notebooks, data,
figures, Colab) and agent context for Claude Code. Fork of Jan Polanco Velasco's
[`jan-project-standard`](https://github.com/hamsomp3/jan_skills_repository) with
[10 bug fixes](ISSUES.md) and an automated test suite.

**ES** — Un skill que crea, audita y estandariza repositorios de investigación y de curso en
Python, con una capa de ML científico y contexto para Claude Code. Fork de
`jan-project-standard` con [10 correcciones](ISSUES.md) y pruebas automáticas.

| | |
|---|---|
| 📘 Skill | [`skills/proyecto-abel/SKILL.md`](skills/proyecto-abel/SKILL.md) |
| 🗺️ Workflow / Flujo | [`references/workflow.md`](skills/proyecto-abel/references/workflow.md) (Mermaid) · [`docs/workflow.html`](docs/workflow.html) (interactive EN/ES page) · SVGs in [`docs/`](docs) |
| 🐞 Issues / Problemas | [`ISSUES.md`](ISSUES.md) |
| 📝 Changes / Cambios | [`CHANGELOG.md`](CHANGELOG.md) |

## Install / Instalación

```bash
# Claude Code / OpenCode via skills.sh (replace <user> with your GitHub user)
npx skills add <user>/proyecto-abel --skill proyecto-abel -g

# Or manually for Claude Code / O manualmente
git clone git@github.com:<user>/proyecto-abel.git
cp -r proyecto-abel/skills/proyecto-abel ~/.claude/skills/
```

## Quick use / Uso rápido

Natural language / Lenguaje natural:

```text
@proyecto-abel create a new research project "PINN Heat Equation",
package mode, with notebooks, for a Q1 paper.

@proyecto-abel audita este repositorio sin modificar nada y dime qué falta.

@proyecto-abel crea un proyecto mínimo para mis estudiantes de Modelación (--app).
```

CLI (no agent / sin agente):

```bash
S=skills/proyecto-abel/scripts
python3 $S/new_project.py --name "PINN Heat" --description "..."   # SciML + git by default
python3 $S/new_project.py --name "Paper X" --minimal --sciml        # single-author paper
python3 $S/new_project.py --name "Taller 1" --app --no-sciml        # course app
python3 $S/new_project.py --path . --audit                          # audit only, writes nothing
```

> **Golden rule / Regla de oro:** without `--force` the scaffolder never overwrites existing
> files. / Sin `--force` nunca sobrescribe archivos existentes.

## Development / Desarrollo

```bash
make test        # 16 fast tests: renderer, every mode, audit, identity, SKILL.md
make test-slow   # + end-to-end: generate a project, uv sync, make check, pre-commit
make lint        # Ruff on scripts and tests
```

CI runs `make lint` and `make test-slow` on Python 3.11 and 3.13
([`.github/workflows/test.yml`](.github/workflows/test.yml)).

## Structure / Estructura

```text
proyecto-abel/
├── README.md · ISSUES.md · CHANGELOG.md · LICENSE · Makefile
├── .github/workflows/test.yml       # CI for the skill itself
├── docs/                            # workflow.html (built) + .fragment.html (source) + SVGs
├── tools/build_workflow_page.py     # make page → rebuilds docs/workflow.html
├── tests/test_scaffolder.py         # automated tests
└── skills/proyecto-abel/            # ← the installable skill
    ├── SKILL.md                     # metadata + instructions
    ├── references/                  # loaded on demand (workflow, colab, git identity…)
    ├── scripts/                     # new_project.py, setup_git_identity.py
    └── assets/templates/            # base · github · agents · sciml
```

## Credits / Créditos

Original standard, templates and scripts: **Jan Polanco Velasco**
([`hamsomp3/jan_skills_repository`](https://github.com/hamsomp3/jan_skills_repository), MIT).
Fork, fixes and SciML layer: **Abel Alvarez Bustos**, Pontificia Universidad Javeriana Cali.

[MIT](LICENSE)
