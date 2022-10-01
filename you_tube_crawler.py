#%%
import re
import urllib.request
import time
import heapq as pq
from pathlib import Path
import math
import json
import argparse

# CONSTANTS
# SLEEP_TIME time is added for politeness policy while crawling; do not reduce.
SLEEP_TIME = 1.1
TITLE_CLIP = 50

# FUNCTIONS
# helper function to create hyperlinked text for html
def create_anchor(link_data):
    """Helper function to generate anchored html from link data.

    Args:
        link_data ([list]): A row of data as list

    Returns:
        [list]: Same data with hyperlink
    """
    title = link_data[0]
    url = link_data[1]
    hyperlink = '<a href=' + url + ' target="_blank">' + title + '</a>'
    # clip author names for neater presentation
    if len(link_data[3])>50:
        link_data[3] = link_data[3][:50]
    res = [hyperlink] + link_data[2:]
    return res

# To get score from the scored list (with anchored title).
# This is to enable sorting of the list containing data.
def get_score(row):
    return row[1]

def get_author_counts_dict(path_to_author_counts_dict="author_counts.json"):
    try:
        with open(path_to_author_counts_dict, 'r') as fp:
            author_counts_dict = json.load(fp)
        return author_counts_dict
    except Exception:
        return {}

# To create html table from data and write to filename
def write_to_html(filename, sorted_list):
    table = "<table>\n"
    # Create the table's column headers
    header = ['Title', 'Score', 'Author', 'Views', 'Likes']
    table += "  <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"

    # Create the table's row data
    for row in sorted_list:
        table += "  <tr>\n"
        for column in row:
            table += "    <td>{0}</td>\n".format(column)
        table += "  </tr>\n"

    table += "</table>"

    with open(target_folder+filename, "w") as f:
        f.writelines(table)

def get_data(link, normalized_author_counts):
    '''Given a link to youtube video, extracts views, likes,
    and other info (title, author) to return a row of data as list.
    normalized_author_counts is used to weight the scores of frequently 
    occuring authors in all crawls done by the user.'''

    row = ['NA', link, float('inf'), 'NA', 0, 0, 0]
    time.sleep(SLEEP_TIME)
    try:
        with urllib.request.urlopen(link) as url:
            theSite=str(url.read())

            # get title
            title = re.findall('''<title>(.+?)</title>''',theSite,re.DOTALL)[0]
            title = re.sub(r'\W+', ' ', title)
            title = title[:TITLE_CLIP]

            # get author
            if re.findall('''"author":"(.+?)"''',theSite,re.DOTALL):
                author = re.findall('''"author":"(.+?)"''',theSite,re.DOTALL)[0]
                author = re.sub(r'\W+', ' ', author)
            else:
                author = 'NA'

            # get views, likes, dislikes.
            try:
                views = re.findall('''{["]viewCount["]:{["]simpleText["]:["](.+?) views["]}''',
                                    theSite,
                                    re.DOTALL)[0]
                likes = re.findall('''{\"accessibilityData\":{\"label\":\"(.+?) likes\"}''',
                                    theSite,
                                    re.DOTALL)[1]

                # if all works continue as below with calculating score
                views=int(views.replace(',', ''))
                likes=int(likes.replace(',', ''))

                # handle edge cases, prevent divide by zero etc.
                if likes==0:
                    likes+=1

                score = views/likes
                # dividing furtther by log10 to prioritize higher number of likes
                final_score = score / (math.log10(likes+10)) # addding 10 to avoid divide by 0

                # multiply scores by author scount if author hass been crawled in the past before
                # this reduces the priority of popular authors
                if author in normalized_author_counts.keys():
                    final_score = final_score*normalized_author_counts[author]

                row = [title, link, final_score, author, views, likes]
            except:
                # if the above doesnt work, insert score as infinite
                row = [title, link, float('inf'), author, 0, 0]
    except:
        print("\n\t\t Issue opening: " + link)

    return row

def normalize_dictionary(dictionary):
    factor=1.0/sum(dictionary.itervalues())
    normalised_dictionary = {k: v*factor for k, v in dictionary.iteritems()}
    return normalised_dictionary

