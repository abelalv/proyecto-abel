---
name: jan-project-standard
description: Estandariza proyectos personales y académicos siguiendo las convenciones de Jan Polanco Velasco. Scaffolding y gobierno de repositorios Python con uv/Astral (Python 3.13+), src-layout, Ruff, pre-commit, Makefile, pytest, CONSTITUTION.md como fuente única de verdad, Conventional Commits, README profesional con badges, licencia MIT, gobernanza de GitHub (plantillas de PR/issue, CI, Dependabot, labels) y archivos de contexto para agentes (AGENTS.md, .opencode/, tgrep). Úsala al crear un proyecto o repositorio nuevo, al redactar o actualizar un CONSTITUTION.md, al configurar uv + Ruff + pre-commit, al añadir un Makefile, al preparar un README con badges, al conectar un repo a GitHub, o al auditar/estandarizar un proyecto existente. Use when scaffolding a new Python repository, writing or updating a CONSTITUTION.md, setting up uv, Ruff, pre-commit or CI, or standardizing an existing project.
license: MIT
compatibility: Requiere Python 3 (el scaffolder usa solo la biblioteca estándar). Para aplicar el estándar al proyecto destino se recomienda uv, git y, opcionalmente, gh.
metadata:
  author: Jan Polanco Velasco
  version: "1.0"
  homepage: https://github.com/hamsomp3/jan_skills_repository
---

# Estándar de proyectos — Jan Polanco Velasco

Este skill encapsula **cómo se construyen y gobiernan los proyectos** de Jan: una forma
de trabajar repetible, reproducible y auditable que ya está aplicada en decenas de
repositorios personales y académicos.

> **Filosofía central:** todo lo que vive dentro de la carpeta del proyecto tiene una
> instrucción escrita. El documento que la contiene es **`CONSTITUTION.md`**, la
> **fuente única de verdad**. Un proyecto sano es un proyecto donde un agente (o una
> persona) puede leer la constitución y operar sin adivinar.

---

## Cuándo usar este skill

- Crear un proyecto o repositorio nuevo desde cero.
- Estandarizar un proyecto existente que no sigue el estándar.
- Redactar, poblar o actualizar un `CONSTITUTION.md`.
- Configurar `uv` + Ruff + pre-commit + Makefile + CI.
- Conectar un proyecto local a un repositorio de GitHub.
- Preparar un README profesional con badges, licencia y estructura.

## Cuándo NO usarlo

- Proyectos que no son de Jan y exigen otro estilo (respeta el `CONSTITUTION.md` del repo).
- Cambios triviales de una línea en un repo ya estandarizado (no re-scaffold).

---

## Las 10 reglas no negociables

1. **CONSTITUTION.md primero.** La constitución se crea al inicio y se **actualiza en el
   mismo commit** ante cualquier cambio arquitectónico, tecnológico o de proceso.
2. **`uv` manda.** Gestión de entornos y dependencias **solo** con `uv`. Prohibido `pip`
   y `requirements.txt`. Dependencias en `pyproject.toml`; `uv.lock` **sí se versiona**.
3. **Python 3.13+** fijado en `.python-version` y en `requires-python`.
4. **src-layout** (`src/<paquete>/`) con build backend `uv_build`, salvo apps simples
   (modo `--app`).
5. **Calidad automatizada:** Ruff (lint + formato), pre-commit y pytest. Nada se sube
   con `make check` en rojo. `--no-verify` está prohibido salvo causa documentada.
6. **Makefile como interfaz.** Todos los comandos del proyecto se exponen en targets
   (`make help` los lista). La paridad local ↔ CI es obligatoria: el CI corre lo mismo.
