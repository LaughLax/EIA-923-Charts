import os
import pandas as pd
import plotly.offline as ply
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import sm

# Read from file
print('Reading data...')
data = pd.read_pickle(r'modified\Emission_Regions.pkl')

my_colors = ['black', 'gray', 'purple', 'cyan', 'fuchsia', 'teal', 'red', 'green', 'orange', 'blue', 'darkkhaki']

if not os.path.exists(r'out\Regions'):
    os.makedirs(r'out\Regions')

for reg in sm.region_to_states:
    print(f'\nBeginning processing for {reg}...')
    areas = ['U.S. Total', reg] + sm.region_to_states[reg]
    data_sel = data.loc[data['Census Division and State'].isin(areas), :]

    print('Pivoting...')
    d_co2 = data_sel.pivot(columns='Census Division and State', values='Carbon Dioxide (CO2) (Thousand Metric Tons)')
    d_co2 /= d_co2.iloc[0]
    d_generation = data_sel.pivot(columns='Census Division and State', values='Generation (Thousand Megawatthours)')
    d_generation /= d_generation.iloc[0]
    d_intensity = data_sel.pivot(columns='Census Division and State', values='Kilograms of CO2 per Megawatthour of Generation')
    d_intensity2 = d_intensity / d_intensity.iloc[0]

    print('Final data shaping...')
    layout = go.Layout(hovermode='closest')

    fig = make_subplots(rows=1, cols=4, subplot_titles = ('CO2 (% 2013 value)', 'Generation (% 2013 value)', 'Intensity (% 2013 value)', 'Intensity (kg/MWh)'))
    fig.update_yaxes(tickformat='.1%', row=1, col=1)
    fig.update_yaxes(tickformat='.1%', row=1, col=2, matches='y')
    fig.update_yaxes(tickformat='.1%', row=1, col=3, matches='y')

    for i, col in enumerate(areas):
        color = my_colors[i]
        fig.add_trace(go.Scatter(name=col,
                                 x=d_co2.index,
                                 y=d_co2[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 line={'color': color}),
                       row=1,
                       col=1)
        
        fig.add_trace(go.Scatter(name=col,
                                 x=d_generation.index,
                                 y=d_generation[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 showlegend=False,
                                 line={'color': color}),
                       row=1,
                       col=2)

        fig.add_trace(go.Scatter(name=col,
                                 x=d_intensity2.index,
                                 y=d_intensity2[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 showlegend=False,
                                 line={'color': color}),
                       row=1,
                       col=3)

        fig.add_trace(go.Scatter(name=col,
                                 x=d_intensity.index,
                                 y=d_intensity[col],
                                 hoverinfo='text+x+y',
                                 text=col,
                                 legendgroup=col,
                                 showlegend=False,
                                 line={'color': color}),
                       row=1,
                       col=4)
        
    print('Creating plot...')
    ply.plot(fig, filename=f'out\\Regions\\{reg}.html', auto_open=False)
    print('Plot created!')

