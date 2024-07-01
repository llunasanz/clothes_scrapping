FROM python:3.10

WORKDIR /srv/project/

# Copy only the requirements file first for better caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY assets assets
COPY schema schema
COPY src src
COPY tests tests

RUN mkdir -p output

EXPOSE 34617

# Use a non-root user
RUN useradd -ms /bin/bash appuser
USER appuser
