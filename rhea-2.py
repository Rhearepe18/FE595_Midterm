import csv
import pandas as pd
import nltk
from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt


#Input: change this movie_id for test purpose
movie_id = 417741


#calculate sentiment polarity
def detect_polarity(reviews):
    return TextBlob(reviews).sentiment.polarity

#get movie index from movie ID 
def get_movie_index(movie_id):
    idx = 0 
    x = 0
    y = 0
    
    for id in reviews_data.movie_id:
        if(id == movie_id):
            break
        else:
            x = x + 1
    return x
    
#Calculate sentiiment polarity of the movie based on reviews
def get_movie_sentiment(movie_idx):
    reviews = str(reviews_data.reviews[movie_idx]) 
    mov_sentiment = detect_polarity(reviews)
    return mov_sentiment

#Find top adjectives in the review
def top_adjectives(movie_idx):
    count = list()
    adjectives = []
    mov_adjectives = pd.DataFrame()
    reviews = str(reviews_data.reviews[movie_idx])
    blob = TextBlob(reviews)
    
    for word, pos in blob.tags:
        if pos =='JJ':
            adjectives.append(word)

    for i in range(0, len(adjectives)):
        count.append(adjectives.count(adjectives[i]))

    mov_adjectives['Adjectives'] = adjectives
    mov_adjectives['Frequency'] = count
    sorted_adj = mov_adjectives.sort_values('Frequency', ascending = False)
    return sorted_adj

#generate word cloud
def word_cloud(text):        
    wc = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    return plt.show()


if __name__ == "__main__":
    movie_index = 0
    mov_sentiment_val = 0.0
    movie_adj = []
    movie_data = pd.read_csv('movie_data.csv')
    reviews_data = movie_data[["movie_id", "reviews", "rating_votes","movie_rating"]]
    
    
    movie_index = get_movie_index(movie_id)
    print("movie index = " + str(movie_index))
    
    mov_sentiment_val = get_movie_sentiment(movie_index)
    print("movie sentiment polarity = " + str(mov_sentiment_val))
    
    mov_adjective = top_adjectives(movie_index)

    #update adjective items based on the overall polarity of the movie
    mov_adjective['polarity'] = mov_adjective.Adjectives.apply(detect_polarity) #add polarity column to include polarity of all the adjectives

    #based on the overall movie sentiment polarity, select only the adjectives that have the same polarity as the movie
    
    if(mov_sentiment_val > 0):
        updated_adj = mov_adjective[mov_adjective.polarity > 0]

    elif(mov_sentiment_val < 0):
        updated_adj = mov_adjective[mov_adjective.polarity < 0]

    else: 
        updated_adj = mov_adjective[mov_adjective.polarity == 0]
        
    print(updated_adj)
    #Output of adjective word cloud
    word_cloud(str(updated_adj.Adjectives))

    
