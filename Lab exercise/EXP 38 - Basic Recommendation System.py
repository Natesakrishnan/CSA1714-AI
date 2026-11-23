
# Recommendation System using Collaborative Filtering

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Create sample user-item ratings
ratings = {
    'Movie1': [5, 4, 0, 0, 2],
    'Movie2': [4, 5, 0, 0, 1],
    'Movie3': [0, 0, 5, 4, 0],
    'Movie4': [0, 0, 4, 5, 0],
    'Movie5': [2, 1, 0, 0, 5]
}

df = pd.DataFrame(
    ratings,
    index=['User1', 'User2', 'User3', 'User4', 'User5']
)

print("User-Item Rating Matrix:")
print(df)

# Step 2: Calculate user similarity
similarity = cosine_similarity(df)

similarity_df = pd.DataFrame(
    similarity,
    index=df.index,
    columns=df.index
)

print("\nUser Similarity Matrix:")
print(similarity_df.round(2))

# Step 3: Select target user
target_user = 'User1'

# Step 4: Calculate predicted ratings
user_sim = similarity_df.loc[target_user].drop(target_user)

weighted_sum = df.T.dot(user_sim)
similarity_sum = df.ne(0).T.dot(user_sim)

predicted_ratings = weighted_sum / similarity_sum.replace(0, float('nan'))

# Step 5: Recommend unrated movies
unrated_movies = df.loc[target_user][df.loc[target_user] == 0].index

recommendations = predicted_ratings.loc[unrated_movies].dropna()
recommendations = recommendations.sort_values(ascending=False)

print("\nRecommendations for", target_user, ":")

if len(recommendations) > 0:
    for movie, score in recommendations.items():
        print(movie, "Predicted Rating:", round(score, 2))
else:
    print("No recommendations available.")
