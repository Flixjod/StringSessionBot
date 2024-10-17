import env
import logging
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from flask import Flask
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, encoding="utf-8", format="%(asctime)s - %(levelname)s - \033[32m%(pathname)s: \033[31m\033[1m%(message)s \033[0m")

app = Client(
    "Session_bot",
    api_id=env.API_ID,
    api_hash=env.API_HASH,
    bot_token=env.BOT_TOKEN,
    in_memory=True,
    plugins={'root':'StringSessionBot'},
)


@app.route('/')
def hello_world():
    return 'Bot Alive'

@app.route('/health', methods=['GET'])
def health_check():
    return 'ok', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.PORT)
    logging.info("Starting the bot")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    uname = app.me.username
    logging.info(f"@{uname} is now running!")
    idle()
    app.stop()
    logging.info("Bot stopped. Alvida!")


