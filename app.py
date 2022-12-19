import streamlit as st
from futsal.parser import parse_positions_table, index_position
from futsal.data import get_positions_table

from futsal.team import HomeTeam

st.set_page_config(page_title='Habaneros F.C.',
                   page_icon="🌶️",
                   layout='centered',
                   initial_sidebar_state='auto')

_, head, _ = st.columns([2, 8, 2])
# icon.header("🌶️")
head.header('🌶️🌶️🌶️ Habaneros F.C. 🌶️🌶️🌶️')

st.markdown("""
<style>
/* Style containers */
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    border-radius: 15px;
    padding: 15px 15px 100px 10px;
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    background-color: #FFFFFF;
</style>
""",
            unsafe_allow_html=True)


#team_name = st.selectbox("Select your team", ['Habaneros F.C.'])

team_name = 'Habaneros F.C.'

# @st.cache
# def load_hometeam():

hometeam = HomeTeam(team_name,
                    st.secrets['FIXTURES_URL']).foresight()

# return

# load_hometeam()

st.markdown(f"""
## _Upcoming games..._
""")


for team in hometeam:

    position = index_position(team['Opponent']['name'])

    div = st.container()

    div.markdown(f"""
    ### {team['Opponent']['name']} ({position})
    """)



    info, stats = div.columns(2)

    #     info.write(f"""
    # Hey guys! {team['Date']}'s game is at {team['Time']}.
    # Please “👍🏼” to confirm you will play tomorrow.
    # See you there!
    # """)
    info.markdown(f"""
    ### {team['Time']}
    #### {" ".join(team['Date'].split()[1:-1])}
    """)
