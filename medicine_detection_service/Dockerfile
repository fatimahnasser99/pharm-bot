FROM python:3.9-slim

ENV APP_HOST="0.0.0.0"
ENV APP_PORT=5001

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