7. **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`,
   `chore:`) en un solo idioma claro; descripciones en imperativo.
8. **GitHub gobernado:** plantilla de Pull Request, plantillas de issue, CI, Dependabot,
   labels declarativas y rama `main` protegida por PRs.
9. **README profesional:** badges, tabla de contenidos, información académica cuando
   aplique, stack, primeros pasos, estructura, contribución y licencia.
10. **Identidad Git automática:** la carpeta `~/Desktop/Repositorios/personal/` hereda
    nombre, correo y llave SSH vía `includeIf` en `~/.gitconfig` (ver más abajo).

---

## Modo A — Crear un proyecto nuevo

### Paso 1 · Ejecutar el scaffolder

El scaffolder copia las plantillas, sustituye variables y deja el proyecto listo. Usa
solo la biblioteca estándar de Python (no requiere `uv` para ejecutarse):

```bash
python3 <SKILL_DIR>/scripts/new_project.py \
  --name "Nombre del Proyecto" \
  --path ./nombre-del-proyecto \
  --owner hamsomp3 \
  --description "Descripción breve del proyecto." \
  --git
```

Opciones más usadas:

| Opción | Efecto |
|--------|--------|
| `--name` | Nombre legible del proyecto (obligatorio). |
| `--path` | Carpeta destino (por defecto `.`). |
| `--repo` | Nombre del repo en GitHub (por defecto, slug del nombre). |
| `--owner` | Cuenta/organización de GitHub (por defecto `hamsomp3`). |
| `--description` | Descripción de una línea (va al README, pyproject y constitución). |
| `--author` / `--email` | Autoría (por defecto `Jan Polanco V.` / `hamsomp3@gmail.com`). |
| `--python-version` | Versión de Python (por defecto `3.13`). |
| `--app` | Proyecto de aplicación (sin paquete ni build-system), en vez de src-layout. |
| `--minimal` | Solo lo esencial: sin `.github`, sin `AGENTS.md`/`.opencode`, sin extras. |
| `--no-types` | Omite `ty` (tipado estático) de dependencias, Makefile y docs. |
| `--no-github` | No genera `.github/`. |
| `--no-agents` | No genera `AGENTS.md` ni `.opencode/`. |
| `--git` / `--no-git` | Inicializa el repositorio git (rama `main`). Por defecto: sí. |
| `--sync` | Ejecuta `uv sync` y `uv run pre-commit install` al terminar. |
| `--force` | Sobrescribe archivos existentes. |
| `--dry-run` | Muestra qué haría sin escribir nada. |

> ⚠️ **Antes de sobrescribir:** si la carpeta destino ya tiene archivos (sobre todo un
> `CONSTITUTION.md` o `README.md` propios), **no uses `--force` a ciegas**. Investiga,
> lee lo existente y fusiona en lugar de reemplazar.

### Paso 2 · Poblar la constitución

Abre `CONSTITUTION.md` y completa, como mínimo, las secciones marcadas con `<!-- ... -->`:

- **Propósito** y **no-propósito** (una o dos frases cada uno).
- **Alcance** (qué entra y qué no).
- **Stack técnico** (confirma o corrige la tabla).
- **Decisiones iniciales** en el historial (fecha + decisión + motivo).
- **Notas y tareas pendientes** (roadmap en formato checklist).

### Paso 3 · Verificar el entorno

```bash
cd nombre-del-proyecto
uv sync
uv run pre-commit install
make check     # lint + formato + pruebas
```

### Paso 4 · Conectar a GitHub

Crea el repositorio (si no existe) y publica:

```bash
gh repo create hamsomp3/<repo> --private --source=. --remote=origin --push
# o, si el repo ya existe:
git remote add origin git@github.com:hamsomp3/<repo>.git
git push -u origin main
```

Luego protege `main` y verifica que la CI esté en verde. Detalle en
[`references/github.md`](references/github.md).

---

## Modo B — Estandarizar un proyecto existente

1. **Audita** el proyecto contra el manifiesto de abajo; anota qué falta o difiere.
2. **Lee** el `CONSTITUTION.md` y el `README.md` existentes antes de tocar nada
   (son trabajo del usuario: no los reemplaces, **complétalos**).
3. **Añade** los archivos ausentes uno a uno, adaptando variables
   (`{{PROJECT_NAME}}`, `{{PACKAGE_NAME}}`, …) al proyecto real.
4. **Migra** lo que aplique: `requirements.txt` → `pyproject.toml` con `uv add`;
   scripts sueltos → `src/<paquete>/`; `.ipynb` → `.py`.
5. **Verifica** con `make check` y registra el cambio en el historial de la constitución.

> El scaffolder sirve como referencia de las plantillas: puedes generar un proyecto
> temporal en `/tmp` con `--dry-run` o copiando un archivo concreto desde
> `assets/templates/`, y adaptarlo.

---

## Manifiesto de archivos del estándar

| Archivo | Propósito |
|---------|-----------|
| `CONSTITUTION.md` | Fuente única de verdad: propósito, stack, estructura, convenciones, flujo y decisiones. |
| `README.md` | Puerta de entrada pública: badges, TOC, descripción, stack, primeros pasos, estructura, contribución, licencia. |
| `pyproject.toml` | Metadatos, dependencias (`uv`), configuración de Ruff y pytest. |
| `uv.lock` | Lockfile determinista (**versionado**). |
| `.python-version` | Versión de Python fijada (`3.13`). |
| `.gitignore` | Ignora venvs, cachés, secretos, artefactos pesados y datos. |
| `.editorconfig` | Convenciones de estilo entre editores. |
| `Makefile` | Interfaz de comandos (`help`, `install`, `dev`, `lint`, `format`, `test`, `check`, `clean`). |
| `.pre-commit-config.yaml` | Higiene de archivos + Ruff + `uv-lock` antes de cada commit. |
| `LICENSE` | MIT por defecto. |
| `CONTRIBUTING.md` | Entorno, ramas, estándares, commits y proceso de PR. |
| `CODE_OF_CONDUCT.md` | Contributor Covenant 2.1 (proyectos con colaboración). |
| `AGENTS.md` | Contexto para agentes LLM (stack, flujo, reglas, tgrep). |
| `.opencode/rules/tgrep.md` | Regla de búsqueda con `tgrep` para agentes en OpenCode. |
| `.github/pull_request_template.md` | Plantilla de PR (Conventional Commits + checklist). |
| `.github/ISSUE_TEMPLATE/` | Formularios de bug, funcionalidad e investigación (spike). |
| `.github/workflows/ci.yml` | CI: pre-commit + pruebas. |
| `.github/workflows/labels.yml` | Sincroniza labels desde `.github/labels.yml`. |
| `.github/labels.yml` | Fuente única de las etiquetas del repositorio. |
| `.github/dependabot.yml` | Actualización automática de dependencias (`uv` y Actions). |
| `src/<paquete>/` | Código del paquete (src-layout). |
| `tests/` | Pruebas con pytest (patrón AAA). |
| `docs/` | Documentación, ADRs, spikes e investigación. |

---

## Variables de las plantillas

Las plantillas bajo `assets/templates/` usan marcadores que el scaffolder sustituye.
Si editas a mano, reemplázalos todos:

| Marcador | Significado |
|----------|-------------|
| `{{PROJECT_NAME}}` | Nombre legible (`Mi Proyecto`). |
| `{{PROJECT_SLUG}}` | Identificador kebab-case (`mi-proyecto`), usado como carpeta y repo. |
| `{{PACKAGE_NAME}}` | Identificador snake_case (`mi_proyecto`), usado como paquete Python. |
| `{{DESCRIPTION}}` | Descripción de una línea. |
| `{{OWNER}}` / `{{REPO}}` | Cuenta y nombre del repositorio. |
| `{{REPO_URL}}` / `{{SSH_URL}}` | URLs HTTPS y SSH del repositorio. |
| `{{AUTHOR}}` / `{{AUTHOR_EMAIL}}` | Autoría. |
| `{{PYTHON_VERSION}}` | Versión de Python (`3.13`). |
| `{{YEAR}}` / `{{DATE}}` | Año y fecha ISO. |

Bloques condicionales (se eliminan si la bandera es falsa):
`{{#if PACKAGE}}…{{/if}}` (src-layout), `{{#if TYPES}}…{{/if}}` (`ty`),
`{{#if GITHUB}}…{{/if}}`, `{{#if AGENTS}}…{{/if}}`.

---

## Documentación de apoyo

Carga estos archivos **solo cuando los necesites** (divulgación progresiva):

| Referencia | Contenido |
|------------|-----------|
| [`references/constitution.md`](references/constitution.md) | Anatomía completa del `CONSTITUTION.md` sección por sección, con ejemplos. |
| [`references/python-stack.md`](references/python-stack.md) | `uv`, `pyproject.toml`, Ruff, Makefile, pre-commit, `.editorconfig`, `.gitignore`. |
| [`references/github.md`](references/github.md) | Creación del repo, remotos SSH, badges, plantillas, CI, Dependabot, labels, ramas. |
| [`references/agent-context.md`](references/agent-context.md) | `AGENTS.md`, `.opencode/rules/`, tgrep e identidad Git automática. |
| [`references/slidev.md`](references/slidev.md) | Presentaciones con Slidev (proyectos de curso): monolito, hub, reglas de sintaxis, export. |

---

## Identidad Git automática (contexto de la máquina)

Dentro de `~/Desktop/Repositorios/personal/`, `~/.gitconfig` incluye:

```ini
[includeIf "gitdir:~/Desktop/Repositorios/personal/"]
    path = ~/.gitconfig-personal
```

Y `~/.gitconfig-personal` define:

```ini
[user]
    name = Jan Polanco V.
    email = hamsomp3@gmail.com
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes
```

**Efecto:** todo repo dentro de esa carpeta usa automáticamente el nombre, correo y
llave SSH correctos, sin flags ni `gh auth` por proyecto. Preferir remotos **SSH**
(`git@github.com:hamsomp3/<repo>.git`); HTTPS puede resolver con un token de otra cuenta.

> ⚙️ Esta sección es configuración **local de la máquina**: nunca se commitea como
> parte del proyecto (vive en la constitución solo como nota, no como archivo del repo).

---

## Flujo diario (commit + push)

```bash
git status                       # 1. ver cambios
make check                       # 2. lint + formato + (tipos) + pruebas
git add -A                       # 3. agregar
git commit -m "tipo: mensaje"    # 4. commitear (los hooks se ejecutan solos)
git push                         # 5. subir
```

---

## Checklist de verificación

Antes de dar por terminado un proyecto o un cambio:

- [ ] `CONSTITUTION.md` existe y está poblado (propósito, stack, estructura, flujo, decisiones).
- [ ] `uv sync` funciona y `uv.lock` está versionado.
- [ ] `make check` pasa en verde (lint + formato + pruebas).
- [ ] `uv run pre-commit run --all-files` pasa (hooks instalados).
- [ ] `README.md` tiene badges, TOC, descripción, stack, primeros pasos y licencia.
- [ ] `LICENSE` presente (MIT por defecto).
- [ ] `.github/` con PR template, issue templates, CI, Dependabot y labels (si aplica).
- [ ] `AGENTS.md` (y `.opencode/rules/tgrep.md`) describen el proyecto para agentes (si aplica).
- [ ] Sin secretos, datos personales ni artefactos pesados versionados.
- [ ] El historial de decisiones de la constitución registra los cambios significativos.

---

## Directiva de mantenimiento

> Cada vez que se realicen cambios significativos (nuevas funcionalidades, cambios
> arquitectónicos, adición de clases/módulos o ajustes de tecnologías), **se debe
> actualizar `CONSTITUTION.md`** en el mismo commit para mantener la verdad central del
> proyecto. El checklist de la plantilla de Pull Request lo verifica explícitamente.
