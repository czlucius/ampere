FROM python:latest
WORKDIR /app
COPY . .
RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install poetry
RUN python3 -m poetry install

CMD ./scripts/bot.sh
