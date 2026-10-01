# jan_skills_repository

[![skills.sh](https://skills.sh/b/hamsomp3/jan_skills_repository)](https://skills.sh/hamsomp3/jan_skills_repository)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-standard-3776AB.svg)](https://agentskills.io)

Repositorio de **skills** (Agent Skills) de Jan Polanco Velasco. Cada skill vive en su
propia carpeta bajo [`skills/`](./skills) con un `SKILL.md` (frontmatter YAML + instrucciones),
siguiendo el [estándar de Agent Skills](https://agentskills.io).

## Skills disponibles

| Skill | Descripción |
|-------|-------------|
| [`jan-project-standard`](./skills/jan-project-standard/SKILL.md) | Estandariza proyectos personales y académicos: `uv` + Astral, **src-layout**, Ruff, pre-commit, Makefile, `CONSTITUTION.md` como fuente única de verdad, Conventional Commits, README con badges, licencia MIT, gobernanza GitHub (PR/issue templates, CI, Dependabot, labels), contexto para agentes (`AGENTS.md`, `.opencode/`, tgrep), **identidad Git automática** (`includeIf`, perfiles Jan y propio para macOS/Windows) y **diagramas de arquitectura con [Archify](https://github.com/tt-a1i/archify)**. |

## Instalación

Con el CLI de [skills.sh](https://www.skills.sh):

```bash
# Instalar en el proyecto actual (se commitea con el repo)
npx skills add hamsomp3/jan_skills_repository --skill jan-project-standard

# Instalar globalmente (disponible en todos los proyectos)
npx skills add hamsomp3/jan_skills_repository --skill jan-project-standard -g

# Instalar para agentes concretos
npx skills add hamsomp3/jan_skills_repository --skill jan-project-standard -a opencode -a claude-code

# Sin prompts (CI-friendly)
npx skills add hamsomp3/jan_skills_repository --skill jan-project-standard -g -a opencode -y
```

Para listar las skills del repositorio sin instalar:

```bash
npx skills add hamsomp3/jan_skills_repository --list
```

> También puedes clonar y usar el script directamente:
> `python3 skills/jan-project-standard/scripts/new_project.py --help`

## Ejemplos de uso (copy-paste)

Invoca la skill en lenguaje natural. Copia cualquiera de estos bloques y ajústalo.

### 1 · Proyecto nuevo (soy Jan)

```text
@jan-project-standard crea un proyecto nuevo.
Nombre: "Detector de Neumonía" · App con Streamlit · paquete Python.
Descripción: "Clasificador de radiografías con Grad-CAM."
Incluye Archify para el diagrama de arquitectura.
```

### 2 · Proyecto existente — estandarizar SIN borrar

```text
@jan-project-standard este proyecto ya existe y tiene README y CONSTITUTION.md.
Repositorio remoto: git@github.com:pedro/mi-proyecto.git
No elimines nada: audítalo, dime qué falta y complétalo.
Respeta mi README y mi CONSTITUTION.md; solo mejora y añade.
```

### 3 · NO soy Jan (alumno / compañero)

```text
@jan-project-standard no soy Jan. Me llamo "Pedro Pérez" (pedro@example.com),
mi repo es git@github.com:pedro/proyecto.git y ya existe con README.
Quiero adoptar el estándar: uv, Ruff, pre-commit, Makefile y CONSTITUTION.md.
No borres nada existente; completa lo que falte.
```

### 4 · Solo auditar (no toca nada)

```text
@jan-project-standard audita este proyecto existente y muéstrame el informe
(FALTA / DIFIERE / OK) sin modificar nada.
```

### 5 · Añadir arquitectura (Archify)

```text
@jan-project-standard instala Archify y genera docs/arquitectura.html a partir
de este repositorio; luego enlázalo en la sección de arquitectura del README.
```

### 6 · Identidad Git automática (macOS / Windows)

```text
@jan-project-standard no soy Jan. Configura mi identidad Git automática
(includeIf): Pedro Pérez <pedro@example.com>, llave ~/.ssh/id_ed25519,
carpeta ~/Repos. Estoy en macOS.
```

### 7 · Actualizar la constitución

```text
@jan-project-standard actualiza CONSTITUTION.md con el nuevo módulo de
autenticación y registra la decisión en el historial. No borres lo anterior.
```

### Equivalentes por CLI (sin agente)

```bash
D=skills/jan-project-standard/scripts

python3 $D/new_project.py --path . --audit                    # auditar (no escribe)
python3 $D/new_project.py --path ./nuevo --name "Mi Proyecto" \
    --description "..." --archify --git                        # crear
python3 $D/new_project.py --path . --name "Mi Proyecto"        # completar (omite lo existente)
python3 $D/setup_git_identity.py --name "Pedro Pérez" --email pedro@example.com \
    --key ~/.ssh/id_ed25519 --dir ~/Repos --platform mac        # identidad Git automática
```

> **Regla de oro:** en un proyecto existente, sin `--force` el scaffolder **nunca** sobrescribe
> archivos; solo crea los que faltan. Los cambios sobre archivos propios se hacen a mano,
> fusionando.

## Estructura

```text
jan_skills_repository/
├── README.md
├── LICENSE
├── .gitignore
└── skills/
    └── jan-project-standard/
        ├── SKILL.md              # metadata + instrucciones
        ├── references/           # documentación de apoyo (carga progresiva)
        ├── scripts/              # scaffolder ejecutable
        └── assets/templates/     # plantillas de archivos del estándar
```

## Crear una skill nueva

1. Crea `skills/<nombre>/SKILL.md` con frontmatter `name` (igual al de la carpeta) y `description`.
2. Añade `references/`, `scripts/` y `assets/` según lo necesites.
3. Valida el frontmatter (nombre en minúsculas, sin guiones dobles, ≤ 64 caracteres).
4. **Entrecomilla los valores con `: `** (dos puntos + espacio). YAML lo interpreta como un
   mapeo anidado y falla con *mapping values are not allowed in this context*:
   `description: "Texto: con dos puntos"`. Vale para `description`, `title`, etc.
5. Añádela a la tabla de **Skills disponibles** de este README.

## Licencia

[MIT](./LICENSE) © 2026 Jan Polanco Velasco
