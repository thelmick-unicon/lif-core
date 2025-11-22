# lif-main
Collection of LIF components

## Toolchain
* python
* uv
* polylith
* ruff
* ty
* pytest
* pre-commit
* commitlint
* cspell
* mkdocs

## Initial Local Development Setup
1. Clone Repository
    * In a terminal, run:
        ```
        git clone git@github.com:LIF-Initiative/lif-main.git
        ```
2. Install uv
    *  Instructions: https://docs.astral.sh/uv/getting-started/installation/
    *  Verify:
        *  In a terminal, run:
            ```
            uv --version
            ```
        *  You should see a something like this:
            ```
            uv 0.7.11
            ```
3.  Create Virtual Environment / Install Dependencies
    *  In a terminal, run:
        ```
        uv sync
        ```
    *  Output will indicate that virtual environment was created at .venv and dependencies installed will be listed
4. Verify Python is Installed
    *  In a terminal, run: 
        ```
        uv run python --version
        ```
    *  You should see: 
        ```
        Python 3.13.4
        ```
4. Verify ruff is Installed
    * In a terminal, run:
        ```
        uv run ruff --version
        ```
    * You should see something like:
        ```
        ruff 0.11.13
        ```
5. Verify ty is Installed
    * In a terminal, run:
        ```
        uv run ty --version
        ```
    * You should see something like:
        ```
        ty 0.0.1-alpha.8
        ```
6. Verify pytest is Installed
    * In a terminal, run:
        ```
        uv run pytest --version
        ```
    * You should see something like:
        ```
        pytest 8.4.0
        ```
7. Verify pre-commit is Installed
    * In a terminal, run:
        ```
        uv run pre-commit --version
        ```
    * You should see something like:
        ```
        pre-commit 4.2.0 (pre-commit-uv=4.1.4, uv=0.7.11)
        ```
8. Verify mkdocs is Installed
    * In a terminal, run:
        ```
        uv run mkdocs --version
        ```
    * You should see something like:
        ```
        mkdocs, version 1.6.1
        ```
9. Install pre-commit Hooks
    * In a terminal, run:
        ```
        uv run pre-commit install
        ```
    * You should see the following output:
        ```
        pre-commit installed at .git/hooks/pre-commit
        ```
    * In a terminal, run:
        ```
        uv run pre-commit install --hook-type commit-msg
        ```
    * You should see the following output:
        ```
        pre-commit installed at .git/hooks/commit-msg
        ```

## Optional Local Development Setup
1. Install jq
    * See: https://jqlang.org/download/
    * This is only needed if you will be using the mongodb-seed Docker container with the sample data

## Common Commands

### Check Code Formatting
```
uv run ruff format
```

### Run Linter
```
uv run ruff check
```

### Run Type Checker
```
uv run ty check
```

### Run All Checks
```
uv run pre-commit run
```

## Using Virtual Environment

Instead of having to prefix each command with `uv run`, you can instead activate the virtual environment.

### Activate
```
source .venv/bin/activate
```

### Deactivate
```
deactivate
```
