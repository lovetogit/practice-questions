# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy your app into the container
COPY app/ /app/

# Install dependencies
RUN pip install flask

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

