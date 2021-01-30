from PIL import Image, ImageDraw, ImageFont
import requests
import hashlib
import os
from datetime import datetime

# test data
import json
rp = open("response.json", "r")
json_response = json.load(rp)
rp.close()
responses = [{
    "full_text": json_response["full_text"],
    "entities": json_response["extended_entities"],
    "screen_name": json_response["user"]["screen_name"],
    "profile_image_url_https": json_response["user"]["profile_image_url_https"]}]


def create_img(tweet_response, dir_name, count):
    # creating url for larger dp
    dp_url_splitted = tweet_response["profile_image_url_https"].split("_normal")
    dp_url_merged = dp_url_splitted[0] + dp_url_splitted[1]
    tweet_response["profile_image_url_https"] = dp_url_merged

    # creating a canvas to work with
    canvas_width = 1149
    canvas_height = 800
    canvas_size = (canvas_width, canvas_height)
    canvas = Image.new("RGB", canvas_size, "#ffffff")
    img_draw = ImageDraw.Draw(canvas)

    # paddings
    left_padding = 50
    top_padding = 40
    right_padding = 50
    # TODO: Set this
    bottom_padding = None

    # opening dp and thumbnail sizing
    dp_p = Image.open(requests.get(tweet_response["profile_image_url_https"], stream=True).raw)
    dp_p_thumbnail_size = (75, 75)
    dp_p.thumbnail(dp_p_thumbnail_size)

    # pasting dp
    dp_position = (left_padding, top_padding)
    canvas.paste(dp_p, dp_position)

    # writing username
    username_font = ImageFont.truetype("montserrat/Montserrat-Bold.ttf", 30)
    username_text_width, username_text_height = img_draw.textsize("@" + tweet_response["screen_name"], username_font)
    username_position = (
        dp_position[0] + dp_p_thumbnail_size[0] + dp_p_thumbnail_size[0] / 2,
        dp_position[1] + dp_p_thumbnail_size[1] / 2 - username_text_height/2)
    img_draw.text(username_position, "@" + tweet_response["screen_name"], fill="#000000", font=username_font)

    # flag representing presence of full_text
    has_full_text = False

    # other_vars
    full_text_text_width = None
    full_text_text_height = None

    if tweet_response["full_text"]:
        has_full_text = True
        # writing full_text
        full_text_font = ImageFont.truetype("montserrat/Montserrat-Regular.ttf", 18)
        full_text_text_width, full_text_text_height = img_draw.textsize(tweet_response["full_text"], full_text_font)
        full_text_position = (
            dp_position[0],
            dp_position[1] + dp_p_thumbnail_size[1] + 50
        )
        img_draw.text(full_text_position, tweet_response["full_text"], fill="#000000", font=full_text_font)

        # cropping
        crop_box = (
            0,
            0,
            canvas_width,
            top_padding + dp_p_thumbnail_size[1] + 50 + full_text_text_height + 50
        )
        cropped_canvas = canvas.crop(crop_box)
        # TODO: get rid of this in production
        # cropped_canvas.show()
        cropped_canvas.save("{}/{}.png".format(dir_name, count))
        count += 1

    if tweet_response["entities"]["media"]:
        media_number = 1
        for media in tweet_response["entities"]["media"]:
            # TODO: handle non photo media
            if media["type"] == "photo":
                if not has_full_text:
                    if media_number == 1:
                        media_position_main_page = (
                            left_padding,
                            top_padding + dp_p_thumbnail_size[1] + 50
                        )
                        media_size_main_page = (
                            canvas_width - 2 * left_padding,
                            canvas_height - media_position_main_page[1] + 10
                        )
                        media_p = Image.open(requests.get(media["media_url"], stream=True).raw)
                        media_p.thumbnail(media_size_main_page)
                        canvas.paste(media_position_main_page, media_p)
                        media_number += 1
                        # TODO: get rid of this in production
                        # canvas.show()
                        canvas.save("{}/{}.png".format(dir_name, count))
                        count += 1

                media_size_more_media = (
                    canvas_width - 2 * left_padding,
                    canvas_height - 10
                )
                media_p = Image.open(requests.get(media["media_url"], stream=True).raw)
                media_p.thumbnail(media_size_more_media)
                # TODO: get rid of this in production
                # media_p.show()
                media_p.save("{}/{}.png".format(dir_name, count))
                count += 1

    return count


create_img(responses[0], "cache_fileSystem/gibra", 0)
