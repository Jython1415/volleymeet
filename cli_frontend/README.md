# CLI Frontend

## Key Files

- `Dockerfile`: The Dockerfile for the CLI frontend. Used to specify how the Docker image should be built.
- `main.py`: The main Python script that is run when the container is started.
- `services.py`: Contains the logic for the services that the CLI frontend provides. Connects to the backend services to get the data.
- `requirements.txt`: Contains the Python packages that are required to run the CLI frontend.
- `setup.cfg`: Contains the configuration for the Python project. Used to specify the package name and version.
- `pyproject.toml`: Contains the configuration for the Python project. Used to specify the build system.

## How to Run

To run the CLI frontend, just build and run the entire project. See the README in the root directory for more information.

## Install Dependencies

To install the dependencies locally, run the following commands:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Updating Dependencies in `requirements.txt`

To update the dependencies in `requirements.txt`, run the following commands:

```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install .
pip freeze > requirements.txt
```

Next, we remove the package itself from the `requirements.txt` file. This is because the package is already installed in the virtual environment, and we don't want to install it again when we run `pip install -r requirements.txt`.

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' '/cli_frontend/d' requirements.txt
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sed -i '/cli_frontend/d' requirements.txt
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    # Windows (Git Bash/Cygwin)
    sed -i '/cli_frontend/d' requirements.txt
else
    echo "Unsupported OS"
fi
```
