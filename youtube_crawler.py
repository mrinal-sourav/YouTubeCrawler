#%%
import time
import heapq as pq
from pathlib import Path
import argparse

# local imports
from utils import *
from data_extraction import *

def smart_crawl(SeedUrl, max_pages, path_to_author_counts_dict="author_counts.json"):
    """To crawl youtube with A_Star (hill-climbing) algorithm using
    views/(likes - dislikes) score as the heuristic.

    Args:
        SeedUrl ([string]): The link to start crawling from.
        max_pages ([int]): The number of videos to crawl.
    """
    
    # get SeedUrl data
    seed_data = get_data(SeedUrl)
    seed_title = seed_data["title"]
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
    pq.heappush(frontier, (seed_data["final_score"], seed_data))

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
            link_data = get_data(link)
            if link_data["final_score"] == float('inf'):
                urllist.append(link_data["link"])
                continue
            author = link_data["author"]
            # update author counts dict
            if author in author_counts.keys():
                author_counts[author] += 1
            else:
                author_counts[author] = 1

            keywords_score = get_keywords_score(seed_keywords, link_data["keywords"])
            priority = (link_data["final_score"] / keywords_score) * author_counts[author]

            urllist.append(link_data["link"])
            median_frontier_priority = get_median_of_frontier(frontier)
            if priority <= median_frontier_priority:
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

    print(f"\n Crawling_Completed; html file written to {target_folder + seed_title}")
    print(f"Author Count updated in : {path_to_author_counts_dict}")
    with open(path_to_author_counts_dict, "w") as f:
        json.dump(author_counts, f)

if __name__ == "__main__":
    # ARGUMENTS
    SeedUrl = input("\n Enter the seed url for the crawl: ") or "https://youtu.be/fHsa9DqmId8"
    max_pages = int(input("\n Enter the number of videos to crawl (200 (default) links takes ~10 minutes): ") or "200")
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
