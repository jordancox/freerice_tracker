FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start_production.sh

# Create data directory (will be mounted as volume)
RUN mkdir -p data

# Expose port
EXPOSE 8080

# Run startup script
CMD ["./start_production.sh"]
