import numpy as np
import pandas as pd
import plotly.graph_objects as go

d = {'Who': ['A', 'B', 'C', 'D', 'E', 'F'],
     'Pants on Fire': [9,7,6,4, 2, 1],
     'False': [7, 6, 4, 5, 2,1],
     'Mostly False': [5, 4, 6,4, 2, 6],
     'Half True' : [4,2,5,6,3, 2],
     'Mostly True': [5,3,2,3,4,3],
    # ' True': [2,4,3,6, 6, 8]}
     }
df = pd.DataFrame(d)

fig = go.Figure()
for col in df.columns[1:3]:
    fig.add_trace(go.Bar(x=-df[col].values,
                         y=df['Who'],
                         orientation='h',
                         name=col,
                         customdata=df[col],
                         hovertemplate = "%{y}: %{customdata}"))
for col in df.columns[3:]:
    fig.add_trace(go.Bar(x= df[col],
                         y =df['Who'],
                         orientation='h',
                         name= col,
                         hovertemplate="%{y}: %{x}"))

fig.update_layout(barmode='relative',
                  height=400,
                  width=700,
                  yaxis_autorange='reversed',
                  bargap=0.01,
                  legend_orientation ='h',
                  legend_x=-0.05, legend_y=1.1
                 )
fig.show()