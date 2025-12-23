# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the configuration file
COPY config.yaml .

# ✅ ADD THIS LINE (REQUIRED)
COPY error_alert_callback.py .

# Expose the port that Hugging Face expects (7860)
EXPOSE 7860

# Start the LiteLLM Proxy Server
# --config: points to your yaml file
# --port: runs on port 7860
# --detailed_debug: helps you see errors in the logs if something goes wrong
CMD ["litellm", "--config", "config.yaml", "--port", "7860", "--detailed_debug"]