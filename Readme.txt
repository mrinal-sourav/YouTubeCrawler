 
 - Code requires the following imports; default python3 installation should have them all :

import re
import urllib.request 
import time 
import heapq as pq
 
 - Inputs: 
	A Seed URL from youtube 
	Number of links/videos to crawl

 - Outputs: 
	A sorted html file with video data in the following format:
		Video Title (with hyperlink), Score, Author, Views, Likes, Dislikes 

	
	Score is calculated by the ratio:

		No. of Views / (Likes - Dislikes)

	The smaller this number, the "better" the video. 
	If EVERY person who views a video also hits "like", this score will be 1. 
	Justin Bieber may come up in negative (and on the top) as he has more dislikes than likes for 
	some of his videos! Ignore negatives and look for videos with large view count but small score. 

 - Sample command (Updated 9th Septtember 2020): 

	Open command prompt or terminal and "cd" into the directory with the code, then type and enter:
	
	python3 you_tube_crawler.py 

- You should get something like: 

 Enter the seed url for the crawl: https://youtu.be/XEb7eGVWEJc

 Enter the number of videos to crawl (getting 100 unique links takes ~7 minutes): 100

        Crawling started from link titled:  Story Of Wick YouTube

        12.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        33.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        37.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        47.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        64.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        77.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        93.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        109.0 percent crawling complete: html file named Story Of Wick YouTube updated 


        --- Crawl took 439.1534779071808 seconds ---

 - IMPORTANT NOTES: 

	WAIT TIME IS ADDED FOR "POLITENESS POLICY" WHILE CRAWLING. (set to 1.2 seconds) 
	PLEASE DO NOT REDUCE IT LEST YOUTUBE THINKS YOU ARE A BOT. 

	It is advisable to crawl not more than 150 links as the subject matter of the SeedURL
	may diverge when the depth of crawl increases. 

	Actual number of urls in the crawled file may have slightly more links than specified. Links gathered may 
	differ based on geographic location crawled from.   

	Code for writing to html is inspired from: 
	https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/  



