# Volleyball Meeting Scheduler

A command-line tool for scheduling volleyball-related meetings. This project is built with Python and uses Poetry for dependency management.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Running the Project](#running-the-project)
5. [Development Setup](#development-setup)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features

- Schedule and manage meetings.
- Simple CLI interface for creating, reading, updating, and deleting meetings.
- Integrates with a MySQL database for persistent storage.

---

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation)
- MySQL (local installation or remote server)

---

## Installation

To get started with development, follow the instructions below to set up the project on your local machine.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Jython1415/cli-monolithic-architecture.git
   cd volleyball-meetings
   ```

2. **Install Poetry** (if you don’t already have it):  

3. **Create a virtual environment and install dependencies**: Poetry will automatically create a virtual environment for the project.

    ```bash
    poetry install
    ```

---

## **Running the Project**

---

## **Development Setup**

To contribute to the project, follow the installation steps, then, activate the virtual environment.

```bash
poetry shell
```

---

## **Testing**

We use `pytest` for testing the project. To run the test suite:

- **Run all tests**:  

    ```bash
    poetry run pytest
    ````

- **View coverage**: You can also generate a test coverage report:  

    ```bash
    poetry run pytest --cov=src
    ```

---

## **Contributing**

Always either use a branch or a fork for changes.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
