from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import requests
import html

# # test data
# import json
# rp = open("response.json", "r")
# json_response = json.load(rp)
# rp.close()
# responses = [{
#     "full_text": json_response["full_text"],
#     "entities": json_response["extended_entities"],
#     "quoted_status": None,
#     "screen_name": json_response["user"]["screen_name"],
#     "profile_image_url_https": json_response["user"]["profile_image_url_https"]}]


# solving line space overflow issue
def process_full_text(full_text):
    max_len = 95
    full_text_list = [phrase + "\n" for phrase in full_text.split("\n")]
    processed_full_text = ""
    for line in full_text_list:
        if len(line) > max_len:
            i = max_len
            while i > 0:
                if line[i] == " ":
                    line = line[:i] + "\n" + process_full_text(line[i + 1:])
                    break
                i -= 1
        processed_full_text += line

    return processed_full_text


def process_response(tweet_response, mode):
    # creating url for larger dp
    screen_name = "user_name"
    try:
        if mode == "q":
            dp_url_splitted = tweet_response["user"]["profile_image_url_https"].split("_normal")
            screen_name = tweet_response["user"]["screen_name"]
            dp_url_merged = dp_url_splitted[0] + dp_url_splitted[1]
            tweet_response["profile_image_url_https"] = dp_url_merged
        elif mode == "s":
            dp_url_splitted = tweet_response["profile_image_url_https"].split("_normal")
            screen_name = tweet_response["screen_name"]
            dp_url_merged = dp_url_splitted[0] + dp_url_splitted[1]
            tweet_response["profile_image_url_https"] = dp_url_merged
    except Exception as e:
        print(e)

    # configs
    photo_media_thumbnail_size = (600, 600)
    quoted_status_image_size = (800, 800)
    dummy_canvas_size = (1100, 800)
    dp_size = (75, 75)
    padding = (40, 50, 10, 30)
    # username_font = ImageFont.truetype("twitterScript/montserrat/Montserrat-Bold.ttf", 30)
    # full_text_font = ImageFont.truetype("twitterScript/montserrat/Montserrat-Regular.ttf", 18)
    # TEST MODE
    username_font = ImageFont.truetype("montserrat/Montserrat-Bold.ttf", 30)
    full_text_font = ImageFont.truetype("open-sans/OpenSans-Regular.ttf", 18)


    # buckets
    media_bucket = []

    # handle media
    if "entities" in tweet_response and tweet_response["entities"] is not None:
        if "media" in tweet_response["entities"]:
            for media in tweet_response["entities"]["media"]:
                # handling photo media
                # if media["type"] == "photo":
                #     media_image = Image.open(requests.get(media["media_url"], stream=True).raw)
                #     media_image.thumbnail(photo_media_thumbnail_size)
                #     media_bucket.append(media_image)
                media_image = Image.open(requests.get(media["media_url"], stream=True).raw)
                media_image.thumbnail(photo_media_thumbnail_size)
                media_bucket.append(media_image)

    # handle quoted status
    quoted_status_image = None
    if "quoted_status" in tweet_response and tweet_response["quoted_status"] is not None:
        quoted_status_image = process_response(tweet_response["quoted_status"], "q")
        quoted_status_image.thumbnail(quoted_status_image_size)

    # handle full_text and user_name header
    dummy_canvas = Image.new("RGB", dummy_canvas_size, "#ffffff")
    dummy_crop_box_size = (0, 0, 0, 0)
    if "full_text" in tweet_response:
        dummy_draw = ImageDraw.Draw(dummy_canvas)

        # opening dp
        dp_p = Image.open(requests.get(tweet_response["profile_image_url_https"], stream=True).raw)
        dp_p.thumbnail(dp_size)

        dummy_canvas.paste(dp_p, (padding[0], padding[1]))
        username_size = dummy_draw.textsize("@" + screen_name, username_font)
        user_name_position = (
            padding[0] + dp_size[0] + 30,
            padding[1] + dp_size[1]/2 - username_size[1]/2
        )
        dummy_draw.text(user_name_position, "@" + screen_name, fill="#000000", font=username_font, spacing=6)

        # printing full_text
        full_text = html.unescape(process_full_text(tweet_response["full_text"]))

        full_text_size = dummy_draw.textsize(full_text, full_text_font)
        full_text_position = (
            padding[0],
            padding[1] + dp_size[1] + 30
        )
        dummy_draw.text(full_text_position, full_text, fill="#000000", font=full_text_font, spacing=6)

        # cropping
        dummy_crop_box_size = (
            0,
            0,
            dummy_canvas_size[0],
            full_text_position[1] + full_text_size[1] + 30
        )
        dummy_canvas = dummy_canvas.crop(dummy_crop_box_size)

    # calculating total height of media
    media_net_height = 0
    for media in media_bucket:
        media_net_height += media.size[1]

    # creating main canvas
    canvas_size = (
        dummy_canvas_size[0],
        dummy_crop_box_size[3] + media_net_height + len(media_bucket) * 10 + 30 + (quoted_status_image.size[1] if quoted_status_image is not None else 0)
    )
    canvas = Image.new("RGB", canvas_size, "#ffffff")
    canvas_draw = ImageDraw.Draw(canvas)
    canvas.paste(dummy_canvas, (0, 0))

    if quoted_status_image is not None:
        canvas.paste(quoted_status_image, (int(canvas_size[0]/2) - int(quoted_status_image_size[0]/2), dummy_crop_box_size[3]))
        quoted_status_border_rect_box = (
            int(canvas_size[0] / 2) - int(quoted_status_image_size[0] / 2),
            dummy_crop_box_size[3],
            int(canvas_size[0] / 2) - int(quoted_status_image_size[0] / 2) + quoted_status_image.size[0],
            dummy_crop_box_size[3] + quoted_status_image.size[1],
        )
        canvas_draw.rectangle(quoted_status_border_rect_box, outline="#1DA1F2")

    main_canvas_media_position_height = dummy_crop_box_size[3] + 10 + (quoted_status_image_size[1] if quoted_status_image is not None else 0)
    if media_bucket:
        for media_image in media_bucket:
            canvas.paste(media_image, (int(canvas_size[0]/2) - int(media_image.size[0]/2), main_canvas_media_position_height))
            main_canvas_media_position_height += media_image.size[1] + 10

    sharpness = ImageEnhance.Sharpness(canvas)
    return sharpness.enhance(1.5)


def create_img(tweet_response, dir_name, count):
    tweet_img = process_response(tweet_response, "s")
    tweet_img.save("{}/{}.pdf".format(dir_name, count))
    return count + 1

