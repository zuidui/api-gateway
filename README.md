# API Gateway  

![GitHub release (latest by date)](https://img.shields.io/github/v/release/zuidui/api-gateway)
![Docker Hub Image Version (latest by date)](https://img.shields.io/docker/v/zuidui/api-gateway?label=docker%20hub)
![GitHub](https://img.shields.io/github/license/zuidui/api-gateway)
![GitHub contributors](https://img.shields.io/github/contributors/zuidui/api-gateway)

## Overview

This project is an API Gateway microservice built with FastAPI. It serves as a central point for routing API requests to various backend services. This microservice also acts as a bridge between the frontend and backend services, providing a unified interface for the client applications. Convert REST API to GraphQL API and combine multiple services into a single endpoint.

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

- `app/`
  - `docker-compose.yml`: Defines the services, their configurations, and networking.
  - `Dockerfile`: Defines the Docker image for the API Gateway service.
  - `requirements.txt`: Lists the Python dependencies for the project.
  - `src/`: Contains the source code for the application.
    - `events/`: Event handling modules.
    - `exceptions/`: Custom exception classes.
    - `main.py`: Entry point for the FastAPI application.
    - `models/`: Database models.
    - `resolver/`: GraphQL resolvers.
    - `routes/`: FastAPI route definitions.
    - `service/`: Service layer for business logic.
    - `utils/`: Utility functions and configurations.
  - `tests/`: Contains the test files.
    - `acceptance/`: Acceptance tests.
    - `integration/`: Integration tests.
    - `unit/`: Unit tests.
- `chart/`
  - Helm charts for Kubernetes deployment.
- `CRD/`
  - Custom Resource Definitions for Kubernetes.
- `scripts/`: Contains helper scripts.
- `.env`: Environment variables used by Docker Compose and the application.
- `Makefile`: Provides a set of commands to automate common tasks.
- `LICENSE`: License file for the project.
- `README.md`: This file.

## Project Commands

The project uses [Makefiles](https://www.gnu.org/software/make/manual/html_node/Introduction.html) to run the most common tasks:

- `help`: Shows this help.
- `todo`: Shows the TODOs in the code.
- `show-env`: Shows the environment variables.
- `set-up`: Prepares the environment for development.
- `clean`: Cleans the app.
- `build`: Builds the app.
- `run`: Runs the app.
- `test`: Run all the tests.
- `test-unit`: Run the unit tests.
- `test-integration`: Run the integration tests.
- `test-acceptance`: Run the acceptance tests.
- `pre-commit`: Runs the pre-commit checks.
- `reformat`: Formats the code.
- `check-typing`: Runs a static analyzer over the code to find issues.
- `check-style`: Checks the code style.
- `publish-image-pre`: Publishes the image to the pre-production registry.
- `publish-image-pro`: Publishes the image to the production registry.

## Services

**API Gateway**: `http://${IMAGE_NAME}:${APP_PORT}`

**Sanity Check**: `http://${IMAGE_NAME}:${APP_PORT}/health`

**Schema Definition**: `http://${IMAGE_NAME}:${APP_PORT}/schema`

**API Documentation**: `http://${IMAGE_NAME}:${APP_PORT}/{DOC_URL}`

**GraphQL Playground**: `http://${IMAGE_NAME}:${APP_PORT}/api/{API_PREFIX}/graphql`

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

## Contact

For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/zuidui/api-gateway) or contact any of the maintainers.
