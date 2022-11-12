import streamlit as st
import pandas as pd
import requests
import io

PLAYERS_INFO_CSV_URL = "https://raw.githubusercontent.com/rpharale/data/main/misc/players.csv"

#@st.cache
def get_players_stat():
    print("Fetching content")
    s = requests.get(PLAYERS_INFO_CSV_URL).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    return df

def create_teams(df, players_available):
    if not players_available:
        return [], []
    team_a = []
    team_b = []
    team_a_score, team_b_score = 0, 0
    team_a_scores, team_b_scores = [], []
    players_to_scores_map = dict(zip(df.PlayerName, df.TotalScore))
    # Keep only the available players in the dict
    players_to_scores_map = {k: v for k,v in players_to_scores_map.items() if k in players_available}
    # Sort the players as per their scores
    players_to_scores_map = dict(sorted(players_to_scores_map.items(), key=lambda item: item[1], reverse=True))
    max_players_per_team = len(players_available) // 2
    for p, s in players_to_scores_map.items():
        # If any team has reached the max limit, stop adding to that team.
        if (len(team_a) == max_players_per_team):
            team_b.append(p)
            team_b_score += s
            team_b_scores.append(s)
        elif (len(team_b) == max_players_per_team):
            team_a.append(p)
            team_a_score += s
            team_a_scores.append(s)
        elif (team_a_score < team_b_score):
            team_a.append(p)
            team_a_score += s
            team_a_scores.append(s)
        else:
            team_b.append(p)
            team_b_score += s
            team_b_scores.append(s)
        
    
    # Handle the case of odd players
    if len(team_a) > len(team_b):
        team_b = team_b + team_a[-1:]
        team_b_scores = team_b_scores + team_a_scores[-1:]
    elif len(team_a) < len(team_b):
        team_a = team_a + team_b[-1:]
        team_a_scores = team_a_scores + team_b_scores[-1:]
    
    return team_a, team_b, team_a_scores, team_b_scores


class TeamMaker:
    class Model:
        pageTitle = "MG Cricket League"

    def __init__(self):
        #self.players_available = set()
        self.df = None
        self.batting_weight = 0.4
        self.bowling_weight = 0.4
        self.fielding_weight = 0.2
        self.output_container = None

    def form_callback(self):
        self.players_available = set()
        for idx, row in self.df.iterrows():
            player_name = row['PlayerName']
            val = st.session_state[f"{player_name}"]
            if val:
                self.players_available.add(player_name)
            #st.write(f"{player_name}={val}")
        #st.write(self.players_available)
        #for item in self.players_available:
        #    print(f"{item}")

    def view(self, model):
        st.title(model.pageTitle)
        
        # Read the players info
        self.df = get_players_stat()

        with st.form(key="TeamMaker"):
            col1, col2, _ = st.columns([30, 30, 40])

            with col1:
                for idx, row in self.df.iterrows():
                    st.checkbox(label=row['PlayerName'], key=f"{row['PlayerName']}", \
                                      value=False)

            with col2:
                self.batting_weight = st.number_input(label="Batting Weight", min_value=0.0, \
                                                      max_value=1.0, value=self.batting_weight)

                self.bowling_weight = st.number_input(label="Bowling Weight", min_value=0.0, \
                                                      max_value=1.0, value=self.bowling_weight)

                self.fielding_weight = st.number_input(label="Fielding Weight", min_value=0.0, \
                                                      max_value=1.0, value=self.fielding_weight)

                st.slider(label="Randomness", min_value=0.0, max_value=1.0)

            col1, _ = st.columns([10, 90])
            with col1:
                self.submit_button = st.form_submit_button("Submit")#, on_click=self.form_callback)
        
        self.form_callback()
        self.output_container = st.container()

        #Error checks
        if abs(self.batting_weight + self.bowling_weight + self.fielding_weight - 1.0) > 1e-6:
            st.error("Batting weight, Bowling weight and Fielding weight should sum to 1.0")
        
        # Calculate the aggregate scores
        self.df['TotalScore'] = self.df["BattingScore"] * self.batting_weight + self.df["BowlingScore"] * \
            self.bowling_weight + self.df['FieldingScore'] * self.fielding_weight
        
        if self.submit_button:
            team_a, team_b, team_a_scores, team_b_scores = create_teams(self.df, self.players_available)
            with self.output_container:
                col1, col2, _ = st.columns([15, 15, 70])

                with col1:
                    df_out_team_a = pd.DataFrame(team_a, columns=['Team A'])
                    styler = df_out_team_a.style.hide(axis='index')
                    st.write(styler.to_html(), unsafe_allow_html=True)
                
                with col2:
                    df_out_team_b = pd.DataFrame(team_b, columns=['Team B'])
                    styler = df_out_team_b.style.hide(axis='index')
                    st.write(styler.to_html(), unsafe_allow_html=True)
                
                st.write("")
                
            with st.expander("Stats"):
                col1, _ = st.columns([50, 50])
                total_score_map = dict(zip(self.df.PlayerName, self.df.TotalScore))
                team_a_score = sum([v for k, v in total_score_map.items() if k in team_a])
                team_b_score = sum([v for k, v in total_score_map.items() if k in team_b])
                with col1:
                    st.write(f"Avg score of Team A: {team_a_score / len(team_a):.2f}")
                    st.write(f"Avg score of Team b: {team_b_score / len(team_b):.2f}")
            
            if st.session_state["user_name"] == "admin":
                with st.expander("Scores"):
                    col1, col2, _ = st.columns([30, 30, 40])

                    with col1:
                        df_out_team_a['Scores'] = team_a_scores
                        styler = df_out_team_a.style.hide(axis='index')
                        st.write(styler.to_html(), unsafe_allow_html=True)

                    with col2:
                        df_out_team_b['Scores'] = team_b_scores
                        styler = df_out_team_b.style.hide(axis='index')
                        st.write(styler.to_html(), unsafe_allow_html=True)
                    
                    st.markdown("&nbsp;")
                    st.markdown("### Detail scores of all the players")
                    col1, _ = st.columns([99, 1])
                    with col1:
                        st.dataframe(self.df)
