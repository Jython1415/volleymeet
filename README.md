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
- MySQL (local installation)

### 1.2 Features

- Schedule and manage meetings.
- Simple CLI interface for creating, reading, updating, and deleting meetings.
- Integrates with a MySQL database for persistent storage.

### 1.3 Installation

*User installation instructions go here.*

## 2 Developer

### 2.1 Requirements

- Python 3.8+
- Poetry
- MySQL (local installation)

### 2.2 Installation

To get started with development, follow the instructions below to set up the project on your local machine.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Jython1415/cli-monolithic-architecture.git volleyball-meetings
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

## 3 License

This project is licensed under the MIT License. See the LICENSE file for details.