def smart_crawl(SeedUrl, max_pages, path_to_author_counts_dict="author_counts.json"):
    """To crawl youtube with A_Star (hill-climbing) algorithm using
    views/(likes - dislikes) score as the heuristic.

    Args:
        SeedUrl ([string]): The link to start crawling from.
        max_pages ([int]): The number of videos to crawl.
    """
    author_counts = get_author_counts_dict(path_to_author_counts_dict)
    # normalize author counts
    normalized_author_counts = normalize_dictionary(author_counts)
    # get SeedUrl data
    seed_data = get_data(SeedUrl, normalized_author_counts)
    seed_title = seed_data[0][:TITLE_CLIP] # clipping to first 50 chars

    print("\n\tCrawling started from link titled: ", seed_title)

    # define variables and constants
    prepend = "https://www.youtube.com/watch?v="
    urllist = []
    scored_list = []
    if seed_data[3] in author_counts.keys():
        author_counts[seed_data[3]] += 1
    else:
        author_counts[seed_data[3]] = 1

    # Frontier is defined as a priority queue and the seed url is added to it.
    # This is a min que and link with the lowest score will be popped first.
    frontier = []
    pq.heappush(frontier, (seed_data[2], seed_data))

    # Iteration starts with atleast one element in frontier.
    # Iteration continues till num_pages reaches the max_pages (defined by user).
    # The loop is structured like bfs using a prio queue (a*) starting from the seed url.
    while frontier and (len(scored_list) <= max_pages):
        links = []
        # current_url is populated starting with the seed url
        _ , current_node = pq.heappop(frontier)
        current_url = current_node[1]
        # wait time is added for politeness policy while crawling
        time.sleep(SLEEP_TIME)
        with urllib.request.urlopen(current_url) as url:
            # Read all the text read from current_url into theSite
            theSite = str(url.read())
            # Extract all other video ids from the current page.
            links = re.findall('''"videoId":"(.+?)"''',theSite,re.DOTALL)
            # Convert ids to absolute youtube urls
            complete_links = [prepend + x for x in links]
            # Filter out the links already crawled so far.
            unique_complete_links = set(complete_links)
            new_links = list(unique_complete_links - set(urllist))

        for link in new_links:
            link_data = get_data(link, normalized_author_counts)
            if link_data[2] == float('inf'):
                urllist.append(link_data[1])
                continue
            # set the score returned in link data, as priority for the queue
            priority = link_data[2]
            author = link_data[3]
            # update author counts dict
            if author in author_counts.keys():
                author_counts[author] += 1
            else:
                author_counts[author] = 1

            urllist.append(link_data[1])
            pq.heappush(frontier, (priority, link_data))
            scored_list.append(create_anchor(link_data))

        # sort data and write to html
        scored_list.sort(key=get_score)
        write_to_html(seed_title + '.html', scored_list)

        # update progress
        percentage_completed = (len(scored_list) / max_pages) * 100
        print("\n\t" + str(percentage_completed)[:5]
         + " percent crawling complete: html file named "
         + seed_title + " updated \n")

    print(f"\n Crawling_Completed; html file written to {target_folder + seed_title}")
    print(f"Author Count updated in : {path_to_author_counts_dict}")
    with open(path_to_author_counts_dict, "w") as f:
        json.dump(author_counts, f)

if __name__ == "__main__":
    # ARGUMENTS
    SeedUrl = input("\n Enter the seed url for the crawl: ") or "https://youtu.be/fHsa9DqmId8"
    max_pages = int(input("\n Enter the number of videos to crawl (120 (default) links takes ~10 minutes): ") or "120")
    target_folder = input("\n Enter the target folder for the resulting html: ") or "./crawled_outputs/default_outputs/"
    if target_folder[-1]!='/':
        target_folder += '/'
    if target_folder[0]=='/':
        target_folder = target_folder[1:]
    target_folder = "./crawled_outputs/" + target_folder
    Path(target_folder).mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    smart_crawl(SeedUrl, max_pages)
    print("\n\t--- Crawl took %s seconds ---" % (time.time() - start_time))
