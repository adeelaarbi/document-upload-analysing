# Project Name

A web application with a React frontend, backend service, and Nginx reverse proxy.

## Prerequisites

Before running this project, make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

The project consists of three main services:
- Frontend (React application)
- Backend service
- Nginx reverse proxy

## Getting Started

### 1. Clone the Repository
- bash git clone <repository-url> cd <project-directory>

### 2. Running the Application

- To start all services, run:
- bash docker-compose up

To run in detached mode (background):
- bash docker-compose up -d


### 3. Accessing the Application

Once all containers are running:
- The application will be available at: `http://localhost`
- Frontend is served through Nginx on port 80
- Backend service is exposed internally on port 8888

### 4. Stopping the Application

To stop the running containers:
- bash docker-compose down




