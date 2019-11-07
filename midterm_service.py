from flask import Flask, escape, request
from imdb import IMDb
import json
import re
from textblob import TextBlob
import requests
from textblob import TextBlob, Word, Blobber
from textblob.classifiers import NaiveBayesClassifier
from textblob.taggers import NLTKTagger
import nltk


app = Flask(__name__)

ia = IMDb()
path_to_database = "/Users/asnafatimaali/Desktop/STEVENS/FE595/Midterm/database.txt"   # PATH TO DATABASE 
with open(path_to_database, 'r') as file:
    data_base = json.loads(file.read())

numbers = {"one|1|I":"one|1|I", "two|2|II":"two|2|II", "three|3|III":"three|3|III",
"four|4|IV":"four|4|IV", "five|5|V":"five|5|V", "six|6|VI":"six|6|VI",
"seven|7|VII":"seven|7|VII", "eight|8|VIII":"eight|8|VIII", "nine|9|IX":"nine|9|IX",
"ten|10|X":"ten|10|X"}
number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "one", "two", "three",
"four", "five", "six", "seven", "eight", "nine", "ten","i", "ii", "iii", "iv", "v", "vi",
"vii", "viii", "ix", "x"]

user_input = "   HArry-Potter DEathly Hallows ii" ##### THIS WILL REFER TO USER'S INPUT
user_input = re.sub(r'[^\w\s]', " ",user_input)
user_input = re.sub(r" +", " ", user_input)

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


def top_match(finds):
    return max(set(finds), key=finds.count)


max_id = top_match(movie_finder)

movie_info = ia.get_movie(max_id)
movie_info = movie_info['synopsis']


@app.route('/homepage', methods =['GET', 'POST'])
def homepage():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'



@app.route('/service1', methods = ['GET'])
def get_sentiment():
    name = request.args.get("name", "Service1")
    text = str(movie_info[0])
    blob = TextBlob(text)
    blob.tags
    blob.noun_phrases
    
    for sentence in blob.sentences:
        text_sentiment = sentence.sentiment.polarity
    
    return (text_sentiment)

print(get_sentiment(text))

@app.route('/service2', methods = ['GET'])
def get_key(val):
    name = request.args.get("name", "Service2")
    
    for key, value in language.items(): 
         if val == value: 
            return key
    return ("key doesn't exist") 
   
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


@app.route('/service3', methods = ['GET'])
def final_text(blob):
    name = request.args.get("name", "Service3")
    
    enter_language=input('enter a language')
    chosen_language = get_key(enter_language)
    blob = TextBlob(str(text))
    
    return (blob.translate(to = chosen_language))

print(final_text(blob))

@app.route('/service4', methods = ['GET'])
def service4():
    name = request.args.get("name", "Service4")
    return f'Hello, {escape(name)}!'


@app.route('/service5', methods = ['GET'])
def service5():
    name = request.args.get("name", "Service5")
    return f'Hello, {escape(name)}!'

movie_info = str(movie_info)
blob = TextBlob(movie_info)
blob.tags

# Top 10 nouns

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
print(count_noun)



@app.route('/service6', methods = ['GET'])
def service6():
    name = request.args.get("name", "Service6")
    return f'Hello, {escape(name)}!'
#Top 10 adjectives
adjectives = []
#Top adjectives using pos
for word, pos in blob.tags:
      if pos == 'JJ':
      adjectives.append(word)


count = list()

for i in range(0, len(adjectives)):
    count.append(adjectives.count(adjectives[i]))


top_adjectives = pd.DataFrame()
top_adjectives['Adjectives'] = adjectives
top_adjectives['Count'] = count

sort_count = top_adjectives.sort_values('Count')
top_adjectives = sort_count.drop_duplicates().tail(10)


if __name__ == "__main__":
    app.run(debug = True)
