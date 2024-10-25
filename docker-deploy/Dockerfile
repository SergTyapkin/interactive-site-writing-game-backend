FROM python:${PYTHON_RELEASE:-3.12-slim}

COPY . /python-backend
WORKDIR /python-backend

RUN rm -rf /opt/venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt

RUN export PORT=${WS_PORT}
CMD ["python3.12", "main.py"]
