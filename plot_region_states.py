import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as ply
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import sm

# Read from file
print('Reading data...')
data = pd.read_pickle(r'modified\Emission_Regions.pkl')

if not os.path.exists(r'out\States'):
    os.makedirs(r'out\States')

for state in sm.state_to_region:
    print(f'\nBeginning processing for {state}...')
    areas = [state, sm.state_to_region[state], 'U.S. Total']
    data_sel = data.loc[data['Census Division and State'].isin(areas), :]

    print('Pivoting...')
    d_co2 = data_sel.pivot(columns='Census Division and State', values='Carbon Dioxide (CO2) (Thousand Metric Tons)')
    d_co2 /= d_co2.iloc[0]
    d_generation = data_sel.pivot(columns='Census Division and State', values='Generation (Thousand Megawatthours)')
    d_generation /= d_generation.iloc[0]
    d_intensity = data_sel.pivot(columns='Census Division and State', values='Kilograms of CO2 per Megawatthour of Generation')

    print('Final data shaping...')
    layout = go.Layout(hovermode='closest')

    fig = make_subplots(rows=1, cols=3, subplot_titles = ('CO2 (% 2013 value)', 'Generation (% 2013 value)', 'Intensity (kg/MWh)'))
    fig.update_yaxes(tickformat='.1%', row=1, col=1)
    fig.update_yaxes(tickformat='.1%', row=1, col=2, matches='y')

    colors = {
        state: 'red',
        areas[1]: 'purple',
        areas[2]: 'blue',
        }

    for col in areas:
        fig.add_trace(go.Scatter(name=col,
                                 x=d_co2.index,
                                 y=d_co2[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 line={'color': colors[col]}),
                       row=1,
                       col=1)
        
        fig.add_trace(go.Scatter(name=col,
                                 x=d_generation.index,
                                 y=d_generation[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 showlegend=False,
                                 line={'color': colors[col]}),
                       row=1,
                       col=2)

        fig.add_trace(go.Scatter(name=col,
                                 x=d_intensity.index,
                                 y=d_intensity[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 showlegend=False,
                                 line={'color': colors[col]}),
                       row=1,
                       col=3)

    print('Creating plot...')
    ply.plot(fig, filename=f'out\\States\\{state}.html', auto_open=False)
    print('Plot created!')

