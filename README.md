# Simple (Coffee Break) reminder discord bot

Warning: *It's working, but it's work in progress*

- Configure as need in `config.py`
- Add `.env` file in project root and add your secret `DISCORD_BOT_TOKEN` (please don't share this token)
- Start the bot running the `main.py`

## Run in Container
```shell
docker build -t coffee_bot .
dokcer run --name my_coffee_bot coffee_bot
```