import streamlit as st
import pandas as pd
import numpy as np
import joblib
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.graph_objects as go

# Load pre-trained models
lda_model = LdaModel.load('lda_model.gensim')
dictionary = Dictionary.load('lda_dictionary.dict')
nmf_model = joblib.load('nmf_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
topic_model = BERTopic.load('bert_topic_model')

# Streamlit UI
st.title("Interactive Topic Modeling with LDA, NMF, and BERTopic")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("Data Preview:", df.head())

    def preprocess_text(text):
        text = str(text).lower()
        text = ''.join([char for char in text if char.isalpha() or char.isspace()])
        return text

    text_column = 'title'
    df['cleaned_text'] = df[text_column].apply(preprocess_text)

    num_topics = st.slider("Select the number of topics to display", 1, 30, 10)

    # Prepare topic models
    corpus = [dictionary.doc2bow(text.split()) for text in df['cleaned_text']]
    lda_topics = [lda_model.get_document_topics(bow) for bow in corpus]

    tfidf_matrix = tfidf_vectorizer.transform(df['cleaned_text'])
    nmf_topics = nmf_model.transform(tfidf_matrix)

    topics, _ = topic_model.transform(df['cleaned_text'].tolist())

    df['lda_topic'] = [max(lda, key=lambda x: x[1])[0] for lda in lda_topics]
    df['nmf_topic'] = np.argmax(nmf_topics, axis=1)
    df['bertopic_topic'] = topics

    def get_top_lda_words(topic_id, num_words=10):
        if topic_id >= lda_model.num_topics:
            return []
        return [word for word, _ in lda_model.show_topic(topic_id, topn=num_words)]

    def get_top_nmf_words(topic_id, num_words=10):
        return [tfidf_vectorizer.get_feature_names_out()[i] for i in np.argsort(nmf_model.components_[topic_id])[::-1][:num_words]]

    def get_top_bertopic_words(topic_id):
        return topic_model.get_topic(topic_id)

    # Calculate aggregated metrics
    lda_scores = [max([score for _, score in lda]) if lda else 0 for lda in lda_topics]
    nmf_scores = np.max(nmf_topics, axis=1)
    bertopic_counts = df['bertopic_topic'].value_counts().to_dict()

    lda_agg = [np.mean([score for idx, score in zip(df['lda_topic'], lda_scores) if idx == i]) for i in range(lda_model.num_topics)]
    nmf_agg = [np.mean([score for idx, score in zip(df['nmf_topic'], nmf_scores) if idx == i]) for i in range(num_topics)]
    bertopic_agg = [bertopic_counts.get(i, 0) for i in range(num_topics)]

    # Create a scatter plot to visualize topic distributions
    fig = go.Figure()

    y_offsets = [-0.2, 0, 0.2]  # Add jitter to avoid overlap

    for i in range(min(num_topics, lda_model.num_topics)):
        lda_words = get_top_lda_words(i)
        nmf_words = get_top_nmf_words(i)
        bertopic_words = get_top_bertopic_words(i)

        fig.add_trace(go.Scatter(
            x=[i, i, i],
            y=[lda_agg[i] + y_offsets[0], nmf_agg[i] + y_offsets[1], bertopic_agg[i] + y_offsets[2]],
            mode='markers',
            name=f"Topic {i}",
            hovertext=[
                f"<b>LDA</b>: {', '.join(lda_words)}",
                f"<b>NMF</b>: {', '.join(nmf_words)}",
                f"<b>BERTopic</b>: {', '.join([word for word, _ in bertopic_words])}"
            ],
            hoverinfo="text",
            marker=dict(size=15, line=dict(width=2))
        ))

    fig.update_layout(
        title="Interactive Topic Visualization (Hover for Words)",
        xaxis_title="Topic Number",
        yaxis_title="Topic Weight / Doc Count",
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig)

    # Displaying topics in a simple expandable section
    st.subheader("Topic Word Lists")
    for i in range(min(num_topics, lda_model.num_topics)):
        with st.expander(f"Topic {i}"):
            st.write(f"**LDA:** {', '.join(get_top_lda_words(i))}")
            st.write(f"**NMF:** {', '.join(get_top_nmf_words(i))}")
            st.write(f"**BERTopic:** {', '.join([word for word, _ in get_top_bertopic_words(i)])}")

    # Select topic to show sample documents
    selected_topic = st.selectbox("Select a topic to view sample documents", range(min(num_topics, lda_model.num_topics)))
    sample_docs = df[df['bertopic_topic'] == selected_topic].head(5)

    st.write(f"Sample Documents for Topic {selected_topic}")
    for doc in sample_docs[text_column]:
        st.markdown(f"- {doc}")

    # Prepare metadata for download
    metadata = df[['title', 'lda_topic', 'nmf_topic', 'bertopic_topic']]
    metadata_file = "topic_metadata.csv"
    metadata.to_csv(metadata_file, index=False)
    st.download_button("Download Topic Metadata", metadata_file)
