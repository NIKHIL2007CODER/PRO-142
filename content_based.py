import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("D:/WhjrNewFolder/C141-MovieRecommedation/final.csv")
df = df[df['soup'].notna()]

count = CountVectorizer(stop_words = "english")

count_matrix = count.fit_transform(df["soup"])

cosine = cosine_similarity(count_matrix , count_matrix)

df = df.reset_index()

indices = pd.Series(df.index , index = df['original_title'])

def get_recommendation(title):
  idx = indices[title]
  simScore = list(enumerate(cosine[idx]))
  simScore = sorted(simScore , key = lambda x:x[1] , reverse = True)
  simScore = simScore[1:11]
  movieIndex = [i[0]for i in simScore]
  return df [["original_title" , "poster_link" , "runtime" , "release_date" , "weighted_rating"]].iloc[movieIndex]