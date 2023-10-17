FROM python:3.10

USER root 
ENV DEBIAN_FRONTEND=noninteractive

# Configure Poetry
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi
RUN source $(poetry env info --path)/bin/activate
COPY . .
CMD ["streamlit", "run","main.py","--server.port=8080","--server.address=0.0.0.0"]