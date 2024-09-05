import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Growth of R&D Expenditures", layout="wide")

file_path = 'nsf24308-tab021.xlsx'
data = pd.read_excel(file_path)

data = data.dropna(subset=['Rank']) 
data['Rank'] = data['Rank'].astype(int)  

min_rank = data['Rank'].min()
max_rank = data['Rank'].max()

st.title('Growth of R&D Expenditures in Universities (2010-2022)')

selected_rank_range = st.slider('Select Rank Range', min_rank, max_rank, (1, 10))

selected_min_rank, selected_max_rank = selected_rank_range
filtered_data = data[(data['Rank'] >= selected_min_rank) & (data['Rank'] <= selected_max_rank)]

institutions = filtered_data['Institution']
years = list(map(str, range(2010, 2023)))

fig = go.Figure()

for i, institution in enumerate(institutions):
    fig.add_trace(go.Scatter(
        x=years,
        y=filtered_data.iloc[i, 2:],
        mode='lines+markers',
        name=f"{institution} (Rank: {filtered_data.iloc[i]['Rank']})",
        line=dict(width=1)
    ))

odu_evms_data = data.loc[data['Institution'].isin(['Old Dominion U.', 'Eastern Virginia Medical School'])].iloc[:, 2:]
odu_evms_sum = odu_evms_data.sum()

fig.add_trace(go.Scatter(
    x=years,
    y=odu_evms_sum,
    mode='lines+markers',
    name='ODU + EVMS Sum',
    line=dict(width=2, dash='dash', color='red')
))

odu_data = data.loc[data['Institution'] == 'Old Dominion U.'].iloc[:, 2:]

fig.add_trace(go.Scatter(
    x=years,
    y=odu_data.values.flatten(), 
    mode='lines+markers',
    name='Old Dominion U.',
    line=dict(width=2, dash='dot', color='blue')  
))

fig.update_layout(
    title='Growth of R&D Expenditures in Universities (2010-2022)',
    xaxis_title='Year',
    yaxis_title='R&D Expenditures (in thousands)',
    xaxis=dict(tickmode='linear', tick0=2010, dtick=1),
    hovermode='closest',
    template='plotly_white',
    height=600
)

st.plotly_chart(fig, use_container_width=True)
