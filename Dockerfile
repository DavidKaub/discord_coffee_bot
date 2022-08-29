FROM python:3.10-slim-bullseye

WORKDIR /discord_bot
COPY discord_bot/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python ./discord_bot/main.py
# CMD [ "python", "main.py"]