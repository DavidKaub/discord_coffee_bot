# set the apikey and limit
import json
import random

import requests as requests

from discord_bot.discord_coffee_reminder import MySettings

app_settings = MySettings()


def get_random_tenor_gif(topic: str, number_of_gifs_to_select_from=100) -> str:
    """Returns the url of a random  gif"""

    # get the top 8 GIFs for the search term
    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (
            topic, app_settings.TENOR_API_KEY, number_of_gifs_to_select_from))

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        response = json.loads(r.content)
        number_of_results = len(response["results"])
        index = random.randint(0, number_of_results - 1)
        selected_gif = response["results"][index]
        url = selected_gif["url"]
        return url
    else:
        raise Exception({"status": r.status_code, "response": r.content})
