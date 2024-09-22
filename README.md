# Volleyball Meeting Scheduler

A command-line tool for scheduling volleyball-related meetings. This project is built with Python and uses Poetry for dependency management.

## Table of Contents

1. [Features](#features)
1. [Requirements](#requirements)
1. [Installation (User)](#installation-user)
1. [Installation (Developer)](#installation-developer)
1. [Testing](#testing)
1. [Contributing](#contributing)
1. [License](#license)

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

## **Installation (User)**

---

## **Installation (Developer)**

To get started with development, follow the instructions below to set up the project on your local machine.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Jython1415/cli-monolithic-architecture.git
   cd volleyball-meetings
   ```

1. **Install Poetry** (if you don’t already have it):  

1. **Create a virtual environment and install dependencies**: Poetry will automatically create a virtual environment for the project.

    ```bash
    poetry install
    poetry shell
    ```

1. **Run the project**:

    ```bash
    poetry run volleyball-meetings
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
