This YouTube crawler crawls youtube starting from a SeedUrl provided by the user. It uses a hillclimbing algorithm based on views/(likes) score of videos. The hypotheses being; videos with good content will have more likes per views. Here's a video from Veritasium that explains how YouTube does not do a great job of providing users with good recommendations: https://youtu.be/fHsa9DqmId8
As such, users may benifit from a rather explorative approach from this crawler to diversify their finds on Youtube.
Additionaly, keyword based matching, and author count based suppression, are used to further refine the results.

 - Code requirements are captured in "requirements.txt",
 other imports should be inbuilt in python 3.5 +.

 - to install requirements:
 pip install -r requirements.txt

 - Uses "argparse" to parse input arguments from command line.
 - Access help for the inputs using "python3 you_tube_crawler -h", like so:
	python3 youtube_crawler.py -h
usage: youtube_crawler.py [-h] [-s SEEDURL] [-o OUTPUTDIR] [-n NUMVIDEOS]

optional arguments:
  -h, --help            show this help message and exit
  -s SEEDURL, --seedUrl SEEDURL
                        The seed url to start the crawling from.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output directory for the resulting html.
                        Defaults to ./crawled_outputs/default_outputs/
  -n NUMVIDEOS, --numVideos NUMVIDEOS
                        the number of videos to crawl : (200 (default) links
                        takes ~10 minutes)
  -a MAXAUTHORCOUNT, --maxAuthorCount MAXAUTHORCOUNT
                        maximum author count to skip crawling videos of the
                        same auther beyong this number

 - Outputs:
	A sorted html file; written to the outputDir provided in "crawled_outputs" folder.
       Format of the output:
		Video Title (with hyperlink that opens the video on a new tab on click), Score, Author, Views, Likes, Dislikes

	Score is calculated by the ratio:

		No. of Views / (Likes*log10(likes))
		Other factors that effect the final priority is a keyword matching algorithm and
		the author count (as more videos from the same author accumulates, priority for the same auther reduces)

	The smaller this number, the "better" the video.
	If EVERY person who views a video also hits "like", this score will approach 1.

 - Sample command (Updated 25th Feb 2023):
	python3 youtube_crawler.py -s https://youtu.be/ROEL3bOWk80 -o music/english
	crawling ... find progress in log file: smart_crawl.log
	--- Crawl took 1207.4183235168457 seconds ---

	Log file contains:

	2024-06-24 12:20:01,824 - INFO - Crawling started with seed URL: https://youtu.be/ROEL3bOWk80
	2024-06-24 12:20:03,331 - INFO - Link = https://youtu.be/ROEL3bOWk80
	2024-06-24 12:20:03,927 - INFO - Likes = 37000
	2024-06-24 12:20:03,928 - INFO - Views = 2709839
	2024-06-24 12:20:03,929 - INFO - Crawling started from link titled: Nothing But Thieves Broken Machine Live for IAMWHO
	2024-06-24 12:20:07,378 - INFO - Link = https://www.youtube.com/watch?v=I6g-FUVDdxw
	2024-06-24 12:20:08,100 - INFO - Likes = 39000
	2024-06-24 12:20:08,101 - INFO - Views = 4436747

	......

	2024-06-24 12:20:54,685 - INFO - 7.000 percent crawling complete
	2024-06-24 12:20:54,685 - INFO - File updated @ : /home/mrinal/Documents/Projects/YouTubeCrawler/crawled_outputs/music/english/Nothing But Thieves Broken Machine Live for IAMWHO.html

	......

 - IMPORTANT NOTES:

	WAIT TIME IS ADDED FOR "POLITENESS POLICY" WHILE CRAWLING. (set to 1.1 seconds)
	PLEASE DO NOT REDUCE IT LEST YOUTUBE THINKS YOU ARE A BOT.

       - General Notes:
	 - Actual number of urls in the crawled file may have slightly more links than specified.
        - Links gathered may differ based on geographic location crawled from.
        - Some popular videos by location may still show up despite little relation to the source link provided.
        - Time taken and scores vary depending on factors like the stats for the source video provided, vpn etc.

	Code for writing to html is inspired from:
	https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/



