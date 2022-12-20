import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os

from futsal.parser import index_position

from futsal.team import HomeTeam

st.set_page_config(page_title='Habaneros F.C.',
                   page_icon="🌶️",
                   layout='centered',
                   initial_sidebar_state='auto')

_, head, _ = st.columns([2, 8, 2])

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


def hide_anchor_link():
    st.markdown("""
        <style>
        .css-mi9erm {display: none}
        </style>
        """,
                unsafe_allow_html=True)


hide_anchor_link()


#team_name = st.selectbox("Select your team", ['Habaneros F.C.'])

team_name = 'Habaneros F.C.'


hometeam = HomeTeam(team_name,
                    os.environ['FIXTURES_URL']).foresight()


st.markdown(f"""
### _Upcoming games..._
""")

for team in hometeam:

    position = index_position(team['Opponent']['name'])

    div = st.container()

    div.markdown(f"""
    ## {team['Time']} - {" ".join(team['Date'].split()[1:-1])}
    """)

    div.markdown(f"""
    ### {team['Opponent']['name']} ({position})
    """)

    div.markdown(f"""Opponents past games""")

    df = team['Opponent']['history'].reset_index()

    df['Result_Code'] = df['Result'].apply(lambda x: x[0])

    df['DateTime'] = pd.to_datetime(df.DateTime)

    df = df.set_index('DateTime')

    reindexed_df = df.reindex(
        pd.date_range(start=df.index.min(), end=df.index.max(), freq='40T'))

    interpolated_df = reindexed_df[['Result_Code', 'Diff']]

    interpolated_df['Diff'] = interpolated_df['Diff'].interpolate(
        method='linear', axis=0)

    interpolated_df = interpolated_df.fillna('')

    zero_point = abs(0 - df.Diff.min() /
                     (df.Diff.max() - df.Diff.min()))

    zero_point = np.clip(zero_point, 0, 1)

    # Create plot showing goal diff history
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=interpolated_df.index,
            y=interpolated_df.Diff,
            text=interpolated_df.Result_Code,
            textposition="top center",
            hoverinfo='skip',
            mode='markers+text',
            name='Markers & Text',
            marker=dict(size=4,
                        color=interpolated_df.Diff,
                        colorscale=[[0, 'rgba(32, 103, 172, 0.85)'],
                                    [zero_point, 'rgba(255, 255, 201, 0.85)'],
                                    [1, 'rgba(223, 84, 74, 0.85)']],
                        showscale=True)))


    # fig.add_trace(
    #     go.Scatter(
    #         x=df.index,
    #         y=df.Diff,
    #         text = df.Result,
    #         hoverinfo='all',
    #         #    labels={
    #         #        "Diff": "Goal Difference",
    #         #        "x": "Date"
    #         #    },
    #         mode='lines',
    #         name='lines',
    #         marker=dict(size=10,
    #                     color=df.Diff,
    #                     colorscale=[[0, 'rgba(32, 103, 172, 0.85)'],
    #                                 [zero_point, 'rgba(255, 255, 201, 0.85)'],
    #                                 [1, 'rgba(223, 84, 74, 0.85)']],
    #                     showscale=True)))


    fig.update_layout(height=300,
                      xaxis_title="Date",
                      yaxis_title="Goal Difference",
                      yaxis_range=[-10, 10],
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)")

    div.plotly_chart(fig, theme=None, use_container_width=True)
