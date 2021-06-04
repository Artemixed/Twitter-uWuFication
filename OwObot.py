import tweepy
from threading import Thread
from queue import Queue

from datetime import datetime
from owotext import OwO
from urlextract import URLExtract
from urllib3.exceptions import ProtocolError

# Huohhhh. Setup da convewtew ʕʘ‿ʘʔ
uwu = OwO()

# Authenticate to Twitter
auth = tweepy.OAuthHandler("API KEY HERE", "SECRET HERE")
auth.set_access_token("ACCESS TOKEN HERE",
                      "SECRET TOKEN HERE")
api = tweepy.API(auth)

# user ID of Twitter user you want to repost
user_id = "ENTER USER ID HERE"

print("It's alive!: ", datetime.now().strftime("%H:%M:%S"))


# override tweepy.StreamListener to add logic to on_status
class twitter_parser(tweepy.StreamListener):
    api = tweepy.API(auth)

    def __init__(self, q=Queue()):
        num_worker_threads = 2
        self.q = q
        for i in range(num_worker_threads):
            t = Thread(target=self.parse_post_message)
            t.daemon = True
            t.start()

    def on_connect(self):
        print("Bot is connected", datetime.now().strftime("%H:%M:%S"))

    def on_exception(self, exception):
        print(exception)
        print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        return

    def on_status(self, status):
        self.q.put(status)

    def parse_post_message(self):
        while True:

            status = self.q.get()

            if status and status.user and status.user.id and status.text and status.user.id == int(user_id):

                extractor = URLExtract()
                urls = extractor.find_urls(status.text)
                status_text = status.text
                url_dictionary = {}

                if len(urls) > 0:
                    count = 0

                    for url in urls:
                        status_text = status_text.replace(url, "<" + str(count) + ">")
                        url_dictionary[str(count)] = url
                        count += 1

                status_text_owo = uwu.whatsthis(status_text)

                if len(urls) > 0:
                    for key in url_dictionary:
                        status_text_owo = status_text_owo.replace("<" + str(key) + ">",
                                                                  url_dictionary.get(str(key)))

                print(status_text_owo, datetime.now().strftime("%H:%M:%S"))
                api.update_status(status_text_owo)

            self.q.task_done()


while True:
    try:
        myStreamListener = twitter_parser()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(follow=[user_id], stall_warnings=True)
        break
    except ProtocolError as e:
        print(e)
        print("ProtocolError happened; Current Time =", datetime.now().strftime("%H:%M:%S"))
        continue
    except AttributeError as ef:
        print(ef)
        print("AttributeError happened; Current Time =", datetime.now().strftime("%H:%M:%S"))
        continue
