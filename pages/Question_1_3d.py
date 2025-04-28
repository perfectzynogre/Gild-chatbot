import streamlit as st
import numpy as np
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

# Sample sentences
sentences = [
    "The Indonesian government has announced a comprehensive plan to accelerate infrastructure development in rural areas, focusing on improving transportation networks, healthcare facilities, and digital connectivity to promote equitable economic growth across the archipelago.",
    "President Joko Widodo emphasized the importance of sustainable energy initiatives by unveiling new policies aimed at reducing carbon emissions, expanding renewable energy projects, and encouraging private sector investment in green technologies.",
    "Amid rising global economic uncertainty, Indonesia's finance ministry introduced fiscal stimulus measures to stabilize the economy, targeting small and medium enterprises with tax incentives, loan support, and streamlined regulatory processes.",
    "The government is strengthening its commitment to environmental conservation by expanding protected forest areas, cracking down on illegal deforestation, and collaborating with international organizations to combat climate change.",
    "In response to increasing public demand for educational reform, the Ministry of Education and Culture launched a nationwide digital learning platform designed to enhance access to quality education, particularly in remote regions affected by inadequate infrastructure.",
    "Indonesia's health authorities are ramping up efforts to improve public healthcare services by increasing budget allocations for hospital upgrades, expanding vaccination programs, and addressing shortages of medical personnel in underserved communities.",
    "The government has initiated a large-scale economic transformation program focusing on industrial diversification, attracting foreign investment in high-tech sectors, and reducing the country's dependency on natural resource exports.",
    "To bolster national security, Indonesian lawmakers passed new legislation aimed at modernizing the armed forces, enhancing cybersecurity infrastructure, and increasing coordination between military and civilian agencies in response to evolving regional threats."
    "The Ministry of Tourism and Creative Economy announced a series of initiatives to revive the tourism industry post-pandemic, including promoting sustainable tourism practices, supporting local businesses, and developing new travel destinations beyond popular hotspots like Bali."
    "In an effort to strengthen diplomatic ties and boost regional cooperation, Indonesia hosted a high-level summit involving Southeast Asian leaders to discuss economic integration, environmental challenges, and strategies for maintaining political stability in the region."
]

# Preprocess the sentences
tokenized_sentences = [simple_preprocess(sentence) for sentence in sentences]

# Train a Word2Vec model
model = Word2Vec(tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)

# Get word vectors
word_vectors = np.array([model.wv[word] for word in model.wv.index_to_key])

# 3D PCA reduction
pca = PCA(n_components=3)
reduced_vectors = pca.fit_transform(word_vectors)

# Color setup
color_map = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'purple',
    4: 'orange',
    5: 'cyan',
    6: 'magenta',
    7: 'yellow',
    8: 'brown',
    9: 'pink'
}

word_colors = []
for word in model.wv.index_to_key:
    for i, sentence in enumerate(tokenized_sentences):
        if word in sentence:
            word_colors.append(color_map[i])
            break

# Create the 3D scatter plot
scatter = go.Scatter3d(
    x=reduced_vectors[:, 0],
    y=reduced_vectors[:, 1],
    z=reduced_vectors[:, 2],
    mode='markers+text',
    text=model.wv.index_to_key,
    textposition='top center',
    marker=dict(color=word_colors, size=2)
)

fig = go.Figure(data=[scatter])

fig.update_layout(
    scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
    title="3D Visualization of Word Embeddings",
    width=1000,
    height=1000
)

# ⭐ Display in Streamlit
st.title("3D Word Embedding Visualization")
st.plotly_chart(fig)
