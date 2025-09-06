FROM python:3.11-slim

WORKDIR /usr/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dbt
RUN pip install dbt-bigquery==1.7.4

# Copy dbt project files
COPY . .

# Set environment variables
ENV DBT_PROFILES_DIR=/usr/app

CMD ["dbt", "--help"]



