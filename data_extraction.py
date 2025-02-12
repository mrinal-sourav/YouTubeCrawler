#%%
import re
import urllib.request
import time
import math
from fuzzywuzzy import process

import logging
logger = logging.getLogger(__name__)

###### CONSTANTS
# SLEEP_TIME time is added for politeness policy while crawling; do not reduce.
SLEEP_TIME = 1.02
STRING_CLIP = 60
EPSILON = 1e-9
KEYWORD_MATCH_THRESHOLD = 95
LIKES_LIMIT = 2000


# REGEX PATTERNS
LIKES_REGEX = re.compile(r'"accessibilityText":"[\d,.KMB]+ likes"}')
VIEWS_REGEX = re.compile(r'"viewCount":{"simpleText":"[\d,.KMB]+ views"')

DIGIT_WITHOUT_CHAR = re.compile(r'\d+')
DIGIT_PATTERN = re.compile(r'\d+[A-Z]')

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
        return 10 ** exponent
    else:
        return EPSILON

def extract_from_regex(regex_pattern, strng):
    match = regex_pattern.search(strng)

    if match:
        string_found = match.group(0)
        return string_found.replace(",","")
    else:
        return "No match found."

def convert_to_integer(number_str):
    """courtesy #chatGPT"""

    suffixes = {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000
    }

    if number_str[-1] in suffixes:
        multiplier = suffixes[number_str[-1]]
        return int(float(number_str[:-1]) * multiplier)
    else:
        return int(float(number_str))

def extract_integers(strng):
    number_with_char = DIGIT_PATTERN.findall(strng)
    just_number = DIGIT_WITHOUT_CHAR.findall(strng)
    if len(just_number) == 2:
        number_str = ".".join(just_number)
    else:
        number_str = just_number[0]
    if number_with_char:
        number_str += number_with_char[0][-1]
    return convert_to_integer(number_str)

def get_data(link):
    '''
    Given a link to youtube video, extracts views, likes,
    and other info (title, author, keywords) to return a row of data as dict.
    '''

    row = {
        "title": 'NA',
        "link": link,
        "final_score": float('inf'),
        "author": 'NA',
        "views":0,
        "likes":0,
        "keywords": [],
        "is_seed": False,
        "priority": float('inf')
        }

    time.sleep(SLEEP_TIME)
    try:
        with urllib.request.urlopen(link) as url:

            logger.info(f"Link = {link}")

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
            likes_strng = extract_from_regex(LIKES_REGEX, theSite)
            if likes_strng == "No match found.":
                logger.info(f"likes string not found")
                return row
            likes = extract_integers(likes_strng)
            logger.info(f"Likes = {likes}")
            if likes<LIKES_LIMIT:
                logger.info(f"likes less than {LIKES_LIMIT}")
                return row

            # get views
            views_strng = extract_from_regex(VIEWS_REGEX, theSite)
            if views_strng == "No match found.":
                logger.info(f"views string not found")
                return row
            views = extract_integers(views_strng)
            logger.info(f"Views = {views}")

            # get keywords
            keywords = re.findall('''<meta name="keywords" content="(.+?)"><''',theSite,re.DOTALL)[0]
            if keywords:
                row["keywords"] = process_keywords(keywords)
            if title:
                row["keywords"] += process_keywords(title)
            row["keywords"] = list(set(row["keywords"]))

            score = views/likes
            # dividing further by log10 of likes to prioritize higher number of likes
            row["final_score"] = score / (math.log10(likes+10)) # addding 10 to avoid divide by 0
            row["views"] = views
            row["likes"] = likes

    except:
        logger.info(f"Issue extracting data for {link}")

    return row

#%%
########## testing
# print(get_data("https://youtu.be/CVU1Mv9e-0U"))


# # %%
# x = "\"accessibilityText\":\"14 likes\"}"
# # %%
# extract_integers(x)

# %%
