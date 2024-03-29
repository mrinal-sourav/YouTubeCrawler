#%%
import re
import urllib.request
import time
import math
from fuzzywuzzy import process

###### CONSTANTS
# SLEEP_TIME time is added for politeness policy while crawling; do not reduce.
SLEEP_TIME = 1.1
STRING_CLIP = 50
EPSILON = 1e-9
KEYWORD_MATCH_THRESHOLD = 80


# REGEX PATTERNS
LIKES_REGEX_PATTERN = re.compile(r'"accessibility":{"accessibilityData":{"label":"[\d,.]+ likes"}}')
VIEWS_REGEX_PATTERN = re.compile(r'"allowRatings":true,"viewCount":"[\d,.]+","author"')

# list of stop words
with open("stop_words.txt", "r") as f:
    stop_words = f.readlines()
    stop_words_list = [x.strip('\n') for x in stop_words]


###### helper functions
def process_keywords(strng):
    lowercase_string = strng.lower()
    keywords = lowercase_string.split(',')
    all_words = []
    for word in keywords:
        word = word.strip()
        if len(word) > 3:
            if ' ' in word:
                all_words += word.split(' ')
            else:
                all_words.append(word)
    filtered_keywords = set(all_words) - set(stop_words_list)
    return list(filtered_keywords)

def get_keywords_score(seed_keywords, match_keywords):
    """Extract a keyword match score.

    Args:
        seed_keywords (listOfStrings): list of processed keywords from the SeedURL
        match_keywords (listOfStrings): list of processed keywords from a crawled url

    Returns:
        keyword_score(10^count of words that match roughly):    The 10 to the power of number of words thresholded by scores as returned by fuzzywuzzy process on each Seed keyword match.

        EPSILON: If no match crosses  KEYWORD_MATCH_THRESHOLD; this has the effect of increasing the final score.
    """
    if match_keywords:
        exponent = 0
        for seed_word in seed_keywords:
            best_match, match_score = process.extractOne(seed_word,match_keywords)
            if match_score >= KEYWORD_MATCH_THRESHOLD:
                exponent += 1
        if exponent > 0:
            keyword_score = 10 ** exponent
            return keyword_score
        else:
            return EPSILON
    else:
        return EPSILON

def extract_from_regex(regex_pattern, strng):
    match = regex_pattern.search(strng)

    if match:
        string_found = match.group(0)
        return string_found.replace(",","")
    else:
        return "No match found."

def extract_integers(strng):
    pattern = re.compile(r'\d+')
    matches = pattern.findall(strng)
    return int(matches[0])

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

            # get likes
            likes_strng = extract_from_regex(LIKES_REGEX_PATTERN, theSite)
            if likes_strng == "No match found.":
                return row
            likes = extract_integers(likes_strng)
            # handle edge cases, prevent divide by zero etc.
            if likes==0:
                likes+=1

            # get views
            views_strng = extract_from_regex(VIEWS_REGEX_PATTERN, theSite)
            if views_strng == "No match found.":
                return row
            views = extract_integers(views_strng)

            # get keywords
            keywords = re.findall('''<meta name="keywords" content="(.+?)"><''',theSite,re.DOTALL)[0]
            if keywords:
                row["keywords"] = process_keywords(keywords)

            score = views/likes
            # dividing further by log10 of likes to prioritize higher number of likes
            row["final_score"] = score / (math.log10(likes+10)) # addding 10 to avoid divide by 0
            row["views"] = views
            row["likes"] = likes

    except:
        print(f"Issue extracting data for {link}")

    return row

#%%
########## testing
# print(get_data("https://youtu.be/bmUxvX2z5N0?list=RDMM"))

# %%
