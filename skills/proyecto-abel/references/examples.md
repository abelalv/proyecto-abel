# Ejemplos de uso / Usage examples

Ten copy-paste scenarios. Each one shows **(a)** what to ask the agent, in English or
Spanish, and **(b)** the equivalent command if you prefer the terminal. Outputs shown are
real runs of the scaffolder.

Diez escenarios para copiar y pegar. Cada uno muestra **(a)** qué pedirle al agente y
**(b)** el comando equivalente. Las salidas son ejecuciones reales.

In every command, `S` is the folder of the skill's scripts / En cada comando `S` es la
carpeta de scripts del skill:

```bash
S=~/.claude/skills/proyecto-abel/scripts      # instalado con npx skills add ... -g
# o, desde un clon del repositorio:  S=skills/proyecto-abel/scripts
```

| # | Scenario / Escenario | Key flags |
|---|----------------------|-----------|
| 1 | New research package (PINN, GNN) / Paquete de investigación | *(defaults)* |
| 2 | Single-author paper / Artículo de un autor | `--minimal --sciml` |
| 3 | Course workshop for students / Taller de curso | `--app --no-sciml --no-github` |
| 4 | Existing repository: audit, complete, align / Repo existente | `--audit`, then no `--force` |
| 5 | Preview before writing / Previsualizar | `--dry-run` |
| 6 | Working in Google Colab | `--python-version` |
| 7 | Recording a decision in the constitution / Registrar una decisión | *(agent only)* |
| 8 | Automatic Git identity / Identidad Git automática | `setup_git_identity.py` |
| 9 | Architecture diagram / Diagrama de arquitectura | `--archify` |
| 10 | Daily loop after setup / Ciclo diario | `make …` |

---

## 1 · New research package / Paquete de investigación nuevo

Use for code that will back a paper and may be reused: a PINN solver, a GNN model, an
epidemiological simulator. You get everything: src-layout package, notebooks/data/figures,
GitHub CI, `AGENTS.md` + `CLAUDE.md`, and git initialized.

**Prompt (EN):**

```text
@proyecto-abel create a new research project "PINN Rumor Inverse".
Description: "Coefficient inverse problem for rumor diffusion with PINNs."
Package mode, with notebooks, for a Q1 paper. My GitHub user is abelalv.
```

**Prompt (ES):**

```text
@proyecto-abel crea un proyecto de investigación nuevo "PINN Rumor Inverse".
Descripción: "Problema inverso de coeficientes en difusión de rumores con PINNs."
Modo paquete, con notebooks, para un artículo Q1. Mi usuario de GitHub es abelalv.
```

**CLI:**

```bash
python3 $S/new_project.py --name "PINN Rumor Inverse" --path ./pinn-rumor-inverse --description "Problema inverso de coeficientes en difusión de rumores con PINNs." --owner abelalv
```

**Result / Resultado** (30 files):

```text
pinn-rumor-inverse/
├── .github/            # CI, PR/issue templates, Dependabot, labels
├── .opencode/rules/    # tgrep rule for OpenCode
├── src/pinn_rumor_inverse/__init__.py
├── tests/test_smoke.py
├── notebooks/README.md # naming convention + Colab cell
├── data/README.md      # data-source table (URL, DOI, GEE asset, license)
├── figures/README.md   # figN_description.pdf convention
├── docs/README.md
├── AGENTS.md · CLAUDE.md · CONSTITUTION.md · README.md · CONTRIBUTING.md
├── Makefile · pyproject.toml · .pre-commit-config.yaml · .python-version
└── LICENSE · CODE_OF_CONDUCT.md · .editorconfig · .gitignore
```

**Next / Después:**

```bash
cd pinn-rumor-inverse
make dev            # uv sync + pre-commit hooks
make notebooks      # Jupyter kernel "PINN Rumor Inverse"
uv add torch numpy scipy matplotlib
make check          # lint + format + types + tests → must be green
```

Then ask the agent / Luego pide al agente:

```text
@proyecto-abel completa CONSTITUTION.md: propósito = estimar el coeficiente de difusión
D(x) en un modelo de rumores; no-propósito = predecir rumores reales; stack = PyTorch.
```

---

## 2 · Single-author paper / Artículo de un solo autor

No GitHub governance (no PR templates, no Dependabot), no agent files, but **keeps** the
research folders. Good for a paper repository that you will publish with the article.

