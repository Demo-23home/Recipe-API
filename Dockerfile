FROM python:3.9-alpine3.13

LABEL maintainer="demo-23home"

ENV PYTHONUNBUFFERED=1

# Copy requirements first (better layer caching)
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Create working directory
WORKDIR /app

# Copy app code
COPY ./app /app

EXPOSE 8000

ARG DEV=false
# Create virtual environment and install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser -D -H django-user

# Add venv to PATH
ENV PATH="/py/bin:$PATH"

# Switch to non-root user
USER django-user



    