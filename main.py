import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


def main():
    st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")

    st.subheader("LinkedIn Post Generator: Codebasics")

    fs = FewShotPosts()
    tags = fs.get_tags()

    # Handle empty tags safely
    if not tags:
        st.error("No tags found. Check your few_shot data.")
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    if st.button("Generate"):
        with st.spinner("Generating post..."):
            try:
                post = generate_post(
                    selected_length,
                    selected_language,
                    selected_tag
                )

                st.success("Generated Post:")
                st.write(post)

            except Exception as e:
                st.error(f"Error generating post: {str(e)}")


if __name__ == "__main__":
    main()