This YouTube crawler crawls youtube starting from a SeedUrl provided by the user. It uses a hillclimbing algorithm based on views/(likes) score of videos. The hypotheses being; videos with good content will have more likes per views. Here's a video from Veritasium that explains how YouTube does not do a great job of providing users with good recommendations: https://youtu.be/fHsa9DqmId8
As such, users may benifit from a rather explorative approach from this crawler to diversify their finds on Youtube.
Additionaly, keyword based matching, and author count based suppression, are used to further refine the results.

 - Code requirements are captured in "requirements.txt",
 other imports should be inbuilt in python 3.5 +.

 - to install requirements:
 pip install -r requirements.txt

 - Uses "argparse" to parse input arguments from command line.
 - Argparse expects a path to a config file.
 - config file should contain the following: 
		seedUrls:
		- "https://youtu.be/ONVpFtiD-fo"
		- "https://youtu.be/P_fHJIYENdI"
		outputDir: "knowledge/science/"
		numVideos: 500
		maxAuthorCount: 5

		seedUrls - One or more links to youtube videos can be
					added (preferrable around similar topics)

		outputDir - where the final html will be written
		numVideos - number of videos to crawl
		maxAuthorCount - number of times author can be
						allowed to repeat in the results

 - Outputs:
	A sorted html file; written to the outputDir provided in "crawled_outputs" folder.
       Format of the output:
		Video Title (with hyperlink that opens the video on a new tab on click), Score, Author, Views, Likes, keywords, is_seed, priority (results are sorted by this key)

	Score is calculated by the ratio:

		No. of Views / (Likes*log10(likes))
			- 	The smaller this number, the "better" the video.
				If EVERY person who views a video also hits "like", this score will approach 1.

		A keyword matching algorithm also influences the priority of the crawl,
		where the keywords of the seedUrls are matched against the keywords of each other
		video in the crawl.



 - Sample command (Updated 12th Feb 2025):
	$python3 youtube_crawler.py

	crawling ... find progress in log file: smart_crawl.log 
	Output File will be named: 
			radio_triple_j_bbc_mahogany_deezer_1.html
	HTML file './crawled_outputs/music/english/radio/radio_triple_j_bbc_mahogany_deezer_1.html' has been created successfully.
	0.4 % crawling complete
	HTML file './crawled_outputs/music/english/radio/radio_triple_j_bbc_mahogany_deezer_1.html' has been created successfully.
	0.899 % crawling complete
	HTML file './crawled_outputs/music/english/radio/radio_triple_j_bbc_mahogany_deezer_1.html' has been created successfully.
	1.400 % crawling complete
	HTML file './crawled_outputs/music/english/radio/radio_triple_j_bbc_mahogany_deezer_1.html' has been created successfully.
	1.9 % crawling complete
	HTML file './crawled_outputs/music/english/radio/radio_triple_j_bbc_mahogany_deezer_1.html' has been created successfully.
	3.300 % crawling complete
	.....

	................................................................

		--- Crawl took 1207.4183235168457 seconds ---

	Alternately, the "smart_crawl.log" file can be referred to for detailed progress with individual urls.

 - IMPORTANT NOTES:

	WAIT TIME IS ADDED FOR "POLITENESS POLICY" WHILE CRAWLING. (set to 1.1 seconds)
	PLEASE DO NOT REDUCE IT LEST YOUTUBE THINKS YOU ARE A BOT.

    - General Notes:
	 	- Actual number of urls in the crawled file may have slightly more links than specified.
        - Links gathered may differ based on geographic location crawled from.
        - Some popular videos by location may still show up despite little relation to the source link provided.
        - Time taken and scores vary depending on factors like the stats for the source video provided, vpn etc.
		- One can also crawl the channel's video page, e.g.:
		https://www.youtube.com/@cokestudio/videos
		 but it will be helpful to also add particular videos from the channel as seed to extract relevant keywords.
