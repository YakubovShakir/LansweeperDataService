FROM python:3.12.2-slim-bookworm
ARG DEBIAN_REPO
ARG PYPI_REPO
ARG POETRY_VERSION=2.1.2
ARG GIT_TAG
ENV WORK_ENV=PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_INDEX_URL=${PYPI_REPO} \
    DEBIAN_FRONTEND=noninteractive \
    DB_HOST="" \
    DB_PORT="" \
    DB_NAME="" \
    DB_USER="" \
    DB_PASS="" \
    PATH="/root/.local/bin:$PATH"\
    GIT_TAG=$GIT_TAG \
    ACCEPT_EULA=Y
RUN \
    echo "deb ${DEBIAN_REPO} stable main" > /etc/apt/sources.list; \
    echo >> /etc/apt/sources.list; \
    echo "deb ${DEBIAN_REPO} stable-updates main" >> /etc/apt/sources.list;

# Установка базовых зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    debconf-utils \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    && rm -rf /var/lib/apt/lists/*
    
COPY ./src/packages/msodbcsql17_17.10.6.1-1_amd64.deb /tmp/
RUN echo "msodbcsql17 msodbcsql/accept_eula boolean true" | debconf-set-selections && \
    dpkg -i /tmp/msodbcsql17_17.10.6.1-1_amd64.deb || (apt-get update && apt-get install -f -y)

# Установка остальных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    rsyslog \
    nginx \
    vim \
    less \
    mc \
    g++ \
    build-essential \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libpq-dev \
    slapd \
    ldap-utils \
    tox \
    lcov \
    valgrind \
    pipx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pipx install poetry==${POETRY_VERSION}
WORKDIR /code
COPY pyproject.toml /code/
COPY README.md /code/
RUN \
    set +x && \
    poetry source add nexus-pypi ${PYPI_REPO} && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi --no-root 
COPY . /code
EXPOSE 8000
CMD ["poetry", "run", "python", "src/main.py"]