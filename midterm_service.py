from collections import defaultdict
from flask import Flask, escape, request, Response, render_template, redirect, url_for
#from fuzzywuzzy import fuzz
from imdb import IMDb
import json
import operator
import os
import pandas as pd
import re
from textblob import TextBlob, Word, Blobber 
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = Flask(__name__)

ia = IMDb()
cwd = os.getcwd()
path_to_database = (os.path.join(cwd, "database.txt"))
#path_to_database = "/Users/asnafatimaali/Desktop/STEVENS/FE595/Midterm_extra/database.txt"   # PATH TO DATABASE 
with open(path_to_database, 'r') as file:
    data_base = json.loads(file.read())

numbers = {"one|1|I":"one|1|I", "two|2|II":"two|2|II", "three|3|III":"three|3|III",
"four|4|IV":"four|4|IV", "five|5|V":"five|5|V", "six|6|VI":"six|6|VI",
"seven|7|VII":"seven|7|VII", "eight|8|VIII":"eight|8|VIII", "nine|9|IX":"nine|9|IX",
"ten|10|X":"ten|10|X"}
number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "one", "two", "three",
"four", "five", "six", "seven", "eight", "nine", "ten","i", "ii", "iii", "iv", "v", "vi",
"vii", "viii", "ix", "x"]


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
    if len(movie_finder) == 0:
        movie_info = "ERROR"
    else:
        max_id = top_match(movie_finder)
        movie_info = ia.get_movie(max_id)
        movie_info = movie_info['synopsis']
        movie_info = str(movie_info)
        movie_info = info_cleaner(movie_info)
    return movie_info

