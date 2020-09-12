 
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

  Enter the seed url for the crawl: https://youtu.be/kD5yc1LQrpQ

 Enter the number of videos to crawl (getting 100 links takes ~10 minutes): 100

        Crawling started from link titled:  Michio Kaku Future of Humans Aliens Space Travel a

        13.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


                 Issue opening: https://www.youtube.com/watch?v=4cX-z-MyNrU

        15.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        28.99 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        28.99 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        41.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        45.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        56.99 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        63.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        70.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        73.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        73.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        80.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        94.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        107.0 percent crawling complete: html file named Michio Kaku Future of Humans Aliens Space Travel a updated 


        --- Crawl took 757.9418661594391 seconds ---

 - IMPORTANT NOTES: 

	WAIT TIME IS ADDED FOR "POLITENESS POLICY" WHILE CRAWLING. (set to 1.2 seconds) 
	PLEASE DO NOT REDUCE IT LEST YOUTUBE THINKS YOU ARE A BOT. 

	It is advisable to crawl not more than 150 links as the subject matter of the SeedURL
	may diverge when the depth of crawl increases. 

	Actual number of urls in the crawled file may have slightly more links than specified. Links gathered may 
	differ based on geographic location crawled from.   

	Code for writing to html is inspired from: 
	https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/  



