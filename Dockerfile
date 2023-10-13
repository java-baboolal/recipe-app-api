FROM python:3.9-alpine3.13
LABEL maintainer="kushwahdeveloper1.com"

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app

EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # /py/bin/pip install -r /tmp/requirements.dev.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"
# USER django-user # commented as throwing permission error

# RUN usermod -aG docker $(whoami)
# RUN chown root:root -R /app/
# RUN adduser -D user
# RUN chown user:user -R /app/
# RUN chmod 777 /app
# USER user
