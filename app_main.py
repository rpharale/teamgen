import streamlit as st
from streamlit_option_menu import option_menu
from tools.utils import load_css
from views.team_maker import TeamMaker
from views.rule_book import RuleBook
from views.settings import Settings
from lib.authenticate import check_password

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

class TeamMakerApp:
    def __init__(self):
        self.menuItem = None
        self.model = None

    def run(self):
        if self.menuItem == self.model.option1:
            TeamMaker().view(TeamMaker.Model())

        if self.menuItem == self.model.option2:
            RuleBook().view(RuleBook.Model())

        if self.menuItem == self.model.option3:
            Settings().view(Settings.Model())

    def view(self, model):
        with st.sidebar:
            self.menuItem = option_menu(model.menuTitle,
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
            st.text("Version: 0.0.2")
            logout = st.button("Logout")
            st.markdown("---")
            st.markdown("TeamMaker is a platform that provides access to all types of tools, resources " + \
                        "and features that can help you increase the performance of your players. This app allows " + \
                        "you to create teams and assign them with specific roles within the game. Besides, it keeps " + \
                        "track of all the rules of your team for easy communication and plays.")
        
        self.model = model
        if logout:
            # New user must be reauthenticated
            st.session_state["password_correct"] = False
        
        if check_password():
            self.run()
        

if __name__ == '__main__':
    app = TeamMakerApp()
    app.view(Model())