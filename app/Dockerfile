# Use an official Python image as the base image
FROM python:3.12-alpine as base

# Set the working directory within the container
WORKDIR /app

# Copy necessary files
COPY requirements.txt .

# Install dependencies and clean up
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Copy the rest of the source code into the container
COPY src /app/src
COPY tests /app/tests

# Define environment variables
ENV APP_PORT=${APP_PORT}
ENV APP_HOST=${APP_HOST}
ENV APP_MODULE=${APP_MODULE}
ENV PYTHONPATH="/app/src"

# Expose the port the FastAPI app will run on
EXPOSE ${APP_PORT}

# Use a single CMD instruction
CMD ["sh", "-c", "uvicorn ${APP_MODULE} --host ${APP_HOST} --port ${APP_PORT}"]
