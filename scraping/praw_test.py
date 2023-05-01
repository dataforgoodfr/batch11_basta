import praw
import json
from praw.models import MoreComments

reddit = praw.Reddit(
    client_id="Your_app_id",
    client_secret="Your_app_secret",
    username="Your_username_on_reddit (u/...)",
    password="Your_reddit_password",
    user_agent="Your_app_name/0.0.1",
)


posts = {}

subs = ["Feminisme", "Elles", "AskMeuf"]
for sub in subs:
    subreddit = reddit.subreddit(sub)
    for submission in subreddit.new(limit=1500):
        posts[submission.id] = {}
        posts[submission.id]["title"] = submission.title
        posts[submission.id]["text"] = submission.selftext
        posts[submission.id]["time"] = submission.created_utc
        posts[submission.id]["flair"] = submission.author_flair_text
        posts[submission.id]["url"] = submission.url
        posts[submission.id]["subreddit"] = submission.subreddit.display_name
        posts[submission.id]["comments"] = []
        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue
            posts[submission.id]["comments"].append(comment.body)

with open("posts.json", "w") as fp:
    json.dump(posts, fp)
