import csv
import pandas as pd

from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt

movie_data = pd.read_csv('/Users/rhearepe/Downloads/movie_data.csv')
reviews_data = movie_data[["movie_id", "reviews", "rating_votes","movie_rating"]]

text = reviews_data.reviews[0]

def word_cloud(movie_id):
    wc = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    return plt.show()

word_cloud(417741)