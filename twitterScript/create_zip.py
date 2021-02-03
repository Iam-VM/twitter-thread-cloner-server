import sys
from datetime import datetime
import os
import create_img
import hashlib
import shutil
import wget


def extract_media(tweet_response, dir_name):
    count = 1
    if "entities" in tweet_response and tweet_response["entities"] is not None:
        if "media" in tweet_response["entities"]:
            for media in tweet_response["entities"]["media"]:
                downloaded = False
                sys.stdout.write("EMN:{}".format(count))
                sys.stdout.flush()
                if media["type"] == "photo":
                    wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1]), bar=None)
                    count += 1
                elif media["type"] == "video":
                    if "video_info" in media:
                        if "variants" in media["video_info"]:
                            for video in media["video_info"]["variants"]:
                                if "content_type" in video:
                                    if video["content_type"] == "video/mp4":
                                        wget.download(video["url"], "{}/{}".format(dir_name, video["url"].split("/")[-1]), bar=None)
                                        count += 1
                                        downloaded = True
                                        break
                    if not downloaded:
                        wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1]), bar=None)
                        count += 1
                elif media["type"] == "animated_gif":
                    if "video_info" in media:
                        if "variants" in media["video_info"]:
                            for video in media["video_info"]["variants"]:
                                if "content_type" in video:
                                    if video["content_type"] == "video/mp4":
                                        wget.download(video["url"], "{}/{}".format(dir_name, video["url"].split("/")[-1]), bar=None)
                                        count += 1
                                        downloaded = True
                                        break
                    if not downloaded:
                        wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1]), bar=None)
                        count += 1
                else:
                    wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1]), bar=None)
                    count += 1

    if "quoted_status" in tweet_response and tweet_response["quoted_status"] is not None:
        if "entities" in tweet_response["quoted_status"]:
            if "media" in tweet_response["entities"]:
                for media in tweet_response["entities"]["media"]:
                    downloaded = False
                    sys.stdout.write("EMN:{}".format(count))
                    sys.stdout.flush()
                    if media["type"] == "photo":
                        wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1].split("?")[0]), bar=None)
                        count += 1
                    elif media["type"] == "video":
                        if "video_info" in media:
                            if "variants" in media["video_info"]:
                                for video in media["video_info"]["variants"]:
                                    if "content_type" in video:
                                        if video["content_type"] == "video/mp4":
                                            wget.download(video["url"], "{}/{}".format(dir_name, video["url"].split("/")[-1].split("?")[0]), bar=None)
                                            count += 1
                                            downloaded = True
                                            break
                        if not downloaded:
                            wget.download(media["media_url"],
                                          "{}/{}".format(dir_name, media["media_url"].split("/")[-1].split("?")[0]), bar=None)
                            count += 1
                    elif media["type"] == "animated_gif":
                        if "video_info" in media:
                            if "variants" in media["video_info"]:
                                for video in media["video_info"]["variants"]:
                                    if "content_type" in video:
                                        if video["content_type"] == "video/mp4":
                                            wget.download(video["url"], "{}/{}".format(dir_name, video["url"].split("/")[-1].split("?")[0]), bar=None)
                                            count += 1
                                            downloaded = True
                                            break
                        if not downloaded:
                            wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1].split("?")[0]), bar=None)
                            count += 1
                    else:

                        wget.download(media["media_url"], "{}/{}".format(dir_name, media["media_url"].split("/")[-1].split("?")[0]), bar=None)
                        count += 1


def zip_dir(out, to_zip_dir):
    shutil.make_archive(out, 'zip', to_zip_dir)
    return out.split("/")[-1] + ".zip"


def create_zip(tweet_responses):
    sys.stdout.write("PRO")
    sys.stdout.flush()

    count = 0
    # creating dir
    dir_name = tweet_responses[-1]["screen_name"] + "__" + hashlib.md5(
        datetime.now().strftime("%H:%M:%S.%f").encode()).hexdigest()
    dir_name = "twitterScript/cache_fileSystem/{}".format(dir_name)
    # TEST MODE
    # dir_name = "cache_fileSystem/{}".format(dir_name)
    os.mkdir(dir_name)
    os.mkdir(dir_name + "/media")
    for tweet_response in tweet_responses:
        count = create_img.create_img(tweet_response, dir_name=dir_name, count=count)
        extract_media(tweet_response, dir_name=dir_name + "/media")
    sys.stdout.write("ZIP")
    sys.stdout.flush()
    filename = "fileSystem/{}".format(dir_name.split("/")[-1])
    # TEST MODE
    # filename = "../fileSystem/{}".format(dir_name.split("/")[-1])
    filename = zip_dir(filename, dir_name)

    return filename
