from PIL import Image, ImageDraw, ImageFont
import requests
import hashlib
from datetime import datetime
import os

# creating directory for caching
# dir_name = tweet_response["screen_name"] + "--" + hashlib.md5(datetime.now().strftime().encode()).hexdigest()


# for testing
import json
rp = open("response.json", "r")
json_response = json.load(rp)
rp.close()
responses = [{
    "full_text": json_response["full_text"],
    "entities": json_response["extended_entities"],
    "screen_name": json_response["user"]["screen_name"],
    "profile_image_url_https": json_response["user"]["profile_image_url_https"]}]


def create_pdf(tweet_responses):



create_pdf(responses)
