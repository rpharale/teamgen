import streamlit as st


class RuleBook:
    class Model:
        pageTitle = "Rule Book"

    def view(self, model):
        st.title(model.pageTitle)