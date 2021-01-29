import sys
import os
from dotenv import load_dotenv
import requests
import hashlib
from datetime import datetime

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
    # TODO: test
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
    # TODO: test
    lfp.write("Entered main if\n")
    built_url = build_url(url_from_args)
    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}

    json_response = send_req(built_url, headers)
    responses.append({"full_text": json_response["full_text"],
                      "entities": json_response["entities"],
                      "screen_name": json_response["user"]["screen_name"],
                      "profile_image_url_https": json_response["user"]["profile_image_url_https"]})

    while json_response["in_reply_to_status_id_str"] is not None:
        built_url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + json_response["in_reply_to_status_id_str"] + "&tweet_mode=extended"
        json_response = send_req(built_url, headers)
        responses.append({"full_text": json_response["full_text"],
                          "entities": json_response["entities"],
                          "screen_name": json_response["user"]["screen_name"],
                          "profile_image_url_https": json_response["user"]["profile_image_url_https"]})

    if to_format_from_args == "pdf":
        # TODO: create pdf here
        print()

    elif to_format_from_args == "txt":
        # TODO: test
        lfp.write("entered txt if\n")
        now = datetime.now().strftime("%H:%M:%S.%f")
        now_hex = hashlib.md5(now.encode()).hexdigest()
        filename = responses[-1]["screen_name"] + "--" + now_hex + ".txt"
        fp = open("../fileSystem/" + filename, "w")
        for tweet in reversed(responses):
            fp.write("----------------------**---------------------------\n")
            fp.write("by @" + tweet["screen_name"] + "\n\n")
            fp.writelines(tweet["full_text"] + "\n")
        fp.close()
        lfp.write("printing filename " + filename)
        # TODO: test
        lfp.close()
        print(filename)

    elif to_format_from_args == "ppt":
        # TODO: create txt here
        print()

    else:
        raise Exception(
            "Requested to create a file of unknown format"
        )



    # print(json.dumps(json_response, indent=4, sort_keys=True))
    sys.stdout.flush()
