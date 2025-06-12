FROM rocker/r-base:4.3.1

WORKDIR /app

COPY app.py ggtree_trial.R requirements.txt ./

RUN Rscript -e "install.packages(c('ggtree', 'ggtreeExtra', 'svglite'))"

RUN apt-get update && apt-get install -y \
    pip \
    python3-pip \
    python3.13-venv \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*


RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir pandas==2.3.0 flask==3.1.1 gunicorn==23.0.0 streamlit==1.45.1


EXPOSE 5000

CMD ["/app/venv/bin/streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]

