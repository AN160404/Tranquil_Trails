import requests

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
    
   
if __name__ == '__main__':
    main()