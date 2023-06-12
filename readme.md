## What it does
This program will take a crawl facetuneapp's blog and create a word cloud based on frequency

## Requirements:
1. requests
2. numpy
3. BeautifulSoup
4. pandas
5. matplotlib
6. pillow
7. wordcloud

copy these to install each package <br>
pip install requests <br>
pip install numpy <br>
pip install beautifulsoup4 <br>
pip install pillow <br>
pip install matplotlib <br>
pip install wordcloud <br>

## How to use:
only files you need are redditScraper.py and noiseWords.csv. The others will be written by the program

1. noiseWords.csv can be edited to remove unwanted words
2. Change the list named filters in main() to get results from desired blog categories
3. wordCloud function has wordcloud size and color settings
4. Run facetuneScraper.py
