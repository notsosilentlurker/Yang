"""
Created on Wed Oct 23 11:25:18 2019

@author: notsosilentlurker
@author: MyNameWuzTaken
"""


import praw
import pandas as pd
import numpy as np
from praw.models import MoreComments
import matplotlib.pyplot as plt
import importlib.util


# Import your client scraping function file. This allows Git Commit without recvealing your secret key stuff.
spec = importlib.util.spec_from_file_location("scraping_info", "C:\Sourcing\scraping_info.py")
imp_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp_loader)
client_id = imp_loader.reddit_client_id()
client_secret = imp_loader.reddit_client_secret()
user_agent = imp_loader.reddit_client_user_agent()

#You will need to fill in the client id, client secret, user agent, and reddit thread id (the one for the big askreddit thread is dko28q)
#You can get these numbers by getting access to the reddit api, its really simple, the walkthrough here: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
#goes through everything you need to get access.
# This holds a list of thread ids for different posts to scrape.
# Currently doesn't allow multiple threads
thread_list = ['dko28q']
all_threads = {}

# Only Scrapes data if object doesn;t exist
if 'reddit' not in locals():
	reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

if 'submission' not in locals():
	posts = []
	for thread in thread_list:
		submission = reddit.submission(id=thread)
		submission.comments.replace_more(limit=None)
		for top_level_comment in submission.comments:
			posts.append(top_level_comment.body)
		all_threads.update({thread : posts})

noun_list = ['debt','loans','groceries','car','health',
			 'food','rent','saving','stress','bill','retirement',
			 'move','drugs','future','beer','alcohol','marijuana','child']

counts = []

# This code makes sure only the first thread in the list runs
posts = posts[0]

All_Thread_Posts = pd.Series(posts)

length = len(All_Thread_Posts)
print(length)

for key in noun_list:
	counts.append(len(All_Thread_Posts.str.findall(key).to_frame().applymap(str).replace('[]', np.nan).dropna()))

for i, key in enumerate(noun_list):
	print('Number of times {} was mentioned: {}'.format(noun_list[i],counts[i]))

totals = pd.DataFrame(data = np.array(counts),
                                index = noun_list)

sum_ = int(totals.sum())
print(totals.sort_values(by = 0, ascending = False))
average_ = (totals/sum_)*100

print(average_.sort_values(by = 0, ascending = False))

x_labels = totals.index

plot = average_.plot.bar()
plot