language = dict([('ab', 'Abkhaz'),
    ('aa', 'Afar'),('af', 'Afrikaans'),('ak', 'Akan'),('sq', 'Albanian'),('am', 'Amharic'),('ar', 'Arabic'),
    ('an', 'Aragonese'),('hy', 'Armenian'),('as', 'Assamese'),('av', 'Avaric'),('ae', 'Avestan'),('ay', 'Aymara'),
    ('az', 'Azerbaijani'),('bm', 'Bambara'),('ba', 'Bashkir'),('eu', 'Basque'),('be', 'Belarusian'),
    ('bn', 'Bengali'),('bh', 'Bihari'),('bi', 'Bislama'),('bs', 'Bosnian'),('br', 'Breton'),('bg', 'Bulgarian'),
    ('my', 'Burmese'),('ca', 'Catalan; Valencian'),('ch', 'Chamorro'),('ce', 'Chechen'),('ny', 'Chichewa; Chewa; Nyanja'),
    ('zh', 'Chinese'),('cv', 'Chuvash'),('kw', 'Cornish'),('co', 'Corsican'),('cr', 'Cree'),('hr', 'Croatian'),
    ('cs', 'Czech'),('da', 'Danish'),('dv', 'Divehi; Maldivian;'),('nl', 'Dutch'),('dz', 'Dzongkha'),
    ('en', 'English'),('eo', 'Esperanto'),('et', 'Estonian'),('ee', 'Ewe'),('fo', 'Faroese'),('fj', 'Fijian'),
    ('fi', 'Finnish'),('fr', 'French'),('ff', 'Fula'),('gl', 'Galician'),('ka', 'Georgian'),('de', 'German'),
    ('el', 'Greek, Modern'),('gn', 'Guaraní'),('gu', 'Gujarati'),('ht', 'Haitian'),('ha', 'Hausa'),('he', 'Hebrew (modern)'),
    ('hz', 'Herero'),('hi', 'Hindi'),('ho', 'Hiri Motu'),('hu', 'Hungarian'),('ia', 'Interlingua'),('id', 'Indonesian'),
    ('ie', 'Interlingue'),('ga', 'Irish'),('ig', 'Igbo'),('ik', 'Inupiaq'),('io', 'Ido'),('is', 'Icelandic'),
    ('it', 'Italian'),('iu', 'Inuktitut'),('ja', 'Japanese'),('jv', 'Javanese'),('kl', 'Kalaallisut'),('kn', 'Kannada'),
    ('kr', 'Kanuri'),('ks', 'Kashmiri'),('kk', 'Kazakh'),('km', 'Khmer'),('ki', 'Kikuyu, Gikuyu'),('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz, Kyrgyz'),('kv', 'Komi'),('kg', 'Kongo'),('ko', 'Korean'),('ku', 'Kurdish'),('kj', 'Kwanyama, Kuanyama'),
    ('la', 'Latin'),('lb', 'Luxembourgish'),('lg', 'Luganda'),('li', 'Limburgish'),('ln', 'Lingala'),('lo', 'Lao'),
    ('lt', 'Lithuanian'),('lu', 'Luba-Katanga'),('lv', 'Latvian'),('gv', 'Manx'),('mk', 'Macedonian'),('mg', 'Malagasy'),
    ('ms', 'Malay'),('ml', 'Malayalam'),('mt', 'Maltese'),('mi', 'Māori'),('mr', 'Marathi (Marāṭhī)'),('mh', 'Marshallese'),
    ('mn', 'Mongolian'),('na', 'Nauru'),('nv', 'Navajo, Navaho'),('nb', 'Norwegian Bokmål'),('nd', 'North Ndebele'),
    ('ne', 'Nepali'),('ng', 'Ndonga'),('nn', 'Norwegian Nynorsk'),('no', 'Norwegian'),('ii', 'Nuosu'),('nr', 'South Ndebele'),
    ('oc', 'Occitan'),('oj', 'Ojibwe, Ojibwa'),('cu', 'Old Church Slavonic'),('om', 'Oromo'),('or', 'Oriya'),
    ('os', 'Ossetian, Ossetic'),('pa', 'Panjabi, Punjabi'),('pi', 'Pāli'),('fa', 'Persian'),('pl', 'Polish'),
    ('ps', 'Pashto, Pushto'),('pt', 'Portuguese'),('qu', 'Quechua'),('rm', 'Romansh'),('rn', 'Kirundi'),
    ('ro', 'Romanian, Moldavan'),('ru', 'Russian'),('sa', 'Sanskrit (Saṁskṛta)'),('sc', 'Sardinian'),('sd', 'Sindhi'),
    ('se', 'Northern Sami'),('sm', 'Samoan'),('sg', 'Sango'),('sr', 'Serbian'),('gd', 'Scottish Gaelic'),('sn', 'Shona'),
    ('si', 'Sinhala, Sinhalese'),('sk', 'Slovak'),('sl', 'Slovene'),('so', 'Somali'),('st', 'Southern Sotho'),('es', 'Spanish; Castilian'),
    ('su', 'Sundanese'),('sw', 'Swahili'),('ss', 'Swati'),('sv', 'Swedish'),('ta', 'Tamil'),('te', 'Telugu'),('tg', 'Tajik'),
    ('th', 'Thai'),('ti', 'Tigrinya'),('bo', 'Tibetan'),('tk', 'Turkmen'),('tl', 'Tagalog'),('tn', 'Tswana'),('to', 'Tonga'),
    ('tr', 'Turkish'),('ts', 'Tsonga'),('tt', 'Tatar'),('tw', 'Twi'),('ty', 'Tahitian'),('ug', 'Uighur, Uyghur'),
    ('uk', 'Ukrainian'),('ur', 'Urdu'),('uz', 'Uzbek'),('ve', 'Venda'),('vi', 'Vietnamese'),('vo', 'Volapük'),
    ('wa', 'Walloon'),('cy', 'Welsh'),('wo', 'Wolof'),('fy', 'Western Frisian'),('xh', 'Xhosa'),('yi', 'Yiddish'),
    ('yo', 'Yoruba'),('za', 'Zhuang, Chuang'),('zu', 'Zulu')])

# These exact stop words are from the NLTK stopwords
stopwords_list = ['a','about','above','after','again','against','ain','all','am','an','and',
'any','are','aren',"aren't",'as','at','be','because','been','before','being','below',
'between','both','but','by','can','couldn',"couldn't",'d','did','didn',"didn't",
'do','does','doesn', "doesn't",'doing','don',"don't",'down','during','each',
'few','for','from','further','had','hadn',"hadn't",'has','hasn',"hasn't",'have',
'haven',"haven't",'having','he','her','here','hers','herself','him','himself',
'his','how','i','if','in','into','is','isn',"isn't",'it',"it's",'its','itself',
'just','ll','m','ma','me','mightn',"mightn't",'more','most','mustn',"mustn't",
'my','myself','needn',"needn't",'no','nor','not','now','o','of','off','on',
'once','only','or','other','our','ours','ourselves','out','over','own','re',
's','same','shan',"shan't",'she',"she's",'should',"should've",'shouldn',"shouldn't",
'so','some','such','t','than','that',"that'll",'the','their','theirs','them','themselves',
'then','there','these','they','this','those','through','to','too','under','until',
'up','ve','very','was','wasn',"wasn't",'we','were','weren',"weren't",'what','when',
'where','which','while','who','whom','why','will','with','won',"won't",'wouldn',
"wouldn't",'y','you',"you'd","you'll","you're","you've",'your','yours','yourself',
'yourselves']


