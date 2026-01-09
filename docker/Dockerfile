FROM python:3.12-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for libpostal and other Python libraries
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    git \
    libtool \
    automake \
    autoconf \
    pkg-config \
    && apt-get clean

# Clone and install libpostal
RUN git clone https://github.com/openvenues/libpostal.git && \
    cd libpostal && \
    ./bootstrap.sh && \
    ./configure MODEL=senzing && \
    make -j4 && \
    make -j8 && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf libpostal

RUN pip install --upgrade pip

# # Install the pypostal bindings
RUN pip install --no-cache-dir requests beautifulsoup4

# Install pandas and scikit-learn
RUN pip install --no-cache-dir pandas numpy scikit-learn

# Install matplotlib and seaborn
RUN pip install --no-cache-dir matplotlib seaborn

# Install matplotlib and seaborn
RUN pip install --no-cache-dir python-Levenshtein fuzzywuzzy Jinja2 pyyaml

RUN groupadd -r devgroup --gid=1000 && \
    useradd -r -g devgroup --uid=1000 --shell=/bin/bash --create-home developer

# Switch to the custom user
USER developer

# Set the workdir
WORKDIR /home/developer