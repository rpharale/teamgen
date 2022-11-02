import streamlit as st
from tools.utils import load_css
from streamlit_option_menu import option_menu
from views.team_maker import TeamMaker
from views.rule_book import RuleBook
from views.settings import Settings

st.set_page_config(
    page_title="TeamMaker",
    #page_icon="favicon.ico",
    layout="wide"
)

load_css()

class Model:
    menuTitle = "Main Menu"
    option1 = "Team Maker"
    option2 = "Rule Book"
    option3 = "Settings"

    menuIcon = "menu-up"
    icon1 = "house"
    icon2 = "list-task"
    icon3 = "gear"

def view(model):
    with st.sidebar:
        menuItem = option_menu(model.menuTitle,
                               [model.option1, model.option2, model.option3],
                               icons=[model.icon1, model.icon2, model.icon3],
                               menu_icon=model.menuIcon,
                               default_index=0,
                               styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "20px"},
                                   "nav-link": {"font-size": "12px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#037ffc"},
                               })

    with st.sidebar:
        st.markdown("---")
        st.text("User: Admin")
        st.text("Version: 0.0.1")
        st.button("Logout")
        st.markdown("---")
        st.markdown("TeamMaker is a platform that provides access to all types of tools, resources " + \
                    "and features that can help you increase the performance of your players. This app allows " + \
                    "you to create teams and assign them with specific roles within the game. Besides, it keeps " + \
                    "track of all the rules of your team for easy communication and plays.")
    
    if menuItem == model.option1:
        TeamMaker().view(TeamMaker.Model())

    if menuItem == model.option2:
        RuleBook().view(RuleBook.Model())

    if menuItem == model.option3:
        Settings().view(Settings.Model())

if __name__ == '__main__':
    view(Model())