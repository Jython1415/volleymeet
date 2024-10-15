FROM python:3.9-slim

WORKDIR /cli_frontend

# Copy the setup files first to install dependencies
COPY setup.cfg setup.cfg
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .

# Copy the rest of the project files
COPY . .

CMD ["python", "main.py", "-h"]
