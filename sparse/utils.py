"""
Utility functions used in the sparse package.
"""

import plotly.graph_objects as go
import numpy as np


def show_plot(x, y, title=None, x_title=None, y_title=None):
    """
    Plotly wrapper.
    """
    fig = go.Figure()

    # add reference spectrum
    fig.add_trace(
        go.Scatter(
            x=np.squeeze(x),
            y=np.squeeze(y),
            mode='lines',
            name=('Data')
        )
    )

    fig.update_layout(
        title="Spectral Data",
        xaxis_title="Wavelength (nm)"
    )
    fig.show()
