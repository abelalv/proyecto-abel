# notebooks/

**EN** — Exploration and prototyping. Notebooks are drafts: once a function works,
move it to `src/{{PACKAGE_NAME}}/` and import it from here. Outputs are stripped
automatically by `nbstripout` before each commit, so the repo stays light and diffs stay
readable.

**ES** — Exploración y prototipos. Los notebooks son borradores: cuando una función
funciona, se mueve a `src/{{PACKAGE_NAME}}/` y se importa desde aquí. `nbstripout`
elimina las salidas antes de cada commit para mantener el repo liviano y los diffs legibles.

## Convención de nombres / Naming

`NN_tema-corto.ipynb` → `01_eda-datos.ipynb`, `02_pinn-baseline.ipynb`, `03_figuras-paper.ipynb`

## Local (uv)

```bash
make notebooks          # uv sync --group notebooks + registra el kernel
```

## Google Colab

Colab trae su propio Python y PyTorch/JAX con CUDA; **no** reemplaces ese entorno con
`uv sync`. Instala solo tu paquete encima / Install only your package on top:

```python
# Celda 1 — clonar e instalar el paquete del proyecto (sin tocar torch/jax de Colab)
!git clone {{REPO_URL}}.git
%cd {{PROJECT_SLUG}}
!pip install -q -e . --no-deps
```

> Excepción documentada a la regla "solo uv": dentro de Colab se usa `pip` porque el
> entorno no es nuestro. Ver `references/colab.md` del skill.
