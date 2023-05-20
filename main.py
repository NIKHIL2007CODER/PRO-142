from flask import Flask, jsonify
import pandas as pd
from demographic import output
from content_based import get_recommendation

movies_data = pd.read_csv('D:/WhjrNewFolder/C141-MovieRecommedation/final.csv')

app = Flask(__name__)

# extracting important information from dataframe
all_movies = movies_data[["original_title" , "poster_link" , "release_date" , "runtime" , "weighted_rating"]]


# variables to store data
liked_movies = []
disliked_movies = []
unwatched_movies = []


# method to fetch data from database
def assign_val():
  m_data = {
    "original_title": all_movies.iloc[0 , 0],
    "poster_link": all_movies.iloc[0 , 1],
    "release_date": all_movies.iloc[0 , 2] or "N/A",
    "duration": all_movies.iloc[0 , 3],
    "rating": all_movies.iloc[0 , 4]

  }
  return m_data

# /movies api
@app.route("/movies")
def get_movies():
  movie_data = assign_val()
  return jsonify({
    "data":movie_data,
    "status":"success"
  })

# /like api
@app.route("/liked")
def liked():
  global all_movies

  movie_data = assign_val()
  liked_movies.append(movie_data)
  all_movies.drop([0] , inplace = True)
  all_movies = all_movies.reset_index(drop = True)
  return jsonify({
    "status":"success"
  })

@app.route("/likedMovies")
def likedMovies():
  global liked_movies
  return jsonify({
    'data':liked_movies,
    "status":"success"
  })


# /dislike api
@app.route("/disliked")
def disliked():
  global all_movies

  movie_data = assign_val()
  disliked_movies.append(movie_data)
  all_movies.drop([0] , inplace = True)
  all_movies = all_movies.reset_index(drop = True)
  return jsonify({
    "status":"success"
  })

# /did_not_watch api
@app.route("/unwatched")
def notwatched():
  global all_movies

  movie_data = assign_val()
  unwatched_movies.append(movie_data)
  all_movies.drop([0] , inplace = True)
  all_movies = all_movies.reset_index(drop = True)
  return jsonify({
    "status":"success"
  })

@app.route("/popularMovies")
def popMovies():
  popMovieData = []
  for index , row in output.iterrows():
    p = {
      "original_title" : row["original_title"],
      "poster_link" : row["poster_link"],
      "release_date" : row["release_date"],
      "duration" : row["runtime"],
      "rating" : row["weighted_rating"]
    }
    popMovieData.append(p)
  return jsonify({
    "data":popMovieData,
    "status":"success"
  })

'''@app.route("/recMovies")
def recMovies():
  global liked_movies
  colNames = ["original_title" , "poster_link" , "runtime" , "release_date" , "weighted_rating"]
  allRecommended = pd.DataFrame(columns = colNames)
  for i in liked_movies:
    recOutput = get_recommendation(i["original_title"])
    print(recOutput)
   allRecommended = allRecommended.append(recOutput)
  allRecommended.drop_duplicates(subset = ["original_title"] , inplace = True)
  recMovieData = []
  print(allRecommended)
  for index , row in allRecommended.iterrows():
    r = {
      "original_title" : row["original_title"],
      "poster_link" : row["poster_link"],
      "duration" : row["runtime"],
      "release_date" : row["release_date"],
      "rating" : row["weighted_rating"]
    }
    recMovieData.append(r)
    
   
  return jsonify({
    "data":allRecommended,
    "status":"success"
  })'''
@app.route("/recMovies")
def recommended_movies():
    global liked_movies
    col_names=['original_title', 'poster_link', 'release_date', 'runtime', 'weighted_rating']
    all_recommended = pd.DataFrame(columns=col_names)
    
    for liked_movie in liked_movies:
        output = get_recommendation(liked_movie["original_title"])
        all_recommended=all_recommended.append(output)

    all_recommended.drop_duplicates(subset=["original_title"],inplace=True)

    recommended_movie_data=[]

    for index, row in all_recommended.iterrows():
        _p = {
            "original_title": row["original_title"],
            "poster_link":row['poster_link'],
            "release_date":row['release_date'] or "N/A",
            "duration": row['runtime'],
            "rating": row['weighted_rating']/2
        }
        recommended_movie_data.append(_p)

    return jsonify({
        "data":recommended_movie_data,
        "status": "success"
    })



if __name__ == "__main__":
  app.run(debug = True)