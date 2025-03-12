from openai import OpenAI
import json


three_rec_sys_prompt='''You are a music recommendation expert. Your task is to suggest musical artists based on a user’s preferences. 

Sometimes, you will be given the name of a single artist that a hypothetical person really enjoys. In this case, your response should include the names of three artists that they are also likely to enjoy, with each recommendation accompanied by a brief explanation of their sound and why they are a good fit based on the original artist.

At other times, the request may provide more context, such as specific genres, moods, or other musical aspects they are looking for. These requests will be similar to those seen on the subreddit “r/ifyoulikeblank.” When given more complex inputs, carefully consider all relevant details before making your recommendations.

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
    """Sends a user message to OpenAI's chat model and returns the assistant's response."""
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": three_rec_sys_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    response_text = response.choices[0].message.content
    print(response_text)
    print("\n\n\n")
    try:
        structured_data = json.loads(response_text)
        return structured_data
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format received"}

# Example usage
# api_key = "your_openai_api_key"
# response_text = get_openai_response("Give me 5 jazz artists to check out.", api_key)
# print(response_text)


def main():
    api_key = ''
    user_input = "I like the beatles but want something darker and heavier"
    response_text = get_three_chatgpt_recs(user_input, api_key)
    print(response_text)

if __name__ == "__main__":
    main()