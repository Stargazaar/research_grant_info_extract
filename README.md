# python_project_template

A modern Python project template managed with [uv](https://docs.astral.sh/uv/).

## Stack

- **uv** — virtualenv + dependency management
- **pyproject.toml** — project metadata and dependencies
- **.python-version** — pins Python to `3.14`
- **src/ layout** — package lives in `src/project_name/`
- **.env** — local secrets (gitignored), templated by `.env.example`

## Getting Started

1. Install uv (if not already): https://docs.astral.sh/uv/getting-started/installation/
2. Ensure Python 3.14 is available:

   ```bash
   uv python install 3.14
   ```

3. Sync dependencies (creates `.venv` automatically):

   ```bash
   uv sync
   ```

4. Configure secrets:

   ```bash
   cp .env.example .env   # then edit .env
   ```

5. Run the app:

   ```bash
   uv run python -m project_name.main
   ```

## Testing

```bash
uv run pytest
```

## Using as a Template

Rename the `src/project_name/` package and update the `name` / `[project.scripts]`
entries in `pyproject.toml` to match your new project.