import asyncio
import asyncpraw
import pandas as pd
import time
from datetime import datetime

async def fetch_reddit_data(query):
    async with asyncpraw.Reddit(client_id='vaGRzJF8B7WelHKQDzvf3w', client_secret='Ngwb0UqRiPbnLEZQdaCWEDGrwUbLzQ', user_agent='test by u/Huge_Donut9460') as reddit:

        # Define the list of subreddits and limits
        subreddits = ['india']  # Add more subreddits as needed
        post_limit = 5
        comment_limit = 5

        # Initialize lists to hold posts and comments
        all_posts = []
        all_comments = []

        for subreddit_name in subreddits:
            # Fetch posts
            posts = []
            subreddit = await reddit.subreddit(subreddit_name)

            try:
                async for submission in subreddit.search(query, limit=post_limit):
                    posts.append([
                        submission.id,  # Store post ID
                        submission.url,  # Store post URL
                        submission.title,  # Store post title
                        submission.selftext,  # Store post selftext
                        datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        subreddit_name
                    ])
            except asyncpraw.exceptions.RedditAPIException as e:
                if e.error_type == 'SUBREDDIT_NOT_FOUND':
                    print(f"Subreddit '{subreddit_name}' not found.")
                else:
                    raise e

            # Create a DataFrame for posts with the required columns
            posts_df = pd.DataFrame(posts, columns=['id', 'url', 'title', 'selftext', 'created_date', 'subreddit'])

            # Function to fetch comments
            async def fetch_comments(submission_id):
                comments = []
                submission = await reddit.submission(id=submission_id)
                await submission.comments.replace_more(limit=comment_limit)
                async for comment in submission.comments:
                    comments.append([
                        submission_id,  # Store post ID for reference
                        comment.id,  # Store comment ID
                        comment.body,  # Store comment body
                        datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    ])
                return comments

            # Fetch comments for each post
            for post_id in posts_df['id']:
                while True:
                    try:
                        all_comments.extend(await fetch_comments(post_id))
                        break
                    except asyncpraw.exceptions.RedditAPIException as e:
                        if e.error_type == 'RATELIMIT':
                            print(f"Rate limit exceeded. Waiting for {e.sleep_time} seconds")
                            time.sleep(e.sleep_time)
                        else:
                            raise e

        # Create DataFrame for comments
        comments_df = pd.DataFrame(all_comments, columns=['post_id', 'comment_id', 'body', 'created_date'])

        # Function to print only URLs from posts DataFrame
        def get_urls(df):
            return df['url'].tolist()

        # Return the URLs
        return get_urls(posts_df)