```text
@proyecto-abel minimal repo for my paper on burned area in El Tuparro (Sentinel-2 dNBR).
Keep notebooks/, data/ and figures/. No GitHub templates.
```

```bash
python3 $S/new_project.py --name "Tuparro dNBR" --path ./tuparro-dnbr --minimal --sciml
```

```text
Modo : paquete (src-layout) · types=sí · github=no · agents=no · archify=no · sciml=sí · git=sí
```

> `--minimal` alone removes the research folders; add `--sciml` to keep them.
> `--minimal` solo quita las carpetas de investigación; añade `--sciml` para conservarlas.

---

## 3 · Course workshop for students / Taller de curso para estudiantes

A simple app (`main.py`, no package), no SciML layer, no GitHub governance. Students can
run it with `uv run python main.py`.

```text
@proyecto-abel crea un proyecto simple para mis estudiantes de Modelación Matemática:
"Taller 1 Crecimiento Logístico", tipo app, sin notebooks ni plantillas de GitHub.
```

```bash
python3 $S/new_project.py --name "Taller 1 Crecimiento Logistico" --path ./taller-1 --app --no-sciml --no-github --description "Taller de modelación: crecimiento logístico."
```

```text
taller-1/
├── main.py
├── tests/test_main.py
├── docs/README.md
├── AGENTS.md · CLAUDE.md · CONSTITUTION.md · README.md · CONTRIBUTING.md
└── Makefile · pyproject.toml · .pre-commit-config.yaml · LICENSE · …
```

**A student (not Abel) using the skill / Un estudiante que usa el skill:**

```text
@proyecto-abel no soy Abel. Me llamo "Laura Gómez" (laura@example.com),
mi repo es git@github.com:laurag/taller-1.git. Crea el taller 1 en modo app.
```

```bash
python3 $S/new_project.py --name "Taller 1" --path ./taller-1-laura --app --no-sciml --author "Laura Gómez" --email laura@example.com --owner laurag
```

---

## 4 · Existing repository: audit → complete → align / Repositorio existente

The safe path for a repo that already has history, a README or a `pyproject.toml`
(for example, the UHI Bogotá GNN project).

**Step 1 — audit, writes nothing / auditar sin escribir nada:**

```text
@proyecto-abel audita este repositorio y muéstrame el informe FALTA / DIFIERE / OK
sin modificar nada.
```

```bash
python3 $S/new_project.py --path . --audit
```

```text
▶ Auditoría del estándar: ~/Repos/uhi-bogota
  ✖ FALTA   .editorconfig
  ✖ FALTA   CONSTITUTION.md
  ✖ FALTA   Makefile
  ...
  ≠ DIFIERE README.md
  ≠ DIFIERE pyproject.toml
  ✓ OK: 0 · ≠ DIFIERE: 2 · ✖ FALTA: 15
```

**Step 2 — complete only what is missing / completar solo lo que falta:**

```text
@proyecto-abel completa lo que falta sin borrar nada. Respeta mi README y mi pyproject.
Nombre "UHI Bogota", descripción "Isla de calor urbana en Bogotá con GNNs".
```

```bash
python3 $S/new_project.py --path . --name "UHI Bogota" --description "Isla de calor urbana en Bogotá con GNNs." --app --no-github
```

```text
  · omitido (ya existe): README.md
  · omitido (ya existe): pyproject.toml
  creados: 18 · sobrescritos: 0 · omitidos: 2

── pyproject.toml existente (no se modificó) ─────────────
  Alinea las dependencias con el estándar / Align it with the standard:
    uv add --dev pre-commit pytest ruff
    uv add --group notebooks ipykernel nbstripout
    uv add -r requirements.txt && rm requirements.txt
  Añade al final de pyproject.toml / Append to pyproject.toml:
    [tool.ruff] ...
    [tool.pytest.ini_options] ...
```

**Step 3 — run what it printed, then verify / ejecutar lo indicado y verificar:**

```bash
uv add --dev pre-commit pytest ruff
uv add --group notebooks ipykernel nbstripout
uv add -r requirements.txt && rm requirements.txt
# pega los bloques [tool.*] que imprimió el scaffolder al final de pyproject.toml
make check
python3 $S/new_project.py --path . --audit     # → only README.md and pyproject.toml DIFIERE
```

> `DIFIERE` on your own README or pyproject is expected: it is your content. Merge by hand
> what you want from the template; never use `--force` on them.

---

