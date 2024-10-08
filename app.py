import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler

# Load job dataset (replace with actual job dataset)
# The dataset should contain 'job_title' and 'skills_required' columns
df = pd.read_csv('jobs.csv')  # Replace with your actual file

# Streamlit app
st.title("Job Recommender System")

st.write("This app recommends jobs based on your skills using clustering algorithms.")

# Input skills from the user
user_input = st.text_input("Enter your skills separated by commas (e.g. Python, Machine Learning, Data Analysis):")

# Preprocess skills data using CountVectorizer (convert to a numerical format)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['skills_required']).toarray()

# Perform KMeans clustering on jobs based on their required skills
kmeans = KMeans(n_clusters=5)  # Number of clusters can be adjusted
df['cluster'] = kmeans.fit_predict(X)

# Predict the closest job cluster based on user input skills
if st.button("Recommend Jobs"):
    if user_input:
        # Vectorize the user's skills input
        user_skills_vect = vectorizer.transform([user_input]).toarray()

        # Find the closest cluster for the user
        user_cluster = kmeans.predict(user_skills_vect)[0]

        # Recommend jobs from the same cluster
        recommended_jobs = df[df['cluster'] == user_cluster]['job_title'].values

        if len(recommended_jobs) > 0:
            st.write(f"**Recommended Jobs for your skills:**")
            for job in recommended_jobs:
                st.write(f"- {job}")
        else:
            st.write("No matching jobs found. Try adding more or different skills.")
    else:
        st.write("Please enter your skills.")

# Optional: Visualize the cluster distribution
if st.checkbox("Show Job Cluster Distribution"):
    st.bar_chart(df['cluster'].value_counts())
