# Use a slim Python image to keep the size small
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

COPY requirements.txt .

# Install dependencies directly (or use a requirements.txt if you have one)
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script into the container
COPY neriping.py .

# Create a default directory for config and data
# We'll point your script here using an environment variable
RUN mkdir /config
ENV NERIPING_CONFIG_DIR=/config

# Run the script
CMD ["python", "-u", "neriping.py"]