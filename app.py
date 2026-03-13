import streamlit as st
import requests

st.title("LLM Evaluation Tool")

prompt = st.text_area("Prompt")
response = st.text_area("Model Response")
rubric = st.text_input(
    "Rubric",
    "Rate the response on accuracy, helpfulness and clarity"
)

# LLM dropdown
judge_model = st.selectbox(
    "Choose Evaluator Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
)

if st.button("Evaluate"):

    res = requests.post(
        "http://127.0.0.1:8000/evaluate",
        json={
            "prompt": prompt,
            "response": response,
            "rubric": rubric,
            "judge_model": judge_model
        }
    )

    if res.status_code == 200:
        data = res.json()

        st.success("Evaluation Complete")

        st.write("### Score")
        st.write(data["score"])

        st.write("### Reasoning")
        st.write(data["reasoning"])

        st.write("### Latency (ms)")
        st.write(data["latency_ms"])

    else:
        st.error("API Error")