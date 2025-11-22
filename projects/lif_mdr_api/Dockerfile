FROM python:3.13-slim

ARG wheel=lif_mdr_api-0.1.0-py3-none-any.whl

ARG deps=requirements.txt

RUN python -m pip install --upgrade pip

WORKDIR /code

COPY ./dist/$wheel /code/$wheel
COPY ./$deps /code/$deps
COPY ./bin /code/bin

# This is adjusted to install third-party dependencies separately (the --no-deps) and install from requirements
RUN pip install --no-cache-dir --upgrade --no-deps /code/$wheel
RUN pip install -r /code/$deps

ENTRYPOINT ["./bin/startup.sh"]
EXPOSE 8012/tcp
