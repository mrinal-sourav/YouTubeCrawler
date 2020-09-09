import csv 
import re
import urllib.request 
import time 
import pandas as pd
import heapq as pq

#initializing arguments
SeedUrl = input("\n Enter the seed url for the crawl: ")
max_pages = int(input("\n Enter the number of videos to crawl (getting 100 unique links takes ~5 minutes): "))

# Defining functions 
def get_data(link): 
    '''Given a link to youtube video, extracts views, likes, dislikes info, 
    and returns a row of data as list'''
    time.sleep(1.1)
    with urllib.request.urlopen(link) as url:
        theSite=str(url.read()) 
        
        # get title
        title = re.findall('''<title>(.+?)</title>''',theSite,re.DOTALL)[0] 
        title = re.sub(r'\W+', ' ', title)
        title = title[:100]
        
        if re.findall('''"author":"(.+?)"''',theSite,re.DOTALL):
            author = re.findall('''"author":"(.+?)"''',theSite,re.DOTALL)[0]
            author = re.sub(r'\W+', ' ', author)
        else:
            author = 'NA'
            
        try:
            views = re.findall('''{["]viewCount["]:{["]simpleText["]:["](.+?) views["]}''',theSite,re.DOTALL)[0]
            likes = re.findall('''{["]accessibilityData["]:{["]label["]:["](.+?) likes["]}''',theSite,re.DOTALL)[0] 
            dislikes = re.findall('''(\d+,?\d*) dislikes["]}''',theSite,re.DOTALL)[0] 
            # if all works continue as below with calculating score
            views=int(views.replace(',', ''))
            likes=int(likes.replace(',', ''))
            dislikes=int(dislikes.replace(',', ''))
            if likes == dislikes or likes == 0:
                likes+=1
            score = views/(likes-dislikes)
            row = [title, link, score, author, views, likes, dislikes]
        except: 
            # if the above doesnt work, insert score as infinite 
            row = [title, link, float('inf'), author, 0, 0, 0]      
    return row

def smart_crawl(SeedUrl, max_pages): 
    ''' To crawl youtube with A_Star algorithm using 
    views/(likes - dislikes) score as heuristics '''
    #get SeedUrl title 
    with urllib.request.urlopen(SeedUrl) as url:
        theSite=str(url.read()) #theSite contains all the text read from current_url 
        seed_title = re.findall('''<title>(.+?)</title>''',theSite,re.DOTALL)[0]
    seed_title = re.sub(r'\W+',' ', seed_title) 

    print("\n\tCrawling started from link titled: ", seed_title[:50])
    
    # define variables and constants
    list_of_site_size =[]
    num_pages = 0
    prepend = "https://www.youtube.com/watch?v="
    urllist = []  
    scored_list = []

    #frontier is defined as a priority queue and the seed url is added to it
    frontier = []
    pq.heappush(frontier, (float('inf'), SeedUrl))

    #iteration starts with atleast one element in frontier 
    #iteration continues till num_pages reaches the max_pages (defined by user) 
    #the loop is structured like bfs using a prio queue (a*) starting from the seed url. 
    while frontier and len(urllist) <= max_pages:
        links = [] 
        _, current_url = pq.heappop(frontier) #current_url is populated starting with the seed url
        time.sleep(1.1) #wait time is added for politeness policy while crawling
        with urllib.request.urlopen(current_url) as url:
            num_pages+=1 
            theSite = str(url.read()) #theSite contains all the text read from current_url 
            links = re.findall('''"videoId":"(.+?)"''',theSite,re.DOTALL)
            complete_links = [prepend + x for x in links]
            unique_complete_links = set(complete_links)
            new_links = list(unique_complete_links - set(urllist))
            urllist += new_links 
            
        for link in new_links:
            link_data = get_data(link)
            priority = link_data[2] # set the score returned, as priority for the queue
            pq.heappush(frontier, (priority, link)) 
            scored_list.append(link_data)   
            
        # save data from dataframe
        df = pd.DataFrame(scored_list, 
                          columns=['Title', 
                                   'URL', 
                                   'Score', 
                                   'Author', 
                                   'Views', 
                                   'Likes', 
                                   'Dislikes']) 
        df = df.sort_values('Score')
        df = df.reset_index(drop=True)  
        df.to_csv('%s.csv' %seed_title[:50])

        percentage_completed = (len(scored_list) / max_pages) * 100 
        print("\n\t" + str(percentage_completed)[:5] + " percent crawling complete: CSV file named " + 
              seed_title[:30] + " created \n") 

start_time = time.time()
smart_crawl(SeedUrl, max_pages)
print("\n\t--- Crawl took %s seconds ---" % (time.time() - start_time))