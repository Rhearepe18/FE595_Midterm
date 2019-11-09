# FE595_Midterm- NLP Web API Services

This project is for creating a web API that will provide users with NLP data on moviessubmitted data. We have crated & deployed this application as a flask application.

# Getting Started

These instructions will get you a copy of the project up and running on your own AWS machine for development and testing purposes.

# Prerequisites

An AWS ec2 instance needs to be created. For more details on this please refer to the AWS user guide here- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html


# Installing
A step by step series of commands to get your environment running

Preparing the AWS instance. First you need to have super user permissions to create folders:

```sudo su```

Install git and Python 3 if they are not already presenton the instance
```
yum install git
yum install python3
```

You may not need to install pip separately, but if you run into an error while installing the required libraries, use the following command:
```
sudo easy_install pip
```

Install the following required libraries:
```
pip3 install flask

pip3 install textblob

python3 -m textblob.download_corpora

pip3 install pandas

pip3 install sklearn
```
We have made the code available in a git repo. Clone to repository and get the code
```
cd ../..
git clone https://github.com/AsnaFatimaAli/FE595_Midterm.git
ls 
cd FE595_MidTerm/
ls -ltr
```
Now lets try to run the flask application-
```
python3 midterm_service.py
[root@ip-172-31-43-40 MidTerm]# python3 midterm_service.py
 * Serving Flask app "midterm_serice" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```
Now the applcation is up and running.

# Running the tests
You can look at the application file using the base link - http://your specfic IP address :8080/

# Built With

Flask - The web framework used
Git - Code management
Textblob &sklearn - Used to create the NLP services

# NLP Description Serivces

Movie Sentiment: provides sentiment of the movie based on the polarity of the movie's synopsis.

Synopsis Translation: allows translation of the synopsis to different languages.

Cosine Similarity: compares how similar are two input movies.

Mood Similarity: computes how much of a mood specified the input movies is, and compares both.

Count Noun: calculates the top noun phrases of a movie.

Adjectives: displays the top adjectives of a movie.

