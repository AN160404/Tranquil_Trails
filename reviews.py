import requests
import asyncio
import asyncpraw
import pandas as pd
import time
from datetime import datetime

def search_youtube(api_key, query, max_results=5):
    # YouTube API URL
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults={max_results}&key={api_key}'

    # Make the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Error occurred while fetching data from YouTube API")
        return []

    data = response.json()

    # Parse the results
    video_details = []
    for item in data.get('items', []):
        video_id = item['id'].get('videoId', None)
        if video_id:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_details.append({
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'video_url': video_url,
                'thumbnail_url': item['snippet']['thumbnails']['default']['url']
            })

    return video_details


async def fetch_reddit_data(query):
    reddit = asyncpraw.Reddit(client_id='vaGRzJF8B7WelHKQDzvf3w', client_secret='Ngwb0UqRiPbnLEZQdaCWEDGrwUbLzQ', user_agent='test by u/Huge_Donut9460')

    # Define the list of subreddits and limits
    subreddits = ['india']  # Add more subreddits as needed
    post_limit = 20
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
    def print_urls(df):
        print("\nPost URLs:")
        urls = df['url'].tolist()
        for url in urls:
            print(url)

    # Print the URLs
    print_urls(posts_df)



def main():
    api_key = 'AIzaSyAxM1LCOMf-EIZO5cf-4n3ouQbRi7PQr70'  # Replace with your actual API key

    # Get search query from user
    query = input("Enter search query for Youtube: ")

    # Get search results
    results = search_youtube(api_key, query)

    # Print the results
    if results:
        print(f"\nTop {len(results)} results for '{query}':\n")
        for i, result in enumerate(results, start=1):
            print(f"Result {i}:")
            print(f"Video URL: {result['video_url']}")
    else:
        print("No results found.")

    # Get user input for the query
    user_query = input("Enter your search query: ")
    
    await fetch_reddit_data(user_query)
if __name__ == '__main__':
    main()

