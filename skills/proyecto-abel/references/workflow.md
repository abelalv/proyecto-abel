# Workflow / Flujo de trabajo

Two diagrams: **(1)** how the skill sets up a project, **(2)** the daily research loop once
the project exists. Each node is bilingual: **English** / *Español*.

Dos diagramas: **(1)** cómo el skill configura un proyecto y **(2)** el ciclo diario de
investigación una vez el proyecto existe.

## 1 · Setting up a project / Configurar un proyecto

```mermaid
flowchart TD
    A(["Start: invoke @proyecto-abel<br/><i>Inicio: invocar @proyecto-abel</i>"]) --> B{"New or existing project?<br/><i>¿Proyecto nuevo o existente?</i>"}

    B -- "New / Nuevo" --> C{"Who will use it?<br/><i>¿Para quién es?</i>"}
    C -- "Research package<br/><i>Paquete de investigación</i>" --> C1["new_project.py --name ... <br/>(default: SciML + GitHub + agents)"]
    C -- "Single-author paper<br/><i>Artículo de un autor</i>" --> C2["new_project.py --minimal<br/>(+ --sciml if notebooks)"]
    C -- "Course / students<br/><i>Curso / estudiantes</i>" --> C3["new_project.py --app<br/>(simple app, no package)"]

    B -- "Existing / Existente" --> D["--audit<br/><i>Auditar sin escribir nada</i>"]
    D --> E{"Report<br/><i>Informe</i>"}
    E -- "FALTA / MISSING" --> F["Run scaffolder without --force<br/><i>Crea solo lo que falta</i>"]
    E -- "DIFIERE / DIFFERS" --> G["Merge by hand, keep user content<br/><i>Fusionar a mano, respetar lo propio</i>"]
    E -- "OK" --> H

    C1 --> H["Fill CONSTITUTION.md<br/><i>Completar la constitución</i>:<br/>purpose · scope · stack · decisions"]
    C2 --> H
    C3 --> H
    F --> H
    G --> H

    H --> I["uv sync && make dev<br/><i>Entorno + hooks pre-commit</i>"]
    I --> J{"make check green?<br/><i>¿make check en verde?</i>"}
    J -- "No" --> K["Fix lint / tests<br/><i>Corregir lint / pruebas</i>"] --> J
    J -- "Yes / Sí" --> L["gh repo create / git push<br/><i>Publicar en GitHub</i>"]
    L --> M{"Optional extras<br/><i>Extras opcionales</i>"}
    M -- "Diagram / Diagrama" --> N["Archify → docs/arquitectura.html"]
    M -- "Git identity / Identidad" --> O["setup_git_identity.py<br/>(includeIf, only if asked)"]
    M -- "Colab" --> P["references/colab.md<br/><i>pip install -e . --no-deps</i>"]
    N --> Z(["Ready / Listo"])
    O --> Z
    P --> Z
    M -- "None / Ninguno" --> Z
```

## 2 · Daily research loop / Ciclo diario de investigación

```mermaid
flowchart LR
    A["Explore in notebooks/<br/><i>Explorar en notebooks/</i>"] --> B{"Does it work?<br/><i>¿Funciona?</i>"}
    B -- "No" --> A
    B -- "Yes / Sí" --> C["Move code to src/<br/><i>Mover el código a src/</i>"]
    C --> D["Write a test (AAA)<br/><i>Escribir una prueba</i>"]
    D --> E["make check<br/><i>lint + format + types + tests</i>"]
    E -- "red / rojo" --> C
    E -- "green / verde" --> F{"Architecture, stack or<br/>hyperparameter change?<br/><i>¿Cambio de arquitectura,<br/>stack o hiperparámetros?</i>"}
    F -- "Yes / Sí" --> G["Update CONSTITUTION.md<br/>(same commit)<br/><i>Actualizar la constitución</i>"]
    F -- "No" --> H
    G --> H["git commit -m 'feat: ...'<br/>nbstripout cleans notebooks<br/><i>nbstripout limpia notebooks</i>"]
    H --> I["git push → CI"]
    I --> J{"Result for the paper?<br/><i>¿Resultado para el artículo?</i>"}
    J -- "Yes / Sí" --> K["Script → figures/figN.pdf<br/><i>Figura generada por código</i>"]
    J -- "No" --> A
    K --> A
```

> GitHub renderiza Mermaid directamente. Copias en SVG para diapositivas y una página
> interactiva EN/ES están en la carpeta `docs/` del repositorio del skill.
> Para re-exportar tras editar: `npx -y @mermaid-js/mermaid-cli -i workflow.md -o workflow.svg`.
