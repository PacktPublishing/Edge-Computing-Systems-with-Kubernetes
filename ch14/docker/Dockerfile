FROM python:3.9-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# System deps (add toolchain & BLAS so SciPy can build if wheels aren't available on ARM)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential gfortran pkg-config \
        libopenblas-dev liblapack-dev \
        libatlas-base-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Prefer wheels on ARM; fall back to building (toolchain above covers it)
ARG TARGETPLATFORM
RUN case "$TARGETPLATFORM" in \
      linux/arm64*|linux/arm/v7) \
        PIP_EXTRA_INDEX_URL=https://www.piwheels.org/simple \
        PIP_ONLY_BINARY=numpy,scipy,scikit-learn \
        pip install --no-cache-dir -r requirements.txt \
      ;; \
      *) \
        pip install --no-cache-dir -r requirements.txt \
      ;; \
    esac

COPY . .

# Build the model at image build time
RUN python3 create_model.py

# Run as non-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -fsS http://127.0.0.1:3000/_health || exit 1

# Use gunicorn for production serving
CMD ["gunicorn", "-b", "0.0.0.0:3000", "index:app", "--workers", "2"]
