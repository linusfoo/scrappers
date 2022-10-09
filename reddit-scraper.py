import praw
from praw.models import MoreComments
import csv
import pandas as pd
import re
import string


subreddits = [ 'singaporeRaw','singapore', 'sporeuncensored'] 


###GET YOUR CLIENT ID, SECRET, USER AGENT
reddit = praw.Reddit(client_id= , client_secret=  , user_agent= ) #TODO: add client id, secret, user_agent

# global_counter = 0
for subreddit in subreddits:   

    # subreddit_counter = 0
    posts = []
    sg_subreddit = reddit.subreddit(subreddit)
    for post in sg_subreddit.top(limit = 1000000):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    print(posts['title'])
    
    for i , row in posts.iterrows():


        ####FOR YOUR TO GET WHATEVER INFO YOU WANT, TITLE, SCORE, ID ...
        all = []
        s = ''
        ID = row['id']
        TITLE = row['title']
        s+= TITLE.replace("\n", "") + '. ' 
        # print("TITLE IS" + TITLE)
        submission = reddit.submission(id=ID) 
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            # print(comment)


            ##CLEANING DATA
            c = comment.body
            c = c.replace("\n","") 
            if len(c.split()) > 1 and not c.startswith('[**Info**]'):  
                c = "".join(filter(lambda char: char in string.printable,c))
                s += c + '. '
        with open("data/reddit_merge/" + subreddit + ".csv", "a", newline='',encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([s])
