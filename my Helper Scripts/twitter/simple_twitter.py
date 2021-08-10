#! python3
"""
My simple twitter api experiment.
The script can update status, optionally with one media,
delete tweets by id,
display a timeline,
show recent retweets or mentions.
"""
import tweepy
import pathlib
from time import sleep


CWD = pathlib.Path(__file__).resolve().parent
DATA = pathlib.Path(CWD, "data")
KEYS_FILES = [
    pathlib.Path(DATA, "consumer_api_key"),
    pathlib.Path(DATA, "consumer_api_key_secret"),
    pathlib.Path(DATA, "authentication_access_token"),
    pathlib.Path(DATA, "authentication_access_token_secret")
]
KEYS = {
    'consumer_key': "api key: ",
    'consumer_secret': "api key secret: ",
    'access_token': "access token: ",
    'access_secret': "access token secret: "
}

COMMANDS = [
    "home [timeline]",
    "20 most recent [retweets] of me",
    "20 most recent [mentions] of me",
    "[tweet]",
    "[delete]",
    "[exit]"
]


def main():    
    t = load()
    me = t.me()
    hello = f"Hello @{me.screen_name}!\n"
    hello += f"id: {me.id}\n"
    hello += f"following: {me.friends_count}, followers: {me.followers_count}\n"
    hello += f"tweets: {me.statuses_count}, liked: {me.favourites_count}"
    print(hello)

    while True:
        print("\n# options:")
        print(*[f"\t{c}" for c in COMMANDS], sep="\n")
        answer = input("\twhat will you please? ")
        
        if "timeline" in answer:
            print()
            for status in t.home_timeline(include_entities=False):
                user = f"@{status.user.screen_name} ({status.user.name})"
                date = str(status.created_at)
                reply = "reply^" if status.in_reply_to_status_id else ""
                likes = status.favorite_count
                retweets = status.retweet_count
                print(f"{user} {date} {reply}\n[{status.text}]\nlikes: {likes}, retweets: {retweets}")
                print("\t***")
                sleep(0.1)

        elif "retweets" in answer:
            print()
            for status in t.retweets_of_me():
                print(f"id: {status.id}\nin: {status.created_at}\n[{status.text}]")
                print("\t***")
                sleep(0.1)
        
        elif "mentions" in answer:
            print()
            for status in t.mentions_timeline():
                print(f"id: {status.id}\nin: {status.created_at}\n[{status.text}]")
                print("\t***")
                sleep(0.1)

        elif "tweet" in answer:
            media_obj = None
            while True:
                media = input("upload media? (y/n) ").lower()
                if media == "y":
                    while len(media) <= 1:
                        media = input("absolute path: ")
                    media_obj = t.media_upload(media)
                    media = True
                    break
                elif media == "n":
                    media = False
                    break

            while True:
                text = input("tweet text: ")
                if 0 < len(text) < 250:
                    break
                elif len(text) >= 250:
                    print("the text is too big :C")

            if not media:
                result = t.update_status(text)
            else:
                result = t.update_status(text, media_ids=[media_obj.media_id_string])

            print(f"tweeted at {result.created_at}")

        elif "delete" in answer:
            to_dell = []
            print("enter id's to destroy by entering one at a time and an empty line for execution:")
            while True:
                num = input()
                if num:
                    try:
                        to_dell.append(int(num))
                    except TypeError:
                        print("id must be int")
                else:
                    break
            
            for status in to_dell:
                t.destroy_status(status)
                sleep(0.1)
            else:
                print("clear")

        elif "exit" in answer:
            break


def load():
    """ Load api-keys from files or command line. """
    found = False
    if DATA.exists():
        try:
            for key, file in zip(KEYS, KEYS_FILES):
                with open(file, 'r') as reader:
                    KEYS[key] = reader.readline().strip()
            found = True
        except OSError:
            pass

    if not found:
        print("files with keys not found; please enter:")
        for key in KEYS:
            print(KEYS[key], end='')
            c = 0
            while c == 0:
                KEYS[key] = input()
                c = len(KEYS[key])

    auth = tweepy.OAuthHandler(KEYS['consumer_key'], KEYS['consumer_secret'])
    auth.set_access_token(KEYS['access_token'], KEYS['access_secret'])
    return tweepy.API(auth)


if __name__ == "__main__":
    main()
