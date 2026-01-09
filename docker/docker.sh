docker run -it --rm \
-v /home/mrinal/projects/YouTubeCrawler/:/home/youtube:rw \
-p 8080:80 \
--entrypoint=bash \
--name youtube_con \
youtube/crawl:latest
