from flask import Flask, escape, request, Response, render_template, redirect, url_for
from fuzzywuzzy import fuzz
from imdb import IMDb
import json
import re
from textblob import TextBlob, Word
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

ia = IMDb()
path_to_database = "/Users/asnafatimaali/Desktop/STEVENS/FE595/Midterm_extra/database.txt"   # PATH TO DATABASE 
with open(path_to_database, 'r') as file:
    data_base = json.loads(file.read())

numbers = {"one|1|I":"one|1|I", "two|2|II":"two|2|II", "three|3|III":"three|3|III",
"four|4|IV":"four|4|IV", "five|5|V":"five|5|V", "six|6|VI":"six|6|VI",
"seven|7|VII":"seven|7|VII", "eight|8|VIII":"eight|8|VIII", "nine|9|IX":"nine|9|IX",
"ten|10|X":"ten|10|X"}
number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "one", "two", "three",
"four", "five", "six", "seven", "eight", "nine", "ten","i", "ii", "iii", "iv", "v", "vi",
"vii", "viii", "ix", "x"]

movie_input = "Lord of the Rings Fellowship" ##### THIS WILL REFER TO USER'S INPUT
movie_input2 = "Lord of the Rings Fellowship" ##### THIS WILL REFER TO USER'S INPUT

def top_match(finds):
    return max(set(finds), key=finds.count)


def info_cleaner(movie_synopsis):
    movie_synopsis = re.sub(r'[^\w\s\'\/]', " ", movie_synopsis) # remove everything that is not an alphanumeric and space
    movie_synopsis = re.sub(r" \'", "", movie_synopsis) # this will remove quotes that are not used as apostrophes
    movie_synopsis = re.sub(r" +", " ", movie_synopsis) # remove multiple spaces 
    movie_synopsis = re.sub(r" \'", "", movie_synopsis)
    movie_synopsis = re.sub(r"^[ \t]+|[ \t]+$", "", movie_synopsis) # remove trailing and leading spaces 
    return movie_synopsis

def movie_selection(user_input):
    user_input = re.sub(r'[^\w\s]', " ",user_input)
    user_input = re.sub(r" +" , " ", user_input)
    user_input = TextBlob(user_input)
    movie_finder = []
    for token in user_input.words:
        if token.lower() in number_list:
            for num, number in numbers.items():
                if re.search(token, num, re.IGNORECASE):
                    token = number
        for key, value in data_base.items():
            if re.search(token,key, re.IGNORECASE):
                movie_finder.append(value)

    max_id = top_match(movie_finder)
    movie_info = ia.get_movie(max_id)
    movie_info = movie_info['synopsis']
    movie_info = str(movie_info)
    movie_info = info_cleaner(movie_info)
    return movie_info


@app.route('/homepage', methods =['GET', 'POST'])
def homepage():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'



@app.route('/service1', methods = ['GET'])
def service1():
    name = request.args.get("name", "Service1")
    return f'Hello, {escape(name)}!'



@app.route('/service2', methods = ['GET'])
def service2():
    name = request.args.get("name", "Service2")
    return f'Hello, {escape(name)}!'



@app.route('/service3', methods = ['GET'])
def service3():
    name = request.args.get("name", "Service3")
    return f'Hello, {escape(name)}!'



@app.route('/service4', methods = ['GET'])
def service4():
    name = request.args.get("name", "Service4")
    return f'Hello, {escape(name)}!'


@app.route('/service5', methods = ['GET'])
def service5():
    name = request.args.get("name", "Service5")
    return f'Hello, {escape(name)}!'


@app.route('/service6', methods = ['GET'])
def service6():
    name = request.args.get("name", "Service6")
    return f'Hello, {escape(name)}!'



if __name__ == "__main__":
    app.run(debug = True)
