import jinja2
import pickle
import regex
import tweepy
from ext_pathlib import Path
from pprint import pp, pprint
from TweepyTweet import TweepyTweet

files = [
    x
    for x in Path(r"C:\DLs\Mini-Python\twitter crawler").scan("*.txt")
    if regex.search("-pickle", x.stem, regex.I)
]


def load_user(user):
    for f in files:
        if regex.search(f"^{user}", f.stem, regex.I):
            file = f
    if file:
        with open(file, "rb") as fl:
            tweets = pickle.load(fl)
        return tweets
    else:
        print("User not found.")


# print(len(load_user("PeachSaliva")))
twts = load_user("incrrctsuprcorp")
# print(twts[0].__dict__.keys())
# pprint(twts[0].__dict__)
twts = [x for x in twts if not (x.is_retweet or x.is_reply or x.has_pics or x.has_vids)][:100]

def write_tweets(tweets: list[TweepyTweet], name: str):
    url_reg = regex.compile("(https?://[^\s]+)")
    twts = []
    for t in tweets:
        """<a href="atlink" class="at">@PatStaresAt</a>"""
        text = url_reg.sub(r'<a class="at" href="\1">\1</a>', t.text)
        text = regex.sub("\@(.*?)\s", r'<a href="https://twitter.com/\1" class="at">@\1</a> ', text)
        t.text = text
        twts.append(t)
    
    jfile = (
        jinja2.Environment(
            loader=jinja2.FileSystemLoader("./"),
        )
        .get_template("twitter_template.html")
        .render(tweets=twts)
    )

    with open(f"{name}.html", "w", encoding="utf-8") as f:
        f.write(jfile)

# write_tweets(twts, "Paige100")
# write_tweets(twts, "Valkyrae100")
write_tweets(twts, "incrrctsuprcorp100")