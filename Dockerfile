# Use Python Alpine base image
FROM python:3.13.0-alpine3.20
RUN apk update && apk upgrade

# Set working directory
WORKDIR /app

# Copy only the required files
COPY ./app.py ./

# Install only the required packages
# Using pip install with no cache and removing pip cache after
RUN pip install --no-cache-dir fastapi uvicorn && \
    rm -rf /root/.cache

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]