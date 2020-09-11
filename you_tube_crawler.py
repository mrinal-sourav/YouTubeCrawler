import re
import urllib.request 
import time 
import heapq as pq

# ARGUMENTS
SeedUrl = input("\n Enter the seed url for the crawl: ")
max_pages = int(input("\n Enter the number of videos to crawl (getting 100 unique links takes ~7 minutes): "))

# CONSTANTS 
SLEEP_TIME = 1.2
TITLE_CLIP = 50

# FUNCTIONS 

# helper function to create hyperlinked text for html 
def create_anchor(link_data):
    title = link_data[0] 
    url = link_data[1] 
    hyperlink = '<a href=' + url + '>' + title + '</a>' 
    res = [hyperlink] + link_data[2:]
    return res 

# to get score from scored list (with anchored title)
def get_score(row):
    return row[1]

# to create html table from data and write to filename
def write_to_html(filename, sorted_list):
    table = "<table>\n"
    # Create the table's column headers
    header = ['Title', 'Score', 'Author', 'Views', 'Likes', 'Dislikes']
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

    with open(filename, "w") as f:
        f.writelines(table)

def get_data(link): 
    '''Given a link to youtube video, extracts views, likes, dislikes,  
    and other info (title, author) to return a row of data as list'''
    
    row = ['NA', link, float('inf'), 'NA', 0, 0, 0] 
    
    # wait time is added for politeness policy while crawling; do not change. 
    time.sleep(SLEEP_TIME)
    
    try:
        with urllib.request.urlopen(link) as url:
            theSite=str(url.read()) 

            # get title
            title = re.findall('''<title>(.+?)</title>''',theSite,re.DOTALL)[0] 
            title = re.sub(r'\W+', ' ', title)
            title = title[:TITLE_CLIP]

            if re.findall('''"author":"(.+?)"''',theSite,re.DOTALL):
                author = re.findall('''"author":"(.+?)"''',theSite,re.DOTALL)[0]
                author = re.sub(r'\W+', ' ', author)
            else:
                author = 'NA'

            try:
                views = re.findall('''{["]viewCount["]:{["]simpleText["]:["](.+?) views["]}''',
                                   theSite,
                                   re.DOTALL)[0]
                likes = re.findall('''{["]accessibilityData["]:{["]label["]:["](.+?) likes["]}''',
                                   theSite,
                                   re.DOTALL)[0] 
                dislikes = re.findall('''(\d+,?\d*) dislikes["]}''',
                                      theSite,
                                      re.DOTALL)[0] 

                # if all works continue as below with calculating score
                views=int(views.replace(',', ''))
                likes=int(likes.replace(',', ''))
                dislikes=int(dislikes.replace(',', ''))

                # handle edge cases, prevent divide by zero etc. 
                if likes == dislikes or likes == 0:
                    likes+=1

                score = views/(likes-dislikes)
                row = [title, link, score, author, views, likes, dislikes]

            except: 
                # if the above doesnt work, insert score as infinite 
                row = [title, link, float('inf'), author, 0, 0, 0]    
    except:
        print("\n\t\t Issue opening: " + link)
    return row

def smart_crawl(SeedUrl, max_pages): 
    ''' To crawl youtube with A_Star algorithm using 
    views/(likes - dislikes) score as heuristics '''
    
    # get SeedUrl data
    seed_data = get_data(SeedUrl)
    seed_title = seed_data[0][:TITLE_CLIP] # clipping to first 50 chars

    print("\n\tCrawling started from link titled: ", seed_title)
    
    # define variables and constants
    list_of_site_size =[]
    prepend = "https://www.youtube.com/watch?v="
    urllist = []  
    scored_list = []
    authors = [seed_data[3]] 

    # Frontier is defined as a priority queue and the seed url is added to it.
    # This is a min que and link with the lowest score will be popped first.  
    frontier = []
    pq.heappush(frontier, (seed_data[2], seed_data))

    # Iteration starts with atleast one element in frontier. 
    # Iteration continues till num_pages reaches the max_pages (defined by user).
    # The loop is structured like bfs using a prio queue (a*) starting from the seed url. 
    while frontier and len(scored_list) <= max_pages:
        links = [] 
        # current_url is populated starting with the seed url
        _ , current_node = pq.heappop(frontier) 
        current_url = current_node[1]
        # wait time is added for politeness policy while crawling
        time.sleep(SLEEP_TIME) 
        with urllib.request.urlopen(current_url) as url: 
            theSite = str(url.read()) # theSite contains all the text read from current_url 
            links = re.findall('''"videoId":"(.+?)"''',theSite,re.DOTALL)
            complete_links = [prepend + x for x in links]
            unique_complete_links = set(complete_links)
            new_links = list(unique_complete_links - set(urllist)) 
            
        for link in new_links:
            link_data = get_data(link)
            # set the score returned in link data, as priority for the queue
            priority = link_data[2] 
            author = link_data[3]
            if author not in authors:
                urllist.append(link_data[1])
                authors.append(author)
                pq.heappush(frontier, (priority, link_data)) 
                scored_list.append(create_anchor(link_data))   
        
        # sort data and write to html
        scored_list.sort(key=get_score)
        write_to_html(seed_title + '.html', scored_list)
        
        # update progress 
        percentage_completed = (len(scored_list) / max_pages) * 100 
        print("\n\t" + str(percentage_completed)[:5] + " percent crawling complete: html file named " + 
              seed_title + " updated \n")

start_time = time.time()
smart_crawl(SeedUrl, max_pages)
print("\n\t--- Crawl took %s seconds ---" % (time.time() - start_time))