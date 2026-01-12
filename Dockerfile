FROM python:3.10-slim

LABEL maintainer="Daouda Abdoul Anzize <nexusstudio100@gmail.com>"
LABEL description="Nexus-Stellar: Emergent computation engine"
LABEL version="0.1.0"

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --no-cache-dir numpy

WORKDIR /nexus
COPY nexus_stellar.py .
COPY examples/ ./examples/

EXPOSE 8000

ENTRYPOINT ["python", "nexus_stellar.py"]