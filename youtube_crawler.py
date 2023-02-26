#%%
import time
import heapq as pq
from pathlib import Path
import argparse

# local imports
from utils import *
from data_extraction import *

from argparse import ArgumentParser

PRIORITY_QUANTILE_THRESHOLD = .75 # To improve on quality as search progresses

def smart_crawl(SeedUrl, max_pages):
    """To crawl youtube with A_Star (hill-climbing) algorithm using
    views/(likes - dislikes) score as the heuristic.

    Args:
        SeedUrl ([string]): The link to start crawling from.
        max_pages ([int]): The number of videos to crawl.
    """

    # get SeedUrl data
    seed_data = get_data(SeedUrl)
    seed_title = seed_data["title"]
    if seed_data["keywords"] == "NA":
        seed_keywords = process_keywords(seed_data["title"])
    else:
        seed_keywords = seed_data["keywords"]

    print("\n\tCrawling started from link titled: ", seed_title)

    # define variables and constants
    prepend = "https://www.youtube.com/watch?v="
    urllist = [SeedUrl]
    scored_list = []
    author_counts = {seed_data["author"]:1}
    # normalize author counts

    # Frontier is defined as a priority queue and the seed url is added to it.
    # This is a min que and link with the lowest score will be popped first.
    frontier = []
    seed_priority = seed_data["final_score"]
    # define priority/score threshold for the queue
    priority_threshold = float('inf')
    pq.heappush(frontier, (seed_priority, seed_data))

    # Iteration starts with atleast one element in frontier.
    # Iteration continues till num_pages reaches the max_pages (defined by user).
    # The loop is structured like bfs using a prio queue (a*) starting from the seed url.
    while frontier and (len(scored_list) <= max_pages):
        # current_url is populated starting with the seed url
        _ , current_node = pq.heappop(frontier)
        current_url = current_node["link"]
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
            urllist.append(link)
            link_data = get_data(link)
            if link_data["final_score"] == float('inf'):
                continue
            author = link_data["author"]
            # update author counts dict
            if author in author_counts.keys():
                author_counts[author] += 1
            else:
                author_counts[author] = 1

            if link_data["keywords"] == "NA":
                link_keywords = process_keywords(link_data["title"])
            else:
                link_keywords = link_data["keywords"]

            keywords_score = get_keywords_score(seed_keywords, link_keywords)
            priority = (link_data["final_score"] / keywords_score) * author_counts[author]

            if priority <= priority_threshold:
                pq.heappush(frontier, (priority, link_data))
                scored_list.append(create_anchor(link_data))

        # sort data and write to html
        scored_list.sort(key=get_score)
        write_to_html(target_folder, seed_title + '.html', scored_list)

        # update progress
        percentage_completed = (len(scored_list) / max_pages) * 100
        print("\n\t" + str(percentage_completed)[:5]
         + " percent crawling complete: html file named "
         + seed_title + " updated \n")

        # update priority threshold based on frontier
        priority_threshold = get_quantile_of_frontier(frontier, PRIORITY_QUANTILE_THRESHOLD)

    print(f"\n Crawling completed; html file written to {target_folder + seed_title}")

if __name__ == "__main__":
    # ARGUMENTS
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--seedUrl",
        help="The seed url to start the crawling from.",
        default="https://youtu.be/fHsa9DqmId8"
        )
    parser.add_argument(
        "-o",
        "--outputDir",
        help="Path to the output directory for the resulting html. Defaults to ./crawled_outputs/default_outputs/",
        default="default_outputs/"
        )
    parser.add_argument(
        "-n",
        "--numVideos",
        type=int,
        help="the number of videos to crawl : (200 (default) links takes ~10 minutes)",
        default=200
        )

    args = parser.parse_args()
    SeedUrl = args.seedUrl
    target_folder = args.outputDir
    max_pages = args.numVideos

    if target_folder[-1]!='/':
        target_folder += '/'
    if target_folder[0]=='/':
        target_folder = target_folder[1:]
    target_folder = "./crawled_outputs/" + target_folder.lower()
    Path(target_folder).mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    smart_crawl(SeedUrl, max_pages)
    print("\n\t--- Crawl took %s seconds ---" % (time.time() - start_time))
