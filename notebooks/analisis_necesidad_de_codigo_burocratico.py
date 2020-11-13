import numpy as np
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("../data/original/Entrenamiento.csv")
df = df[['Bureaucratic_Code_0_Approval','Bureaucratic_Code_0_Approved','Stage']]

conditionlist = [
    (df['Bureaucratic_Code_0_Approval'] == 1) & (df['Bureaucratic_Code_0_Approved'] == 1),
    (df['Bureaucratic_Code_0_Approval'] == 1) & (df['Bureaucratic_Code_0_Approved'] == 0),
    (df['Bureaucratic_Code_0_Approval'] == 0) & (df['Bureaucratic_Code_0_Approved'] == 1),
    (df['Bureaucratic_Code_0_Approval'] == 0) & (df['Bureaucratic_Code_0_Approved'] == 0)]
choicelist = [1, 2, 3, 4]
df['estado1'] = np.select(conditionlist, choicelist, default='Not Specified')

conditionlist = [
    (df['Bureaucratic_Code_0_Approved'] == 1) & (df['Stage'] == 'Closed Won'),
    (df['Bureaucratic_Code_0_Approved'] == 1) & (df['Stage'] == 'Closed Lost'),
    (df['Bureaucratic_Code_0_Approved'] == 0) & (df['Stage'] == 'Closed Won'),
    (df['Bureaucratic_Code_0_Approved'] == 0) & (df['Stage'] == 'Closed Lost')]
choicelist = [5, 6, 7, 8]
df['estado2'] = np.select(conditionlist, choicelist, default='Not Specified')

e1 = df['estado1'].value_counts().values
e2 = df['estado2'].value_counts().values
values = np.concatenate((e1, e2), axis=None).tolist()

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["necesita codigo burocratico", "no necesita codigo burocratico", "obtuvo codigo burocratico", "no obtuvo burocratico", "oportunidad ganada", "oportunidad perdida"],
      color = "blue"
    ),
    link = dict(
      source = [0, 0, 1, 2, 2, 3, 3], # indices correspond to labels, eg A1, A2, A2, B1, ...
      target = [2, 3, 3, 4, 5, 4, 5],
      value = values
  ))])

fig.update_layout(
    title={
        'text': "Analisis de necesidad de codigo burocratico",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()