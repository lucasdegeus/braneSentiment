#!/usr/bin/env python3

## Import required packages
import spacy
import re
import numpy as np
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
import demoji
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from emosent import get_emoji_sentiment_rank
import sys
import os
import yaml
import base64
from typing import List
demoji.download_codes()
sid = SentimentIntensityAnalyzer()

## Create regular expression to remove URLs
REMOVE_URL = re.compile(
    "([^0-9A-Za-z# \t" +
    "[!\"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~]\"" + # UNTESTED PLS TEST
    "\U0001F300-\U0001F5FF" + # symbols & pictographs
    "\U0001F600-\U0001F64F" + # emoticons
    "\U0001F900-\U0001F9FF" +  # Supplemental Symbols and Pictographs
    "])|(\w+:\/\/\S+)")

#Removes url from a tweet
def remove_url(txt):
    return " ".join(re.sub(REMOVE_URL, "", txt).split())

#Splits multi word hashtags into seperate words
def split_hashtag(hashtag):
    if hashtag.isupper() or hashtag.islower():
        return hashtag
    return ' '.join(word for word in re.findall('[A-Z][^A-Z]*', hashtag))


#Splits a tweet up in sentences
def preprocess(tweet):
    final = []
    for sentence in nltk.sent_tokenize(tweet):
        new_tweet = remove_url(sentence)
        new_tweet = new_tweet.split()
        final_tweet = []
        for i in new_tweet:
            if i[0] == "#":
                final_tweet.append(split_hashtag(i[1:]))
            else:
                final_tweet.append(i)
        if len(final_tweet) > 2:
            final.append(' '.join(word for word in final_tweet))
    return final

## Retrieve the sentiment score for each preprocessed tweet and append to the results array
def vader_score2(tweet):
    result = [sid.polarity_scores(i)['compound'] for i in preprocess(tweet)]
    result2 = []
    for i in result:
        if i != 0.0:
            result2.append(i)
    if len(result2) == 0:
        return 0.0
    return np.mean(result2)

## Calculate the emoji-sentiment in each tweet, if none are present return False
def calc_emoji_sent(tweet):
    emojis = demoji.findall_list(tweet, desc = False)
    emosentiment = []
    for emoji in emojis:
        try:
            emoji_sentiment = get_emoji_sentiment_rank(emoji)['sentiment_score']
            emosentiment.append(emoji_sentiment)
        except:
            continue
    if len(emosentiment) > 0:
        return (sum(emosentiment) / len(emosentiment))
    else:
        return False

## Combine the textual-sentiment and emoji-sentiment
def vader2_emo_senti(tweet):
    v2 = vader_score2(tweet)
    emo = calc_emoji_sent(tweet)
    if emo == False:
        return(v2)
    else:
        score = (v2 + emo) / 2
        return(score)

## Call the sentiment functions and return an array of floats
def get_sentiment(s: List[str]) -> List[float]:
    final_sentiment = [float(vader2_emo_senti(string)) for string in s]
    return (final_sentiment)



if __name__ == "__main__":
  command = sys.argv[1]
  ## Get inputs from environment and parse as string
  strings = [str(os.environ[f"INPUT_{i}"]) for i in range(int(os.environ["INPUT"]))]

  ## Define functions that can be called
  functions = {
    "get_sentiment": get_sentiment,
  }
  ## Call sentiment function
  output = functions[command](strings)
  ## Brane output lines
  print("--> START CAPTURE")
  print(yaml.dump({"output": output}))
  print("--> END CAPTURE")
