import streamlit as st

def main():
    st.title("2D Word Embedding Visualization")

    # Show the uploaded PNG
    st.image("assets/q1_2d.png", caption="2D Visualization of Word Embeddings", use_container_width=True)

if __name__ == "__main__":
    main()
