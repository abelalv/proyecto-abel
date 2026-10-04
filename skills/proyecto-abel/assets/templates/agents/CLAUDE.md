# CLAUDE.md — {{PROJECT_NAME}}

@AGENTS.md

## Notas para Claude Code / Claude Code notes

- Lee `CONSTITUTION.md` antes de cambiar arquitectura, stack o flujo; actualízala en el
  mismo commit. / Read `CONSTITUTION.md` first and update it in the same commit.
- Dependencias **solo** con `uv add` / `uv remove`. Nunca `pip install` en el entorno local.
- Antes de terminar una tarea: `make check` debe pasar en verde.
- Código reutilizable va en `src/`; los notebooks solo importan. / Reusable code lives in
  `src/`; notebooks only import it.
- En código numérico: fija semillas, documenta unidades y dimensiones en docstrings, y no
  cambies tolerancias ni hiperparámetros sin registrarlo en la constitución.
- No borres ni sobrescribas datos en `data/` ni resultados en `figures/` sin pedir permiso.
