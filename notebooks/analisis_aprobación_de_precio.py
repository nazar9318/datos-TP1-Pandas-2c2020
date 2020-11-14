import numpy as np
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("../data/original/Entrenamiento.csv")
df = df[(df['Stage']!='Proposal') & (df['Stage']!='Negotiation') & (df['Stage']!='Qualification')]
df = df[['Pricing, Delivery_Terms_Quote_Appr','Pricing, Delivery_Terms_Approved','Stage']]

conditionlist = [
    (df['Pricing, Delivery_Terms_Quote_Appr'] == 1) & (df['Pricing, Delivery_Terms_Approved'] == 1),
    (df['Pricing, Delivery_Terms_Quote_Appr'] == 1) & (df['Pricing, Delivery_Terms_Approved'] == 0),
    (df['Pricing, Delivery_Terms_Quote_Appr'] == 0) & (df['Pricing, Delivery_Terms_Approved'] == 1),
    (df['Pricing, Delivery_Terms_Quote_Appr'] == 0) & (df['Pricing, Delivery_Terms_Approved'] == 0)]
choicelist = [1, 2, 3, 4]

df['estado1'] = np.select(conditionlist, choicelist, default='Not Specified')

conditionlist = [
    (df['Pricing, Delivery_Terms_Approved'] == 1) & (df['Stage'] == 'Closed Won'),
    (df['Pricing, Delivery_Terms_Approved'] == 1) & (df['Stage'] == 'Closed Lost'),
    (df['Pricing, Delivery_Terms_Approved'] == 0) & (df['Stage'] == 'Closed Won'),
    (df['Pricing, Delivery_Terms_Approved'] == 0) & (df['Stage'] == 'Closed Lost')]
choicelist = [5, 6, 7, 8]

df['estado2'] = np.select(conditionlist, choicelist, default=8)

e1 = df['estado1'].value_counts().sort_index().values
e2 = df['estado2'].value_counts().sort_index().values

e1 = e1/e1.sum()*100
e2 = e2/e2.sum()*100

values = np.concatenate((e1, e2), axis=None).tolist()


fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["necesita aprobación", "no necesita aprobación", "obtuvo aprobación", "no obtuvo aprobación", "oportunidad ganada", "oportunidad perdida"],
      color = "blue"
    ),
    link = dict(
      source = [0, 0, 1, 2, 2, 3, 3], # indices correspond to labels, eg A1, A2, A2, B1, ...
      target = [2, 3, 3, 4, 5, 4, 5],
      #value = [9890, 3803, 3254, 6404, 3971, 3443, 3129]
      value = values
  ))])

fig.update_layout(
    title={
        'text': "Analisis de aprobación de precio total de oportunidades",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()