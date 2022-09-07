FROM python:3.10-slim-bullseye

COPY . /discord_coffee_bot
WORKDIR /discord_coffee_bot

RUN pip install --no-cache-dir -r discord_bot/requirements.txt

ENTRYPOINT ["python3",  "./discord_bot/main.py"]
