import streamlit as st
import pandas as pd
import llm_music_utils

st.title("LLM Music Recommendations")
st.write(
    "Enter a request, receive recommendations"
)

openai_api_key = st.secrets['openai_key']

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:


    user_input = st.text_input(label="", placeholder="Enter an artist's name, or more")
    
    if user_input:
        response = llm_music_utils.get_three_chatgpt_recs(user_input, openai_api_key)
        recommendations = response["recommendations"]
        additional_notes = response["additional_notes"]
        recommendations_df = pd.DataFrame(recommendations)
        
        for rec in recommendations:
            with st.container():
                col1, col2 = st.columns(2, border=True)
                with col1:
                    st.write(f"### {rec['artist']}")
                with col2:
                    st.write(rec['description'])    
        
        st.write(additional_notes)   
