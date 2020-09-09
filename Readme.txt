 
 - Code requires the following imports:

import csv 
import re
import urllib.request 
import time 
import pandas as pd
import heapq as pq
 
 - Inputs: 
	A Seed URL from youtube 
	Number of links/videos to crawl

 - Outputs: 
	A sorted csv file with video data in the following format:
		Video Title, Video link, Score, Author, Views, Likes, Dislikes 

	
	Score is calculated by the ratio:

		No. of Views / (Likes - Dislikes)

	The smaller this number, the "better" the video. 
	If EVERY person who views a video also hits "like", this score will be 1. 
	Justin Bieber may come up in negative (and on the top) as he has more dislikes than likes for 
	some of his videos! Ignore negatives and look for videos with large view count but small score. 

 - Sample command (Updated 20th March 2018): 

	Open command prompt or terminal and "cd" into the directory with the code, then type and enter:
	
	python3 you_tube_crawler.py 

- You should get something like: 

 Enter the seed url for the crawl: https://www.youtube.com/c/TED/videos?view=0&sort=p&flow=grid

 Enter the number of videos to crawl: 100

        30.0 percent crawling complete: CSV file named TED YouTube created 


        49.0 percent crawling complete: CSV file named TED YouTube created 


        69.0 percent crawling complete: CSV file named TED YouTube created 


        87.0 percent crawling complete: CSV file named TED YouTube created 


        94.0 percent crawling complete: CSV file named TED YouTube created 


        98.0 percent crawling complete: CSV file named TED YouTube created 


        104.0 percent crawling complete: CSV file named TED YouTube created 


        --- Crawl took 302.28309321403503 seconds ---

 - IMPORTANT NOTES: 

	WAIT TIME IS ADDED FOR "POLITENESS POLICY" WHILE CRAWLING. (updated from 2 seconds to 1.1 seconds) 
	PLEASE DO NOT REDUCE IT LEST YOUTUBE THINKS YOU ARE A BOT. 

	Actual number of urls in the crawled file may have slightly more links than specified. Links gathered may 
	differ based on geographic location crawled from.   

 - TIP: 
	Once you have the csv file from a crawl, look for videos with relatively large views 
	that appear towards the top. 


