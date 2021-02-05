# Backend Application of ***twitter-thread-cloner***

## About Twitter-Thread-Cloner
> Go to website: ```http://twittertcloner.ddns.net:4000/```

* Twitter-Thread-Cloner (TTC) is a website service that helps in downloading a twitter thread post in PDF, TXT and ZIP formats.

![TTC Screenshot](https://github.com/Iam-VM/twitter-thread-cloner-server/blob/master/doc/ttc-screenshot.png?raw=true)

## Built With

* ExpressJS
* Python3
* Socket.io

## Where are the scripts ?

The core logic of the backend can be found in ```/twitterScripts``` directory.

## How does it work with the Twitter API ?

* It is expected that the user will input the last tweet from the thread for cloning.
* The system takes this input URL, sends GET request to the URL and receives and stores the information as JSON.
* Then the system will look for the tweet which the previous URL refers and if it does, then sends GET requests to it too.
* The system will keep on sending GET requests for tweet information until the tweet which refers to none.
* Information received from Twitter API in response are saved and used for processing into the required file formats.



