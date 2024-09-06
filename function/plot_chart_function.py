import streamlit
from plotly import graph_objects as go
import random
import pandas as pd

def create_stacked_bar_chart(data, title = None,bar_col = None, color_mapping = None, line_col=None, barmode='relative',legend=False, line_axis ='y2'):

            currency = data['reportedCurrency'].iloc[0]

            def get_random_color():
                return f'#{random.randint(0, 0xFFFFFF):06x}'
            fig = go.Figure()
            if bar_col is not None:
              bar_col = bar_col[::-1]
              for col in bar_col:
                  fig.add_trace(go.Bar(
                      x=data.index,
                      y=data[col],
                      name=col,

                      marker_color=color_mapping.get(col, get_random_color()) if color_mapping else get_random_color(),
                      hoverinfo='y+name'  # Display both value and name on hover
                  ))

            # Add line plot if line data is provided
            if line_col is not None :

                for line in line_col :
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data[line],
                        mode='lines+markers',
                        name=line,
                        line=dict( width=2),
                        marker=dict( size=8),
                        hoverinfo='y+name',
                        yaxis=line_axis
                    ))

            # Update layout
            fig.update_layout(
                barmode=barmode,  # Stacking bars on top of each other
                title=title,
                xaxis=dict(title='Year',
                            showticklabels=True ),
                yaxis=dict(title=f'Amount {currency}'),
                legend=dict(
                    x=0,
                    y=-0.2,  # Adjust this value to move the legend further below
                    traceorder='normal',
                    orientation='h',
                    visible=legend
                ),
                height=400,
                margin=dict(l=10, r=10, t=30, b=10),
                yaxis2=dict(
                    title=None,
                    overlaying='y',
                    side='right'),


            )
            return fig