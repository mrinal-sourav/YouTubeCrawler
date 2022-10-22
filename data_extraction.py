#%%
import re
from tkinter import E
import urllib.request
import time
import math
import statistics
from fuzzywuzzy import process

# CONSTANTS
# SLEEP_TIME time is added for politeness policy while crawling; do not reduce.
SLEEP_TIME = 1.1
STRING_CLIP = 50
EPSILON = 1e-9
KEYWORD_MATCH_THRESHOLD = 50

def process_keywords(strng):
    lowercase_string = strng.lower()
    keywords = lowercase_string.split(',')
    all_words = []
    for word in keywords:
        word = word.strip()
        if ' ' in word:
            all_words += word.split(' ')
        else:
            all_words.append(word)
    return list(set(all_words))

def get_keywords_score(seed_keywords, match_keywords):
    """Extract a keyword match score.

    Args:
        seed_keywords (listOfStrings): list of processed keywords from the SeedURL
        match_keywords (listOfStrings): ist of processed keywords from a crawled url
    
    Returns:
        keyword_score(0<float<=1):   The reciprocal of, the average of, thresholded match scores as returned by fuzzywuzzy process on 
                                        each Seed keyword match. 
        100: If no match crosses  KEYWORD_MATCH_THRESHOLD; this has the effect of increasing the final score.                        
    """
    match_scores = []
    for seed_word in seed_keywords:
        best_match, match_score = process.extractOne(seed_word,match_keywords)
        if match_score > KEYWORD_MATCH_THRESHOLD:
            match_scores.append(match_score)
    if match_scores:
        average_score = statistics.mean(match_scores)
        return average_score
    else:
        return EPSILON

def get_data(link):
    '''Given a link to youtube video, extracts views, likes,
    and other info (title, author, keywords) to return a row of data as dict.
    '''

    row = {
        "title": 'NA',
        "link": link,
        "final_score": float('inf'),
        "author": 'NA',
        "views":0,
        "likes":0,
        "keywords": "NA"
        }

    time.sleep(SLEEP_TIME)
    try:
        with urllib.request.urlopen(link) as url:
            theSite=str(url.read())

            # get title
            title = re.findall('''<title>(.+?)</title>''',theSite,re.DOTALL)[0]
            title = re.sub(r'\W+', ' ', title)
            row["title"] = title[:STRING_CLIP]

            # get author
            if re.findall('''"author":"(.+?)"''',theSite,re.DOTALL):
                author = re.findall('''"author":"(.+?)"''',theSite,re.DOTALL)[0]
                row["author"] = re.sub(r'\W+', ' ', author)
                row["author"] = row["author"][:STRING_CLIP]

            # get views, likes, dislikes.
            try:
                views = re.findall('''{["]viewCount["]:{["]simpleText["]:["](.+?) views["]}''',
                                    theSite,
                                    re.DOTALL)[0]
                likes = re.findall('''{\"accessibilityData\":{\"label\":\"(.+?) likes\"}''',
                                    theSite,
                                    re.DOTALL)[1]

                keywords = re.findall('''<meta name="keywords" content="(.+?)"><''',theSite,re.DOTALL)[0]

                # if all works continue as below with calculating score
                views=int(views.replace(',', ''))
                likes=int(likes.replace(',', ''))

                # handle edge cases, prevent divide by zero etc.
                if likes==0:
                    likes+=1

                score = views/likes
                # dividing further by log10 to prioritize higher number of likes
                row["final_score"] = score / (math.log10(likes+10)) # addding 10 to avoid divide by 0
                row["views"] = views
                row["likes"] = likes

                if keywords:
                    row["keywords"] = process_keywords(keywords)

            except:
                print("\n\t\t Issue Extracting data from : " + link)

    except:
        print("\n\t\t Issue opening: " + link)

    return row
#%%
########## testing 
# import json
# with open("./author_counts.json", "r") as fp:
#     author_counts = json.load(fp)

# def normalize_dictionary(dictionary):
#     factor=1.0/sum(dictionary.values())
#     normalised_dictionary = {k: v*factor for k, v in dictionary.items()}
#     return normalised_dictionary

# author_counts = normalize_dictionary(author_counts)
# link = "https://youtu.be/KFRQ61PnTVE?list=RDKFRQ61PnTVE"

# data = get_data("https://youtu.be/KFRQ61PnTVE?list=RDKFRQ61PnTVE", author_counts)

# match_string = "ninJa, undercurent"
# strOptions = process_keywords(match_string)
# # %%
# print(strOptions)
# print(get_keywords_score(data["keywords"], strOptions))

# # %%
# data["keywords"]

# %%
