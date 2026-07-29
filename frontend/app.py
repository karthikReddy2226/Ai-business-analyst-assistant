import streamlit as st
import requests

st.title("🤖 AI Business Analyst")

question = st.text_input("Ask your question")

if st.button("Analyze"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            res = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question},
                timeout=60,
            )
            res.raise_for_status()
            st.write(res.json()["response"])
        except requests.exceptions.ConnectionError:
            st.error("Could not reach the backend. Is `uvicorn main:app` running on port 8000?")
        except Exception as e:
            st.error(f"Error: {e}")