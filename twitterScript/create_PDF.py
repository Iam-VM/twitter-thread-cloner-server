import hashlib
import sys
from datetime import datetime
import os
import shutil
import create_img
from PyPDF2 import PdfFileReader, PdfFileWriter


# # for testing
# import json
# rp = open("response.json", "r")
# json_response = json.load(rp)
# rp.close()
# responses = [{
#     "full_text": json_response["full_text"],
#     "entities": json_response["extended_entities"],
#     "screen_name": json_response["user"]["screen_name"],
#     "profile_image_url_https": json_response["user"]["profile_image_url_https"]}]


def merge_pdf(dir_name, count):
    sys.stdout.write("MRG")
    sys.stdout.flush()

    pdf_writer = PdfFileWriter()
    for i in range(count):
        pdf_reader = PdfFileReader("{}/{}.pdf".format(dir_name, i))
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    out_file_name = dir_name.split("cache_fileSystem/")[1]
    with open(os.getcwd() + "/fileSystem/{}.pdf".format(out_file_name), 'wb') as out:
        pdf_writer.write(out)
    # TEST
    # with open("../fileSystem/{}.pdf".format(out_file_name), 'wb') as out:
    #     pdf_writer.write(out)

    # removing cache
    shutil.rmtree(dir_name)
    return "{}.pdf".format(out_file_name)


def create_pdf(tweet_responses):
    sys.stdout.write("PRO")
    sys.stdout.flush()

    count = 0
    # creating dir
    dir_name = tweet_responses[-1]["screen_name"] + "__" + hashlib.md5(datetime.now().strftime("%H:%M:%S.%f").encode()).hexdigest()
    dir_name = "twitterScript/cache_fileSystem/{}".format(dir_name)
    # TEST MODE
    # dir_name = "cache_fileSystem/{}".format(dir_name)
    os.mkdir(dir_name)
    for tweet_response in tweet_responses:
        count = create_img.create_img(tweet_response, dir_name=dir_name, count=count)

    return merge_pdf(dir_name=dir_name, count=count)

