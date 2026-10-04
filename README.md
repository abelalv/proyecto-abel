# proyecto-abel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-standard-3776AB.svg)](https://agentskills.io)
[![Fork of](https://img.shields.io/badge/fork%20of-jan__skills__repository-lightgrey.svg)](https://github.com/hamsomp3/jan_skills_repository)

**EN** — An [Agent Skill](https://agentskills.io) that scaffolds, audits and standardizes
Python research and teaching repositories: `uv` + Ruff + pre-commit + pytest + Makefile,
`CONSTITUTION.md` as the single source of truth, a Scientific ML layer (notebooks, data,
figures, Colab) and agent context for Claude Code. Fork of Jan Polanco Velasco's
[`jan-project-standard`](https://github.com/hamsomp3/jan_skills_repository) with
[9 bug fixes](ISSUES.md).

**ES** — Un skill que crea, audita y estandariza repositorios de investigación y de curso en
Python, con una capa de ML científico y contexto para Claude Code. Fork de
`jan-project-standard` con [9 correcciones](ISSUES.md).

| | |
|---|---|
| 📘 Skill | [`skills/proyecto-abel/SKILL.md`](skills/proyecto-abel/SKILL.md) |
| 🗺️ Workflow / Flujo | [`docs/workflow.md`](docs/workflow.md) (bilingual Mermaid diagrams) |
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

## Structure / Estructura

```text
proyecto-abel/
├── README.md · ISSUES.md · CHANGELOG.md · LICENSE
├── docs/workflow.md                 # bilingual workflow diagrams
└── skills/proyecto-abel/
    ├── SKILL.md                     # metadata + instructions
    ├── references/                  # loaded on demand (incl. colab.md)
    ├── scripts/                     # new_project.py, setup_git_identity.py
    └── assets/templates/            # base · github · agents · sciml
```

## Credits / Créditos

Original standard, templates and scripts: **Jan Polanco Velasco**
([`hamsomp3/jan_skills_repository`](https://github.com/hamsomp3/jan_skills_repository), MIT).
Fork, fixes and SciML layer: **Abel Alvarez Bustos**, Pontificia Universidad Javeriana Cali.

[MIT](LICENSE)
