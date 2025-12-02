#!/bin/bash
# Healthcheck script for debugging

echo "=== Healthcheck Debug ==="
echo "Time: $(date)"
echo "Working directory: $(pwd)"
echo ""

echo "=== Files in /app ==="
ls -lah /app/ | head -20
echo ""

echo "=== Checking if Streamlit is running ==="
ps aux | grep streamlit
echo ""

echo "=== Checking port 8501 ==="
netstat -tlnp 2>/dev/null | grep 8501 || ss -tlnp 2>/dev/null | grep 8501 || echo "Port check tools not available"
echo ""

echo "=== Testing localhost:8501 ==="
curl -v http://localhost:8501/_stcore/health 2>&1 || echo "Health endpoint failed"
echo ""

echo "=== Testing localhost:8501 root ==="
curl -v http://localhost:8501/ 2>&1 | head -20 || echo "Root endpoint failed"
echo ""

echo "=== End healthcheck debug ==="
