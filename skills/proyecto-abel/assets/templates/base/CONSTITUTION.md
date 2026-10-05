# CONSTITUTION — {{PROJECT_NAME}}

> **Verdad central del proyecto.** Este documento define el propósito, el stack, la
> estructura, las convenciones y el flujo de trabajo de `{{PROJECT_NAME}}`. Si algo aquí
> contradice al código, el código manda **y este archivo se actualiza**.

> ⚠️ **Directiva de mantenimiento:** cada vez que se realicen cambios significativos
> (nuevas funcionalidades, cambios arquitectónicos, adición de clases/módulos o ajustes
> de tecnologías), **se debe actualizar este archivo en el mismo commit** para mantener
> la verdad central del proyecto bien documentada.

---

## 0. Identidad del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | {{PROJECT_NAME}} |
| **Descripción** | {{DESCRIPTION}} |
| **Repositorio** | {{REPO_URL}} |
| **Autoría** | {{AUTHOR}} — {{AUTHOR_EMAIL}} |
| **Licencia** | MIT |
| **Rama principal** | `main` |
| **Estado** | En construcción 🚧 |

## 1. Propósito y no-propósito

### Propósito

<!-- Una o dos frases: qué problema resuelve el proyecto y para quién. -->

### No-propósito

<!-- Qué NO es este proyecto. Evita expectativas equivocadas y desvíos de alcance. -->

## 2. Alcance

### Dentro del alcance

- ...

### Fuera del alcance (por ahora)

- ...

