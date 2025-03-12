# LLM Music Recommendations

A Streamlit app to generate musical artist recommendations using LLM APIs

[View the page here](https://llm-music-recs.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```
2. Create the secrets file

   ```
   $ touch LLM-music-recommendations/.streamlit/secrets.toml
   ```
3. Add OpenAI key to secrets.toml
   
   ```
   openai_key = 'key-goes-here'
   ```
4. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