## 5 · Preview before writing / Previsualizar sin escribir

```bash
python3 $S/new_project.py --name "SCIS Model" --path ./scis-model --dry-run
```

```text
  (dry-run: no se escribirá nada)
[git] (dry-run) se inicializaría el repositorio en la rama main.
  creados: 30 · sobrescritos: 0 · omitidos: 0
```

---

## 6 · Working in Google Colab / Trabajar en Colab

If the package must be installed inside Colab, match Colab's Python version when you
create the project (check it with `!python --version`):

```bash
python3 $S/new_project.py --name "Cocha Shallow Water" --path ./cocha-swe --python-version 3.12
```

First cell of each notebook / Primera celda de cada notebook:

```python
# Install only this package; keep Colab's own CUDA builds of torch/jax
!git clone https://github.com/abelalv/cocha-swe.git
%cd cocha-swe
!pip install -q -e . --no-deps
```

```text
@proyecto-abel prepara notebooks/01_swe-baseline.ipynb para Colab con la celda de
instalación, semillas fijas y verificación de GPU.
```

Details: [`colab.md`](colab.md).

---

## 7 · Recording a decision / Registrar una decisión en la constitución

```text
@proyecto-abel actualiza CONSTITUTION.md: cambiamos de diferencias finitas a una PINN
para estimar D(x) porque el coeficiente es desconocido. Regístralo en el historial y
actualiza el stack. No borres lo anterior.
```

Expected change / Cambio esperado (§ historial):

```markdown
| 2026-10-06 | Pasar de diferencias finitas a PINN para el problema inverso | D(x) es desconocido y se estima con los datos |
```

The same commit must include the code change (rule 1). / El mismo commit incluye el cambio
de código (regla 1).

---

## 8 · Automatic Git identity / Identidad Git automática

Preview first; nothing is written with `--print` / Primero previsualiza:

```bash
python3 $S/setup_git_identity.py --name "Abel Alvarez Bustos" --email abel@example.com --key ~/.ssh/id_ed25519 --dir ~/Repos --platform linux --print
```

```text
── ~/.gitconfig-personal ─────────
[user]
	name = Abel Alvarez Bustos
	email = abel@example.com
[core]
	sshCommand = ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes

── añadir a ~/.gitconfig ─────────
[includeIf "gitdir:~/Repos/"]
	path = ~/.gitconfig-personal
```

Remove `--print` to apply it (it backs up `~/.gitconfig` first). / Quita `--print` para
aplicarlo (hace copia de seguridad de `~/.gitconfig`).

```text
@proyecto-abel configura mi identidad Git automática para la carpeta ~/Repos
con mi correo de GitHub y la llave ~/.ssh/id_ed25519. Estoy en Ubuntu.
```

---

## 9 · Architecture diagram / Diagrama de arquitectura (Archify)

```bash
python3 $S/new_project.py --name "VFR LLM" --path ./vfr-llm --archify
```

```text
@proyecto-abel instala Archify y genera docs/arquitectura.html a partir de este
repositorio: 8–12 componentes, un camino principal y las dependencias externas.
Enlázalo en la sección de arquitectura del README.
```

Details: [`archify.md`](archify.md).

---

## 10 · Daily loop / Ciclo diario

```bash
make help                 # list targets
make notebooks            # (once) Jupyter kernel for this project
# explore in notebooks/ → move working code to src/ → write a test
make check                # lint + format + types + tests
git add -A
git commit -m "feat: add PINN loss with Neumann boundary terms"
git push                  # CI runs the same checks
```

Diagram of this loop: [`workflow.md`](workflow.md).

---

## Writing good prompts / Cómo pedirle bien al agente

Include these pieces / Incluye estas piezas:

```text
@proyecto-abel
Soy / I am:       Abel  |  otro usuario → nombre, correo, usuario de GitHub
Estado / State:   nuevo / new  |  existente / existing
Tipo / Type:      paquete de investigación | artículo (--minimal --sciml) | curso (--app)
Objetivo / Goal:  crear | auditar | completar sin borrar | añadir X | registrar decisión
```

| Avoid / Evita | Instead / En su lugar |
|---------------|-----------------------|
| "Rehaz mi repo con el estándar" (may tempt `--force`) | "Audita y completa sin borrar nada" |
| "Instala torch con pip" | "Añade torch con uv" (Colab is the only pip exception) |
| Editing figures by hand | "Regenera figures/fig3 con el script" |