## 3. Stack técnico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python {{PYTHON_VERSION}}+ |
| **Gestor de paquetes y entorno** | [`uv`](https://docs.astral.sh/uv/) |
{{#if PACKAGE}}| **Build backend** | `uv_build` (src-layout) |
| **Paquete Python** | `{{PACKAGE_NAME}}` |
{{/if}}{{#if TYPES}}| **Tipado estático** | [`ty`](https://github.com/astral-sh/ty) |
{{/if}}| **Testing** | [`pytest`](https://docs.pytest.org/) |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) |
| **Pre-commit** | [pre-commit](https://pre-commit.com) |
{{#if GITHUB}}| **CI/CD** | [GitHub Actions](.github/workflows/ci.yml) |
{{/if}}{{#if SCIML}}| **Notebooks** | Jupyter (`ipykernel`, grupo `notebooks`) + [`nbstripout`](https://github.com/kynan/nbstripout) |
{{/if}}{{#if ARCHIFY}}| **Diagramas de arquitectura** | [Archify](https://github.com/tt-a1i/archify) (HTML interactivo en `docs/`) |
{{/if}}{{#if GITHUB}}| **Dependencias automáticas** | [Dependabot](.github/dependabot.yml) |
{{/if}}
> ⚠️ **Regla dura:** toda gestión de dependencias y entornos pasa por `uv`. Está
> **prohibido** `pip` y `requirements.txt`.{{#if SCIML}} Única excepción documentada: dentro de
> Google Colab se instala el paquete con `pip install -e . --no-deps` (el entorno no es nuestro).{{/if}}

## 4. Estructura del repositorio

```text
{{PROJECT_SLUG}}/
{{#if PACKAGE}}├── src/{{PACKAGE_NAME}}/        # código del paquete (src-layout)
{{/if}}{{#unless PACKAGE}}├── main.py                  # punto de entrada
{{/unless}}├── tests/                   # pruebas (pytest)
├── docs/                    # documentación, ADRs e investigación
{{#if SCIML}}├── notebooks/               # exploración (salidas limpiadas con nbstripout)
├── data/                    # datos locales; raw/processed fuera de Git
├── figures/                 # figuras finales generadas por código
{{/if}}{{#if GITHUB}}├── .github/                 # gobernanza (PR/issue templates, CI, Dependabot, labels)
{{/if}}{{#if AGENTS}}├── .opencode/rules/         # reglas para agentes (tgrep)
├── AGENTS.md                # contexto para agentes LLM
├── CLAUDE.md                # contexto para Claude Code (importa AGENTS.md)
{{/if}}├── CONSTITUTION.md          # este archivo — verdad central
├── README.md                # puerta de entrada pública
├── CONTRIBUTING.md          # guía de contribución
├── CODE_OF_CONDUCT.md       # código de conducta
├── Makefile                 # automatización de tareas
├── pyproject.toml           # metadatos y dependencias (uv)
├── uv.lock                  # lockfile determinista (versionado)
├── .python-version          # versión de Python fijada
└── .pre-commit-config.yaml  # hooks de calidad
```

## 5. Convenciones de código

- **Estilo:** [PEP 8](https://peps.python.org/pep-0008/) y [PEP 257](https://peps.python.org/pep-0257/),
  impuesto por **Ruff** (`line-length = 100`, comillas dobles).
- **Tipado:** anotaciones en funciones y firmas públicas.
- **Nomenclatura:** `snake_case` (funciones/variables), `PascalCase` (clases),
  `UPPER_CASE` (constantes).
- **Docstrings:** en módulos, clases y funciones públicas.
- **Pruebas:** `pytest` con el patrón **AAA** (*Arrange · Act · Assert*).
- **Idioma:** UI, comentarios y commits en español; identificadores de código en inglés.
- **Reglas propias:**
  - <!-- Agrega aquí invariantes del dominio (p. ej. "unidades SI en todo el código", "semillas fijas"). -->
{{#if SCIML}}- **Reproducibilidad (investigación):**
  - Semillas fijadas y registradas en cada experimento.
  - Unidades y dimensiones documentadas en los docstrings.
  - Los notebooks importan desde el paquete; el código reutilizable vive en `src/`.
  - Toda figura de `figures/` se regenera con un script; nunca se edita a mano.
  - Fuentes de datos documentadas en `data/README.md`.
{{/if}}

## 6. Calidad y automatización

| Herramienta | Rol | Comando |
|-------------|-----|---------|
| `uv` | Entornos y dependencias | `uv sync` |
| Ruff | Lint + formato | `make lint` / `make format` |
{{#if TYPES}}| `ty` | Verificación de tipos | `make typecheck` |
{{/if}}| `pytest` | Pruebas | `make test` |
| `pre-commit` | Hooks antes de cada commit | `make pre-commit` |
{{#if GITHUB}}| GitHub Actions | CI (pre-commit + pruebas) | `.github/workflows/ci.yml` |
{{/if}}{{#if SCIML}}| `nbstripout` | Limpia salidas de notebooks | automático (pre-commit) |
{{/if}}
- Ningún commit se salta los hooks (`--no-verify` está prohibido salvo causa justificada y documentada).
{{#if GITHUB}}- La **CI debe estar en verde** antes de fusionar un Pull Request.
{{/if}}{{#unless GITHUB}}- `make check` debe estar en verde antes de cada push (no hay CI configurada).
{{/unless}}- Toda dependencia nueva entra con `uv add` / `uv add --dev` (nunca editando `uv.lock` a mano).

## 7. Repositorio y Git

- **Remoto (SSH):** `{{SSH_URL}}`
- **Rama principal:** `main`
- **Estrategia de ramas:** `feat/...`, `fix/...`, `docs/...`, `refactor/...`, `test/...`, `chore/...`; integración vía Pull Request.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) —
  `feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`, `chore:`.
- **Identidad git:** se resuelve sola dentro de la carpeta de repositorios configurada con
  `includeIf` (ver §11).

## 8. Flujo diario (commit + push)

```bash
# 1. Ver cambios
git status

# 2. Verificación completa (lint + formato + pruebas)
make check

# 3. Agregar y commitear (los hooks se ejecutan solos)
git add -A
git commit -m "tipo: mensaje descriptivo"

# 4. Subir a GitHub
git push
```

## 9. Historial de decisiones técnicas

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| {{DATE}} | Adoptar `uv` como gestor único de entornos y dependencias | Reproducibilidad; prohibido `pip`/`requirements.txt` |
| {{DATE}} | Adoptar Ruff (lint + formato) y pre-commit | Calidad automatizada antes de cada commit |
| {{DATE}} | Adoptar Conventional Commits | Historial legible y automatizable |
| {{DATE}} | Adoptar licencia MIT y `CONSTITUTION.md` como fuente única de verdad | Claridad legal y operativa |

## 10. Notas y tareas pendientes

- [ ] Completar las secciones marcadas de este documento.
- [ ] Configurar el remoto y proteger `main`.
- [ ] Definir la primera funcionalidad y sus pruebas.
- [ ] <!-- Agrega el roadmap del proyecto. -->

## 11. Configuración local (no trackear)

> Configuración específica de la máquina local. **NO incluir en commits.**

Dentro de la carpeta de proyectos, `~/.gitconfig` aplica:

```ini
[includeIf "gitdir:~/Repos/"]
    path = ~/.gitconfig-personal
```

`~/.gitconfig-personal`:

```ini
[user]
    name = <Tu Nombre>
    email = <tu-correo>
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes
```

> Ajusta la carpeta y tus datos. Guía completa (macOS/Windows) en el skill
> `proyecto-abel` → `references/git-identity.md`.
