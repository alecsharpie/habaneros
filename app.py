import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from futsal.parser import index_position

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
### _Upcoming games..._
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

    stats.markdown(f"""game history""")

    df = team['Opponent']['history']

    df = df.reset_index().set_index('DateTime')

    # print(df)

    df = df.resample('H').interpolate()

    print(df)

    # fig = px.scatter(
    #     df,
    #     x=df.index,
    #     y="Diff",
    #     color='Diff',
    #     colorscale = [[0, 'rgba(214, 39, 40, 0.85)'],
    #            [0.142, 'rgba(255, 255, 255, 0.85)'],
    #            [1, 'rgba(6,54,21, 0.85)']],
    #     hover_name=df['Team'],
    #     labels={
    #         "Diff": "Goal Difference",
    #         "x": "Date"
    #     },
    # )

    df_points  = df[~df['Result'].isnull()]

    print(df_points)

    # fig.add_scatter(
    #     x=df_points.index,
    #     y=df_points.Diff,
    #     fill=df_points.Diff,
    #     color_continuous_scale='Turbo',
    #     hover_name=df_points['Team'],
    #     labels={
    #         "Diff": "Goal Difference",
    #         "x": "Date"
    #     },
    # )


    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.Diff,
            hoverinfo='all',
            #    labels={
            #        "Diff": "Goal Difference",
            #        "x": "Date"
            #    },
            mode='markers',
            name='markers',
            marker=dict(size=4,
                        color=df.Diff,
                        colorscale=[[0, 'rgba(32, 103, 172, 0.85)'],
                                    [0.2, 'rgba(255, 255, 201, 0.85)'],
                                    [1, 'rgba(223, 84, 74, 0.85)']],
                        showscale=True)))


    # fig.add_trace(go.Scatter(x=random_x, y=random_y2,
    #                     mode='lines',
    #                     name='lines'))


    fig.update_layout(height=300,
    yaxis_range=[-10,10],
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)")

    stats.plotly_chart(fig, theme=None, use_container_width=True)