happy_list = ["overjoy","cheerful", "happy","content", "delighted", "delight","ecstatic", "elated","glad", "joyful","joyous","joy", 
"jubilant", "lively", "merry","overjoyed","peaceful","pleasant", "pleased","thrilled", "upbeat","blessed","blest","blissful", "blithe",
"captivated", "chipper", "chirpy","convivial", "exultant", "gay","gleeful", "gratified","intoxicated", "light", "peppy","perky", "sparkling", 
"sunny","tickled", "up", "satisfy"]
happy_list = " ".join(happy_list)

sad_list = ["bitter", "dismal", "melancholy", "mournful", "somber","wistful", "low", 
"morose", "bereaved", "wistful", "sorry", "doleful", "heartsick", "hurting","gloomy", "blue","weeping"
"dejected","sad", "irritate","lousy","upset","incapable","disappointment","doubtful","alone",
"hostile","discourage","uncertain","insult","ashame","indecisive","fatigue","sore","powerless",
"perplex","useless","annoy","diminish","embarrass","inferior","upset","guilty","hesitant","vulnerable",
"hateful","dissatisfy","shy","empty","unpleasant","miserable","stupefied","forced","offensive","detestable",
"disillusion","hesitant","bitter","repugnant","unbelieving","despair","aggressive","despicable","skeptical",
"frustrated","resentful","distress","inflame","abominable","misgiving","woeful","terrible","lost","pathetic","incensed","indespair","unsure","tragic","infuriate","sulky","uneasy",
"cross","dominate","tense","boil","insensitive","fearful","tearful","dull","terrified","torment",
"sorrowful","nonchalant","deprive","neutral","anxious","pain","grief","reserve",
"anguish","weary","deject","desolate","bore","nervous","reject","desperate","preoccupied","injure",
"pessimistic","worry","offend","unhappy","disinterest","afflict","lonely","lifeless","timid","ache",
"grieve","shaky","victim","mourn","restless","heartbroken","dismay","doubt","agony","threaten","coward","humiliate","alienate","wary"]
sad_list = " ".join(sad_list)

scary_list = ["alarm", "torture", "morbid", "tragic", "distrustful", "enraged", "provoke", "bad", "alarming", "chilling", "creepy", 
"eerie", "horrifying", "horrify", "intimidating", "shocking", "spooky", "shock", "bloddcurdling", "panic"
"horrendous", "gore", "unnerving" "frightening",  "daunting", "blood", "carnage", "slaughter", "evil", "paralyze", "dark"]
scary_list = " ".join(scary_list)

romantic_list = ["amorous", "charming", "corny", "dreamy", "erotic", "exciting", "exotic", "fanciful", "glamorous", "passionate", "tender", 
"chivalrous", "fond", "pituresque", "loving", "idyllic", 'heart','lovely', 'family','caring','forever','trust','passion','romance','sweet',
'kiss','love','hugs','warm','fun','kisses','joy','friendship','marriage','husband','wife','forever']
romantic_list = " ".join(romantic_list)

mystery_list =["suspicious", "baffling", "cryptic", "curious", "enigmatic", "inexplicable", "mystical", "obscure", "perplexing", "puzzling", "mysterious", "mystery"
"secretive", "weird", "abstruse", "arcane", "covert", "hidden", "impenetrable", "strange", "unknown", "insoluble", "incomprehensible", "furtive", "difficult", 
"necromantic", "occult", "oracular", "recondite", 'spiritual', "subjective", "symbolic", 'uncanny', "transcendental", "unfathomable", "unknowable", "unnatural", "veiled"]
mystery_list = " ".join(mystery_list)

