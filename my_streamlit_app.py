import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# Désactiver l'avertissement Matplotlib
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Cars')
df = pd.read_csv("https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv")

# Obtenez la liste complète des continents disponibles
all_continents = df['continent'].unique()

# Ajouter des boutons pour filtrer par continent avec tous les continents sélectionnés par défaut
st.sidebar.header('Filtrer par continent')
continents = st.sidebar.multiselect('Sélectionner les continents:', all_continents, default=all_continents)

# Appliquer le filtre à l'ensemble du DataFrame
filtered_df = df[df['continent'].isin(continents) if continents else True]

# Afficher le DataFrame filtré
st.subheader('Résultats filtrés')
st.write(filtered_df)

# Afficher la heatmap de corrélation avec Plotly pour le DataFrame filtré
st.subheader('Analyse de corrélation avec Plotly')
correlation_matrix_filtered = filtered_df.select_dtypes(include='number').corr()

# Créer la heatmap avec annotations
fig_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix_filtered.values,
    x=correlation_matrix_filtered.columns,
    y=correlation_matrix_filtered.columns,
    colorscale='icefire',  # Utiliser l'échelle 'icefire'
    hoverongaps=False,
    hovertemplate="Variable x: %{x}<br>Variable y: %{y}<br>Corrélation: %{z}<extra></extra>",
))

fig_corr.update_layout(title='Heatmap de Corrélation')

# Afficher le graphique
st.plotly_chart(fig_corr)

# Afficher des graphiques de distribution pour certaines variables avec Plotly pour le DataFrame filtré
st.subheader('Analyse de distribution')
selected_variable = st.selectbox('Sélectionner une variable:', filtered_df.columns)
fig_dist = px.histogram(filtered_df, x=selected_variable, nbins=50, title=f'Distribution de {selected_variable}')
st.plotly_chart(fig_dist)