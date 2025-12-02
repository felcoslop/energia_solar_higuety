FROM python:3.11-slim

# Accept build args from EasyPanel (even if not used for Streamlit)
ARG FLASK_ENV
ARG SECRET_KEY
ARG DATABASE_URL
ARG GIT_SHA

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create .streamlit directory for config
RUN mkdir -p .streamlit

# Expose Streamlit port
EXPOSE 8501

# Set environment variables for better logging
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check - more lenient for startup
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=5 \
    CMD curl -f http://localhost:8501/_stcore/health || curl -f http://localhost:8501/ || exit 1

# Run Streamlit with explicit logging
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --logger.level=info
