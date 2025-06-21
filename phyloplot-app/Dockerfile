# Use Ubuntu as the base image
FROM ubuntu:24.04

# Set the working directory
WORKDIR /app

# Set environment variable to disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and R
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    build-essential 

RUN apt-get update && apt-get install -y \
    software-properties-common && \
    wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | gpg --dearmor > /usr/share/keyrings/cran.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cran.gpg] https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" > /etc/apt/sources.list.d/cran.list && \
    apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update && \
    apt-get install -y libfontconfig1-dev \
    libharfbuzz-dev libfribidi-dev
# Install R packages
RUN Rscript -e "install.packages('BiocManager')"
RUN Rscript -e "install.packages('systemfonts')"
RUN Rscript -e "BiocManager::install(version = '3.21', ask = FALSE)"
RUN Rscript -e "BiocManager::install(c('ggplot2', 'dplyr', 'tidyr', 'ape', 'ggtree'))"
RUN Rscript -e "BiocManager::install(c('ggtreeExtra', 'svglite', 'Polychrome'))"

# Install Python dependencies
RUN apt-get update && \
    apt-get install -y python3.12 python3-pip python3.12-venv


RUN python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install streamlit pandas matplotlib seaborn

# Copy application files
COPY app.py ggtree_trial.R requirements.txt ./

# Setup cron job to clean /app/tmp every day
RUN echo "0 0 * * * root find /app/tmp -type f -mtime +1 -delete" > /etc/cron.d/clean-tmp && \
    chmod 0644 /etc/cron.d/clean-tmp && \
    touch /var/log/cron.log

# Create a directory for temporary files
RUN mkdir -p /app/tmp

# Expose the port for Streamlit
EXPOSE 5000

# Run the Streamlit app
CMD ["venv/bin/python3", "-m", "streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0"]
