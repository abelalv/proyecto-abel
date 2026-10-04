# Google Colab y GPU — convivencia con `uv` / Colab, GPUs and `uv`

> **EN** — The "only `uv`" rule applies to environments *we own* (your laptop, a lab
> server). Colab's runtime is not ours: it ships its own Python, CUDA, PyTorch and JAX.
> Replacing them with `uv sync` usually breaks GPU support or wastes several minutes per
> session. So in Colab we install **only our package, without dependencies**, on top of
> what Colab already provides.
>
> **ES** — La regla "solo `uv`" aplica a entornos *propios*. El runtime de Colab no es
> nuestro: trae su Python, CUDA, PyTorch y JAX. En Colab se instala **solo el paquete del
> proyecto, sin dependencias**.

## 1 · Celda de arranque estándar / Standard setup cell

```python
# Clona el repo y lo instala en modo editable sin tocar torch/jax de Colab
import os, subprocess
REPO = "https://github.com/<usuario>/<repo>.git"   # o privado: usa un token en Secrets
if not os.path.exists("<repo>"):
    subprocess.run(["git", "clone", "-q", REPO], check=True)
%cd <repo>
!pip install -q -e . --no-deps
```

Si el paquete necesita librerías que Colab no trae (p. ej. `deepxde`, `torch-geometric`),
instálalas explícitamente en la celda (`!pip install -q deepxde`) y **regístralas también**
en `pyproject.toml` con `uv add` en tu máquina, para que el lockfile siga siendo la verdad.

## 2 · Versión de Python / Python version

El estándar fija `requires-python >= 3.13`. Si la versión de Python de Colab es menor
(compruébalo con `!python --version`), `pip install -e .` fallará. Opciones:

1. Crear el proyecto con `--python-version 3.12` (o la que use Colab) — recomendado para
   proyectos que viven en Colab.
2. Mantener 3.13 localmente y no instalar el paquete en Colab (solo `sys.path.append("src")`).

## 3 · PyTorch / JAX con CUDA en local (uv)

En tu máquina (Ubuntu + GPU NVIDIA), declara el índice de PyTorch en `pyproject.toml` para
que `uv` resuelva la build CUDA correcta. Consulta la guía oficial de uv
("Using uv with PyTorch") y fija la variante CUDA que corresponda a tu driver. Para JAX:
`uv add "jax[cuda12]"` (ajusta según tu versión de CUDA).

## 4 · Reproducibilidad mínima en notebooks / Minimal reproducibility

```python
# Fija semillas y registra el entorno al inicio de cada notebook
import random, numpy as np, torch
SEED = 42
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
print(torch.__version__, torch.cuda.is_available())
```

Guarda pesos y resultados pesados en Google Drive o en `results/` (ignorado por Git), nunca
dentro del repositorio.
