FROM python:${PYTHON_RELEASE:-3.12-alpine}

COPY . /python-backend
WORKDIR /python-backend

RUN rm -rf /opt/venv && \
    python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN pip install -r requirements.txt

CMD ["python3.12", "main.py"]
