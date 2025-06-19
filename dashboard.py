import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import os

# Load data
csv_file = 'PROPERTYVALUATIONS.csv'
df = pd.read_csv(csv_file)

# ... existing code ... 