comedy_list = ["absurd", "amusing", "droll", "entertaining", "hilarious", "ludicrous", "playful", "ridiculous", "silly", "whimsical", "antic", "slapstick", "farcical",
"jolly", "laughable", "mirthful", "priceless", "riotous", "waggish", "witty", "joke", "comedy", "comedic", "comedians"]
comedy_list = " ".join(comedy_list)

vectorization = TfidfVectorizer()

def cosine_similarity(input1, input2):
    tfidf = vectorization.fit_transform([input1, input2])
    return ((tfidf * tfidf.T).A)[0,1]

@app.route('/', methods =['GET', 'POST'])
def homepage():
    return render_template('services.html')


@app.route('/service1', methods = ["GET", "POST"])
def service1():
    render_template('one.html')
    if request.method == "POST":
        return redirect(url_for('/service1_result'))
    else:
        return render_template('one.html')

@app.route('/service1_result', methods = ['GET', 'POST'])
def service1_result():
    user_input1 = request.form['text']

    def get_sentiment(user_movie_input):
        text = movie_selection(user_movie_input)
        if text == "ERROR":
            text_sentiment = "Cannot Compute Sentiment for this Movie. Please Enter Another Title."
        else:
            blob = TextBlob(text)
            for sentence in blob.sentences:
                text_sentiment = sentence.sentiment.polarity
        
        return (text_sentiment)
    movie_sentiment = get_sentiment(user_input1)
    return render_template('present.html', output = movie_sentiment)

@app.route('/service2',methods = ['GET', "POST"])
def service2():
    render_template('two.html')
    if request.method == "POST":
        return redirect(url_for('/service2_result'))
    else:
        return render_template('two.html')

@app.route('/service2_result', methods = ['GET', "POST"])
def service2_result():
    user_input1 = request.form['text']
    user_input2 = request.form['text2']

    def get_key(val):
        for key, value in language.items(): 
            if val.lower() == value.lower():
                lang = key
                break
            else:
                lang = "Cannot Translate Synopsis"
        return lang
    
    def final_text(user_movie_input, chosen_language):
        chosen_language = get_key(chosen_language)
        if chosen_language == "Cannot Translate Synopsis":
            translation = chosen_language
        else:
            blob = TextBlob(movie_selection(user_movie_input))
            if blob == "ERROR":
                translation = "Cannot Translate for this Movie. Please Enter Another Title."
            else:
                translation = blob.translate(to = chosen_language)
        return(translation)

    return render_template('present.html', output = final_text(user_input1, user_input2))

@app.route('/service3', methods = ['GET', 'POST'])
def service3():
    render_template('three.html')
    if request.method == "POST":
        return redirect(url_for('/service3_result'))
    else:
        return render_template('three.html')

@app.route('/service3_result', methods = ['GET', 'POST'])
def service3_result():
    user_input1 = request.form['text']
    user_input2 = request.form['text2']
    
    def lemmatize_sentence(input_string):
        lemma_sentence = ""
        lemmas = []
        input_string = TextBlob(input_string)
        for x in input_string.words:
            x = Word(x)
            lemmas.append(x.lemmatize())
        for lemma in lemmas:
            if lemma not in stopwords_list:
                lemma_sentence = lemma_sentence + " " + lemma
        lemma_sentence = re.sub(r" \'", "\'", lemma_sentence)
        lemma_sentence = re.sub(r"^[ \t]+|[ \t]+$", "", lemma_sentence)

        return lemma_sentence

    movie1 = lemmatize_sentence(movie_selection(user_input1))
    movie2 = lemmatize_sentence(movie_selection(user_input2))
    if movie1 == "ERROR" or movie2 == "ERROR":
        score = "Cannot Calculate the Similarity between these movies. Please Enter Another Title."
    else:
        score = cosine_similarity(movie1, movie2)
        score = str(score)
    return render_template('present.html', output = score)


@app.route('/service4', methods = ['GET', 'POST'])
def service4():
    render_template('four.html')
    if request.method == "POST":
        return redirect(url_for('/service4_result'))
    else:
        return render_template('four.html')


