# Volleyball Meeting Scheduler

This project is a web application that allows a user to manage meetings from a web interface. The backend and persistence layers are hosted on separate servers, and the frontend is intended to be loaded on a separate device.

## Table of Contents

- [1 User Instructions](#1-user-instructions)
- [2 Developer Instructions](#2-developer-instructions)
- [3 License](#3-license)

---

## 1 User Instructions

## 2 Developer Instructions

### 2.1 Frontend

#### 2.1.1 How to run Frontend

These instructions assume the working directory is set to the `frontend` directory.

```bash
npm install
npm install react-big-calendar moment
npm run dev
```

### 2.2 Backend + Persistence

### 2.2.1 Docker Usage

Build the Docker image (only needed if changes were made to Dockerfile):

```bash
docker-compose build
```

Start the services:

```bash
docker-compose up
```

Stop the services (when done testing):

```bash
docker-compose down
```

### 2.2 Environment Variables

Copy the `.env` file from Google Drive to the root of the project directory. This file contains the environment variables needed to run the backend and persistence layers.

## 3 License

This project is licensed under the MIT License. See the LICENSE file for details.
