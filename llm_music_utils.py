from openai import OpenAI
import json
import requests
import base64


three_rec_sys_prompt='''You are a music recommendation expert. Your task is to suggest musical artists based on a user’s preferences. 

Sometimes, you will be given the name of a single artist that a hypothetical person really enjoys. In this case, your response should include the names of three artists that they are also likely to enjoy, with each recommendation accompanied by a brief explanation of their sound and why they are a good fit based on the original artist. If there are any albums that might be particularly relevant, feel free to mention them in your descriptions.

At other times, the request may provide more context, such as specific genres, moods, or other musical aspects they are looking for. These requests will be similar to those seen on the subreddit “r/ifyoulikeblank.” When given more complex inputs, carefully consider all relevant details before making your recommendations.

If possible, aim to provide diverse recommendations within the requested style, including both well-known and lesser-known artists. Your goal is to make thoughtful, high-quality suggestions that align with the user’s taste.

### **Response Format**
Always format your response as a JSON object with the following structure:

{
  "recommendations": [
    {
      "artist": "Artist Name",
      "description": "A description of their music, key characteristics, and why they are a relevant recommendation."
    },
    {
      "artist": "Artist Name",
      "description": "Description"
    },
    {
      "artist": "Artist Name",
      "description": "Description"
    }
  ],
  "additional_notes": "Use this space for errors or anything else that the user should know."
}

Your response must always be a valid JSON object with this exact structure. Do not include any other text or formatting outside of the JSON. Do not include any backticks or the word "json"

'''

def get_three_chatgpt_recs(user_input: str, api_key: str) -> str:
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": three_rec_sys_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    response_text = response.choices[0].message.content

    try:
        structured_data = json.loads(response_text)
        return structured_data
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format received"}



def get_spotify_access_token(client_id: str, client_secret: str):
    """
    Get an OAuth access token from Spotify.

    Parameters:
        client_id (str): Your Spotify API Client ID.
        client_secret (str): Your Spotify API Client Secret.

    Returns:
        str: The access token, or an error message if the request fails.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return {"error": f"Failed to get access token: {response.json()}"}



def get_related_artists(artist_name: str, access_token: str):
    """
    Given an artist's name, fetch their related artists from Spotify's API.
    
    Parameters:
        artist_name (str): The name of the artist to search for.
        access_token (str): A valid Spotify API OAuth token.

    Returns:
        list: A list of related artist names or an error message.
    """
    # Step 1: Get the artist's Spotify ID
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1  # We only need the top result
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch artist ID: {response.json()}"}
    
    results = response.json()
    if not results["artists"]["items"]:
        return {"error": "No artist found with that name."}
    
    
    artist_id = results["artists"]["items"][0]["id"]
    print(artist_id)
    # Step 2: Get related artists
    #related_url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    related_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    print(related_url)
    response = requests.get(related_url, headers=headers)
    print(headers)
    print(response.json())
    if response.status_code != 200:
        return {"error": f"Failed to fetch related artists: {response.json()}"}
    
    related_artists = response.json()["artists"]
    
    # Extract and return artist names
    return [artist["name"] for artist in related_artists]



def main():
    # api_key = ''
    # user_input = "I like the beatles but want something darker and heavier"
    # response_text = get_three_chatgpt_recs(user_input, api_key)
    # print(response_text)
    
    client_id = "spotify id"
    client_secret = "spotify secret"
    access_token = get_spotify_access_token(client_id, client_secret)
    print(access_token)  # Use this in your API calls
    related_artists = get_related_artists("Black Sabbath", access_token)
    print(related_artists)
if __name__ == "__main__":
    main()