This YouTube crawler crawls youtube starting from a SeedUrl provided by the user. It uses a hillclimbing algorithm based on views/(likes) score of videos. The hypotheses being; videos with good content will have more likes per views. Here's a video from Veritasium that explains how YouTube does not do a great job of providing users with good recommendations: https://youtu.be/fHsa9DqmId8
As such, users may benifit from a rather explorative approach from this crawler to diversify their finds on Youtube.
Addistionaly, keyword based matching, and author count based suppression, are used to further refine the results.

 - Code requirements are captured in "requirements.txt", 
 other imports should be inbuilt in python 3.5 +. 

 - to install requirements:
 pip install -r requirements.txt
 
 - Inputs: 
	- A Seed URL from youtube 
	- Number of links/videos to crawl 
	- Target Folder: The folder to write the resulting file to. 
		This enables creating a heirarchy of topics on the user's local system.   

 - Outputs:
	A sorted html file with video data in the following format:
		Video Title (with hyperlink), Score, Author, Views, Likes, Dislikes 
	
	Score is calculated by the ratio:

		No. of Views / (Likes*log10(likes))
		Updated to (Views/Likes) since YouTube decided to remove dislikes

	The smaller this number, the "better" the video. 
	If EVERY person who views a video also hits "like", this score will be 1.

 - Sample command (Updated 21st October 2020): 

	Open command prompt or terminal and "cd" into the directory with the code, then type and enter:
	
	python3 you_tube_crawler.py 

- You should get something like: 

  Enter the seed url for the crawl: https://www.youtube.com/c/VEVO/videos?view=0&sort=p&flow=grid

 Enter the number of videos to crawl (120 (default) links takes ~10 minutes): 

 Enter the max. num. of times you want to see authors repeat (default=3): 

 Enter the target folder for the resulting html: outputs/music

        Crawling started from link titled:  Vevo YouTube

        2.5 percent crawling complete: html file named Vevo YouTube updated 


        17.5 percent crawling complete: html file named Vevo YouTube updated 


        33.33 percent crawling complete: html file named Vevo YouTube updated 


        43.33 percent crawling complete: html file named Vevo YouTube updated 


        56.66 percent crawling complete: html file named Vevo YouTube updated 


        70.0 percent crawling complete: html file named Vevo YouTube updated 


        82.5 percent crawling complete: html file named Vevo YouTube updated 


        87.5 percent crawling complete: html file named Vevo YouTube updated 


        97.5 percent crawling complete: html file named Vevo YouTube updated 


        108.3 percent crawling complete: html file named Vevo YouTube updated 


        --- Crawl took 531.0542154312134 seconds ---

 - IMPORTANT NOTES: 

	WAIT TIME IS ADDED FOR "POLITENESS POLICY" WHILE CRAWLING. (set to 1.2 seconds) 
	PLEASE DO NOT REDUCE IT LEST YOUTUBE THINKS YOU ARE A BOT. 

	Actual number of urls in the crawled file may have slightly more links than specified. Links gathered may 
	differ based on geographic location crawled from.   

	Code for writing to html is inspired from: 
	https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/  



