#%%
import time
import logging
import heapq as pq
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd

# local imports
from utils import *
from data_extraction import *

# # To improve on quality as search progresses, lower the better; reduces crawl speed.
# PRIORITY_QUANTILE_THRESHOLD = .90

# Set up logging
logging.basicConfig(
    filename='smart_crawl.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

def smart_crawl(SeedUrls, max_pages, target_folder, max_author_count):
    """To crawl youtube with A_Star (hill-climbing) algorithm using
    views/(likes - dislikes) score as the heuristic.

    Args:
        SeedUrls ([string]): The link to start crawling from.
        max_pages ([int]): The number of videos to crawl.
    """

    # initialize variables
    prepend = "https://www.youtube.com/watch?v="
    url_id_list = [x.split("=")[-1] for x in SeedUrls]
    all_titles = []
    scored_list = []

    # Frontier is defined as a priority queue and the seed url is added to it.
    # This is a min que and link with the lowest score will be popped first.
    # Initializing frontier with the list of SeedUrls with priority 0.
    frontier = []
    all_seed_keywords = []
    author_counts = {}
    for SeedUrl in SeedUrls:
        seed_data = get_data(SeedUrl)
        all_titles.append(seed_data["title"])
        author = seed_data["author"]
        # update author counts dict
        if author in author_counts.keys():
            author_counts[author] += 1
        else:
            author_counts[author] = 1

        seed_data["is_seed"] = True
        seed_data["priority"] = seed_data["final_score"]
        pq.heappush(frontier, (seed_data["final_score"], seed_data))
        scored_list.append(seed_data)
        all_seed_keywords += seed_data["keywords"]
    all_seed_keywords = list(set(all_seed_keywords))
    if all_titles:
        filename_strng = ' '.join(all_titles)
        filename = '_'.join(process_keywords(filename_strng)) + ".html"
    else:
        filename = "default_filename.html"
    print(f"Output File will be named: \n\t {filename}")
    # Iteration starts with atleast one element in frontier.
    # Iteration continues till num_pages reaches the max_pages (defined by user).
    # The loop is structured like bfs using a prio queue (hill-climbing) starting from the seed url.
    while (len(frontier) > 0) and (len(scored_list) <= max_pages):

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
            # Filter out the links already crawled so far.
            unique_complete_links = set(links)
            new_links = list(unique_complete_links - set(url_id_list))

        logger.info("length_new_links: %d", len(new_links))
        for link_id in new_links:
            url_id_list.append(link_id)
            # Convert ids to absolute youtube urls
            complete_new_link = prepend + link_id
            link_data = get_data(complete_new_link)
            if link_data["final_score"] == float('inf'):
                continue
            if link_data["title"] in all_titles:
                continue
            all_titles.append(link_data["title"])

            author = link_data["author"]
            # update author counts dict
            if author in author_counts.keys():
                author_counts[author] += 1
            else:
                author_counts[author] = 1

            # skip link if author count reaches maximum
            if author_counts[author] > max_author_count:
                continue

            keywords_score = get_keywords_score(all_seed_keywords, link_data["keywords"])
            priority = (link_data["final_score"] / keywords_score)
            link_data["priority"] = priority
            logger.info(f"priority: {priority}")

            pq.heappush(frontier, (priority, link_data))
            scored_list.append(link_data)

        score_df = pd.DataFrame(scored_list)
        score_df = score_df.sort_values(by='priority', ascending=True)
        score_df = score_df.reset_index(drop=True)
        df_to_html(score_df, output_file = target_folder + filename)

        # update progress
        percentage_completed = (len(score_df) / max_pages) * 100
        print("%s percent crawling complete", str(percentage_completed)[:5])
        logging.info("%s percent crawling complete", str(percentage_completed)[:5])

        # # update priority threshold based on frontier
        # if frontier:
        #     priority_threshold = get_quantile_of_frontier(frontier, PRIORITY_QUANTILE_THRESHOLD)

    logging.info("Crawling completed @ : %s.html", target_folder + "/test.html")

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--config_path",
        help="path to a configuration file for the parameters of the crawl",
        default="./configs/config.yaml"
        )
    args = parser.parse_args()

    # load config file if provided
    if args.config_path:
        config_data = load_yaml_config(args.config_path)
        # Load parameters from config
        SeedUrls = config_data.get("seedUrls", [])
        target_folder = config_data.get("outputDir", "default_outputs")
        max_pages = config_data.get("numVideos", 100)
        max_author_count = config_data.get("max_author_count", 5)

        if SeedUrls:
            if target_folder[-1]!='/':
                target_folder += '/'
            if target_folder[0]=='/':
                target_folder = target_folder[1:]
            target_folder = "./crawled_outputs/" + target_folder.lower()
            Path(target_folder).mkdir(parents=True, exist_ok=True)

            start_time = time.time()
            print("crawling ... find progress in log file: smart_crawl.log ")
            smart_crawl(SeedUrls, max_pages, target_folder, max_author_count)
            print(f"--- Crawl took {(time.time() - start_time)} seconds ---")
        else:
            print("Error: No seedUrls provided.")
    else:
        print("Error: No config file provided.")
