import json
import sys
import os
from dotenv import load_dotenv
import requests
import hashlib
from datetime import datetime
import create_PDF

# TODO: test
lfp = open("./script.log", "a")
lfp.write("Entered into script\n")

load_dotenv()

url_from_args = sys.argv[1]
to_format_from_args = sys.argv[2]
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_KEY_SECRET = os.getenv('CONSUMER_KEY_SECRET')
responses = []


def build_url(tweet_url):
    url_parts = tweet_url.split('/')
    tweet_id = url_parts[-1]
    return 'https://api.twitter.com/1.1/statuses/show.json?id=' + tweet_id + "&tweet_mode=extended"


def send_req(url, header):
    # TEST
    lfp.write("Entered send_req \n")
    response = requests.request("GET", url, headers=header)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


if __name__ == '__main__':
    # TEST
    lfp.write("Entered main if\n")
    built_url = build_url(url_from_args)
    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}

    json_response = send_req(built_url, headers)
    responses.append({"full_text": json_response["full_text"],
                      "screen_name": json_response["user"]["screen_name"],
                      "entities": json_response["extended_entities"] if "extended_entities" in json_response else json_response["entities"],
                      "quoted_status": json_response["quoted_status"] if json_response["is_quote_status"] else None,
                      "profile_image_url_https": json_response["user"]["profile_image_url_https"]})

    while json_response["in_reply_to_status_id_str"] is not None:
        built_url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + json_response["in_reply_to_status_id_str"] + "&tweet_mode=extended"
        json_response = send_req(built_url, headers)
        responses.append({"full_text": json_response["full_text"],
                          "quoted_status": json_response["quoted_status"] if json_response["is_quote_status"] else None,
                          "entities": json_response["extended_entities"] if "extended_entities" in json_response else json_response["entities"],
                          "screen_name": json_response["user"]["screen_name"],
                          "profile_image_url_https": json_response["user"]["profile_image_url_https"]})

    responses.reverse()

    if to_format_from_args == "pdf":
        # TODO: create pdf here
        filename = create_PDF.create_pdf(responses)

        sys.stdout.write(filename)

    elif to_format_from_args == "txt":
        # TEST
        lfp.write("entered txt if\n")
        now = datetime.now().strftime("%H:%M:%S.%f")
        now_hex = hashlib.md5(now.encode()).hexdigest()
        filename = responses[-1]["screen_name"] + "--" + now_hex + ".txt"
        fp = open(os.path.join(os.getcwd() + "/fileSystem", filename), "w")
        # for tests
        # fp = open(os.path.join(os.getcwd() + "/../fileSystem", filename), "w")
        for tweet in responses:
            fp.write("----------------------Tweet---------------------------\n")
            fp.write("by @" + tweet["screen_name"] + "\n\n")
            fp.writelines(tweet["full_text"] + "\n\n")
            if "entities" in tweet:
                if "media" in tweet["entities"]:
                    fp.write("----Media----\n")
                    for media in tweet["entities"]["media"]:
                        fp.write("{}: {}\n".format(media["type"], media["media_url"]))
                    fp.write("--------\n")
            if "quoted_status" in tweet and tweet["quoted_status"] is not None:
                fp.write("----Quoted----\n")
                if "full_text" in tweet["quoted_status"]:
                    fp.write("{}\n\n".format(tweet["quoted_status"]["full_text"]))
                if "entities" in tweet["quoted_status"]:
                    if "media" in tweet["quoted_status"]["entities"]:
                        fp.write("-Quoted-Media-\n")
                        for media in tweet["quoted_status"]["entities"]["media"]:
                            fp.write("{}: {}\n".format(media["type"], media["media_url"]))
                        fp.write("---\n\n")
                fp.write("--------\n\n")

        fp.close()
        lfp.write("printing filename " + filename)
        # TEST
        lfp.close()
        sys.stdout.write(filename)

    elif to_format_from_args == "ppt":
        # TODO: create ppt here
        print()

    else:
        raise Exception(
            "Requested to create a file of unknown format"
        )



    # print(json.dumps(json_response, indent=4, sort_keys=True))
    sys.stdout.flush()
