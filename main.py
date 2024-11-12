import streamlit as st
from openai import OpenAI
st.title("Medico-Bot💊🩺")

# Get OpenAI API key as input
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Check if the API key is provided
if api_key:
    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("What is up?"):
        # Modify the user input without showing it to the user
        modified_input = f'{user_input} - Answer only medical healthcare related queries. If it is not, decline to answer.'

        st.session_state.messages.append({"role": "user", "content": modified_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your OpenAI API key.")
