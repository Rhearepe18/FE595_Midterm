# FE595_Midterm- NLP Web API Services

This project is for creating a web API that will provide users with NLP data on moviessubmitted data. We have crated & deployed this application as a flask application.

# Getting Started

These instructions will get you a copy of the project up and running on your own AWS machine for development and testing purposes.

# Prerequisites

An AWS ec2 instance needs to be created. For more details on this please refer to the AWS user guide here- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html


# Installing
A step by step series of commands to get you env running

Preparing the AWS instance. First you need to have super user permissions to create folders:

```sudo su```

Now we begin by installing git and Python 3 if they are not already present
```
yum install git
yum install python3
```

We need to install new python packages with help of pip. So lets install pip.
```
sudo easy_install pip
```
If the installation is successful, you will be able to check the version of pip

```
pip --version
```
If this gives an error then we can try an alternate command

```
python3 --version
sudo apt-get install python-pip
```
This command might work, but if does not we need to download & install pip and setup PATH variable to get pip working. Use the following commands -
```
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip --version
```
It is possible that the AWS instance Linux version still gives error for pip after this

follow the below steps to add the installation path of pip to the PATH variable
```
echo $PATHecho $PATH
export PATH=~/.local/bin:$PATH
echo $PATH
pip --version
```
Now we are ready to install the required libraries -
```
pip install requests

pip install textblob

python3 -m textblob.download_corpora

pip install pandas

pip install Flask-Limiter
```
We have made the code available in a git repo. Clone to repository and get the code
```
git clone https://github.com/AsnaFatimaAli/FE595_Midterm.git
ls -ltr
cd MidTerm/
ls -ltr
```
Now lets try to run the flask application-
```
python3 midterm_service.py
[root@ip-172-31-43-40 MidTerm]# python3 midterm_service.py
 * Serving Flask app "midterm" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```
Now the applcation is up and running.

# Running the tests
You can look at the application swagger file using the base link - http://:8080/

You can call the various end points as described in the swagger UI

# Built With

Flask - The web framework used
Git - Code management
Textblob - Used to create the NLP services

# NLP Description Serivces

Movie Sentiment: provides sentiment of the movie based on the movie's polarity synopsis.

Synopsis Translation: allows translation of the synopsis to different languages.

Cosyine Similarity: compares how similar are two input movies.

Mood Similarity: computes what's the mood of each of the input movies and compares both.

Count Noun: calculates the top noun phrases of a movie.

Adjectives: displays the top adjectives of a movie.