@app.route('/service4_result', methods = ['GET', 'POST'])
def service4_result():
    user_input1 = request.form['text']
    user_input2 = request.form['text2']


    def mood_similarity(user_movie_input, mood_input):
        if movie_selection(user_movie_input) == "ERROR":
            service_output = "Cannot Calculate the Mood of this Movie, please enter another title"
        else:
            user_movie_input = movie_selection(user_movie_input)
            mood_input = str(mood_input)
            if mood_input in happy_list:
                service_output = "The cosine score of this being a happy movie is {}".format(cosine_similarity(user_movie_input, happy_list))
            elif mood_input in sad_list:
                service_output = "The cosine score of this being a sad movie is {}".format(cosine_similarity(user_movie_input, sad_list))
            elif mood_input in scary_list:
                service_output = "The cosine score of this being a scary movie is {}".format(cosine_similarity(user_movie_input, scary_list))
            elif mood_input in mystery_list:
                service_output = "The cosine score of this being a mysterious movie is {}".format(cosine_similarity(user_movie_input, mystery_list))
            elif mood_input in romantic_list:
                service_output = "The cosine score of this being a romantic movie is {}".format(cosine_similarity(user_movie_input, romantic_list))
            elif mood_input in comedy_list:
                service_output = "The cosine score of this being a comedic movie is {}".format(cosine_similarity(user_movie_input, comedy_list))
            else:
                service_output = "Please enter another mood, or a synonym variation."
        return(service_output)

    mood_score = mood_similarity(user_input1, user_input2)
    mood_score = str(mood_score)

    return render_template('present.html', output = mood_score)

@app.route('/service5', methods = ['GET', 'POST'])
def service5():
    render_template('five.html')
    if request.method == "POST":
        return redirect(url_for('/service5_result'))
    else:
        return render_template('five.html')  

@app.route('/service5_result', methods = ['GET', 'POST'])
def service5_result():
    user_input1 = request.form['text']

    def top_noun_phrases(user_movie_input): 
        movie_info = movie_selection(user_movie_input)
        if movie_info == "ERROR":
            count_noun = "Cannot Calculate the Top Noun Phrases of this Movie, please enter another title"
            count_noun = pd.DataFrame([x.split(';') for x in count_noun.split('\n')])
        else:
            blob = TextBlob(movie_info)
            nouns = list(blob.noun_phrases)
            frequency = defaultdict(int)

            for noun in nouns:
                if noun in frequency:
                    frequency[noun] += 1
                else:
                    frequency[noun] = 1

            top_common_nouns = sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)
            top_common_nouns = top_common_nouns[:10]
            count_top_ten = pd.DataFrame(top_common_nouns)
            count_noun = count_top_ten.rename(columns={0: "Nouns", 1: "Frequency"})
            count_noun = count_noun.reset_index(drop=True)

        return count_noun

    top_noun = top_noun_phrases(user_input1)

    return render_template('present2.html', tables=[top_noun.to_html(classes='data', header="true")])


@app.route('/service6', methods = ['GET', "POST"])
def service6():
    render_template('six.html')
    if request.method == "POST":
        return redirect(url_for('/service6_result'))
    else:
        return render_template('six.html')  


@app.route('/service6_result', methods = ['GET', "POST"])
def service6_result():

    user_input1 = request.form['text']

    count = list()
    adjectives = []
    def top_adj(user_movie_input):
        movie_info = movie_selection(user_movie_input)
        if movie_info == "ERROR":
            top_adjectives = "Cannot Calculate the Top Adjectives of this Movie, please enter another title"
            top_adjectives = pd.DataFrame([x.split(';') for x in top_adjectives.split('\n')])
        else:
            blob = TextBlob(movie_info)

            for word, pos in blob.tags:
                if pos == 'JJ':
                    adjectives.append(word)

            for i in range(0, len(adjectives)):
                count.append(adjectives.count(adjectives[i]))

            top_adjectives = pd.DataFrame()
            top_adjectives['Adjectives'] = adjectives
            top_adjectives['Count'] = count

            sort_count = top_adjectives.sort_values('Count',ascending = False)
            top_adjectives = sort_count.drop_duplicates().head(10)
            top_adjectives = top_adjectives.reset_index(drop=True)
        return top_adjectives

    top_adjies = top_adj(user_input1) 

    return render_template('present2.html', tables=[top_adjies.to_html(classes='data', header="true")])


@app.route('/service7_result', methods = ['GET', "POST"])
def service6_result():




@app.route('/service8_result', methods = ['GET', "POST"])
def service6_result():

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

    


@app.route('/service9_result', methods = ['GET', "POST"])
def service6_result():




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
