import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def read_data( filename ):
    return pd.read_csv(filename , index_col = 0)

if __name__ == "__main__":


    import sys
    import argparse

    parser = argparse.ArgumentParser(
                description="""relaxes points plotted on a sphere""")
    parser.add_argument('-i','--input-prefix', type=str, required=True,
             help='''input points prefix (the script will look for files <input-prefix>_round<roundNumber>.csv).
              * Expects 3 columns that should be named x, y, and z, and an index column.
              ''')
    parser.add_argument('-o','--output-file', type=str, required=True,
             help='''name of the html output file for the plot.''')

    parser.add_argument('-a', type=int, default=1,
             help='round to start plotting from.')
    parser.add_argument('-b', type=int,
             help='round to plot to.')


    args = parser.parse_args()
    input_prefix = args.input_prefix

    print("detecting steps")
    rounds_to_plot = []

    for i in range( args.a , args.b + 1 ):
        filename = f"{input_prefix}_round{i}.csv"
        if os.path.exists( filename ):
            rounds_to_plot.append(i)

    print(f"detected {len(rounds_to_plot)} rounds to plot")
    print(rounds_to_plot)

    fig = go.Figure()

    # Add traces, one for each slider step
    for step in range(len(rounds_to_plot)):
        
        filename = f"{input_prefix}_round{rounds_to_plot[step]}.csv"

        tmp = read_data( filename )# Create figure
        
        fig.add_trace(
            go.Scatter3d(
                visible=False,
                x = tmp.x , 
                y = tmp.y , 
                z = tmp.z , 
                mode='markers',
                text = list( tmp.index )
            )
        )

    # Make 10th trace visible
    fig.data[0].visible = True

    # Create and add slider
    steps = []
    for i in range(len(rounds_to_plot)):

        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": "Round: " + str( rounds_to_plot[i] )}],  # layout attribute
            label = str(i)
        )
        
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)


    sliders = [dict(
        active=0,
        currentvalue={"prefix": "iteration: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
    )

    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=4, range=[-1,1],),
            yaxis = dict(nticks=4, range=[-1, 1],),
            zaxis = dict(nticks=4, range=[-1, 1],),
            aspectmode='cube'),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10),
        )

    #fig.show()
    fig.write_html( args.output_file )
    fig