import pandas as pd 

df = pd.read_csv("D:/WhjrNewFolder/C141-MovieRecommedation/final.csv")

df  = df.sort_values("weighted_rating" , ascending = False)

output  = df[["original_title" , "poster_link" , "runtime" , "release_date" , "weighted_rating"]].head(20)

