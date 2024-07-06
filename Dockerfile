FROM python:3.10

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/

RUN mkdir /srv/project/

WORKDIR /srv/project/

# Copy the poetry files
COPY pyproject.toml /srv/project/

# Install dependencies
RUN poetry install

COPY app /srv/project/app
COPY assets /srv/project/assets
COPY schema /srv/project/schema
COPY src /srv/project/src
COPY tests /srv/project/tests

# Ensure the scripts are executable
RUN chmod +x /app/infra/get_last_price.sh
RUN chmod +x /app/tests/test__infra__get_last_price.sh

RUN mkdir output/

# Ensure Poetry's environment is used for subsequent commands
ENV PATH="/srv/project/.venv/bin:$PATH"

EXPOSE 34617
