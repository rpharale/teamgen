import streamlit as st
from pathlib import Path

RULE_BOOK_PATH = "./data/rules.md"

def read_markdown_file(file_path):
    return Path(file_path).read_text()

class RuleBook:
    class Model:
        pageTitle = ""

    def view(self, model):
        st.title(model.pageTitle)

        markdown_text = read_markdown_file(RULE_BOOK_PATH)
        st.markdown(markdown_text, unsafe_allow_html=True)