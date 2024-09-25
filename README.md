# Volleyball Meeting Scheduler

A command-line tool for scheduling volleyball-related meetings. This project is built with Python and uses Poetry for dependency management.

## Table of Contents

- [1 User](#1-user)
  - [1.1 Requirements](#11-requirements)
  - [1.2 Features](#12-features)
  - [1.3 Installation](#13-installation)
- [2 Developer](#2-developer)
  - [2.1 Requirements](#21-requirements)
  - [2.2 Installation](#22-installation)
  - [2.3 Testing](#23-testing)
  - [2.4 Contribution Guidelines](#24-contribution-guidelines)
- [3 License](#3-license)

---

## 1 User

### 1.1 Requirements

- Python 3.8+

### 1.2 Features

- Schedule and manage meetings.
- Simple CLI interface for creating, reading, updating, and deleting meetings.

### 1.3 Installation

```bash
pip install volleymeet
```

## 2 Developer

### 2.1 Requirements

- Python 3.8+
- Poetry

### 2.2 Installation

To get started with development, follow the instructions below to set up the project on your local machine.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Jython1415/cli-monolithic-architecture.git volleymeet
   cd volleymeet
   ```

1. **Install Poetry** (if you don’t already have it):  

1. **Create a virtual environment and install dependencies**: Poetry will automatically create a virtual environment for the project.

    ```bash
    poetry install
    poetry shell
    ```

1. **Create the database**:

    ```bash
    poetry run python database/db_setup.py
    ```

1. **Run the project**:

    ```bash
    poetry run volleyball-meetings
    ```

### 2.3 Testing

We use `pytest` for testing the project. To run the test suite:

- **Run all tests**:  

    ```bash
    poetry run pytest
    ````

- **View coverage**: You can also generate a test coverage report:  

    ```bash
    poetry run pytest --cov=src
    ```

### 2.4 Contribution Guidelines

Always either use a branch or a fork for changes.

### 2.5 Build and Publish

To release a new version of the project, follow these steps:

1. **Update the Version**

    Bump the version in pyproject.toml using Poetry's versioning command.

    ```bash
    poetry version <major|minor|patch>
    ```

1. **Update the Changelog**

    Document new features, fixes, or changes in CHANGELOG.md.

1. **Commit Changes**
  
    Commit  on bump and changelog update.

1. **Tag the Release**

    ```bash
    git tag v<x.y.z>
    git push origin main --tags
    ```

1. **Build the Package**

    ```bash
    poetry build
    ```

1. **Publish to PyPI**

    ```bash
    poetry publish --build
    ```

## 3 License

This project is licensed under the MIT License. See the LICENSE file for details.
