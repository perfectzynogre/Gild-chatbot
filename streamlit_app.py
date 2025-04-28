import streamlit as st
import time
import re

# Define your images mapping
images = {
    "question 1 2d image": "assets/q1_2d.png",
    "question 1 3d image": "assets/q1_3d.png",  # Add this if you have a 3d image for question 1
    "question 2 image": "assets/q2.png",
    "question 3 image": "assets/q3.png",
    "question 4 image": "assets/q4.png"
}

placeholderstr = "Please input your command"
user_name = "perfectzynogre"
user_image = "https://www.w3schools.com/howto/img_avatar.png"

def stream_data(stream_str):
    for word in stream_str.split(" "):
        yield word + " "
        time.sleep(0.15)

def main():
    st.set_page_config(
        page_title='K-Assistant - The Residemy Agent',
        layout='wide',
        initial_sidebar_state='auto',
        menu_items={
            'Get Help': 'https://streamlit.io/',
            'Report a bug': 'https://github.com',
            'About': 'About your application: **Hello world**'
            },
        page_icon="img/favicon.ico"
    )

    # Show title and description.
    st.title(f"💬 {user_name}'s Chatbot")

    with st.sidebar:
        selected_lang = st.selectbox("Language", ["English", "繁體中文"], index=1)
        if 'lang_setting' in st.session_state:
            lang_setting = st.session_state['lang_setting']
        else:
            lang_setting = selected_lang
            st.session_state['lang_setting'] = lang_setting

        st_c_1 = st.container(border=True)
        with st_c_1:
            st.image("https://www.w3schools.com/howto/img_avatar.png")

    st_c_chat = st.container(border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            if user_image:
                st_c_chat.chat_message(msg["role"], avatar=user_image).markdown(msg["content"])
            else:
                st_c_chat.chat_message(msg["role"]).markdown(msg["content"])
        elif msg["role"] == "assistant":
            st_c_chat.chat_message(msg["role"]).markdown(msg["content"])
        else:
            try:
                image_tmp = msg.get("image")
                if image_tmp:
                    st_c_chat.chat_message(msg["role"], avatar=image_tmp).markdown(msg["content"])
            except:
                st_c_chat.chat_message(msg["role"]).markdown(msg["content"])

    def generate_response(prompt):
        # Check for specific image requests based on the prompt
        for key in images:
            if f"show {key}" in prompt.lower():
                image_url = images[key]
                return f"Here is the image you requested: ![image]({image_url})"
        
        # Check if the user greets the chatbot (say hello)
        greetings = ["hello", "hi", "hey", "greetings", "howdy"]
        if any(greet in prompt.lower() for greet in greetings):
            return (
                "Hello! I'm here to assist you. Type one of these prompts to show an image:\n\n"
                "- Please show question 1 2d image\n"
                "- Please show question 1 3d image\n"
                "- Please show question 2 image\n"
                "- Please show question 3 image"
            )

        # Default response if no image request or greeting detected
        return f"You say: {prompt}"

    # Chat function section (timing included inside function)
    def chat(prompt: str):
        st_c_chat.chat_message("user", avatar=user_image).write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # If the response contains an image link, render the image
        if "![image]" in response:
            image_url = response.split("](")[1][:-1]  # Extract URL from markdown
            st_c_chat.chat_message("assistant").image(image_url, caption="Requested Image", use_container_width=True)
        else:
            st_c_chat.chat_message("assistant").write_stream(stream_data(response))

    if prompt := st.chat_input(placeholder=placeholderstr, key="chat_bot"):
        chat(prompt)

if __name__ == "__main__":
    main()
