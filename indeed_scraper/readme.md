# Module Dependencies

## !!! I highly recommend to create a new environment before installing these dependencies !!!

pandas
selenium
requests
bs4
time
re
math
nltk
matplotlib
random
datetime
selenium
# Intro

The goal of this project is to scrape data from Indeed.com for up to 50 data science related resumes for every state.

From each resume, the resume title is stored, the state is stored, the data science skills that appear are marked as 1, and the data science skills that don't appear are marked as 0.

To prevent the ip-address from getting blocked, the sleep time is randomized between each request

A set of randomly generated headers are generated and cycled between to further obfuscate the connection.

# Process

## Obtaining Good and Fast Ip Addresses

### Open make_headers.ipynb:  (using python 2)

Run the file to make 1000 headers that stores them in a text file called headers.txt in the monster_scraper folder.

### Open break_ip_text_files_onto_n_pats.ipynb:  (using python 2)

Go to https://www.proxy-list.download/HTTPS and https://www.proxy-list.download/HTTP and download their US filtered proxies from the page into the SetUpProxies folder, naming the files HttpsProxyList.txt and HttpProxyList.txt, respectively.

Run the file and it will break the HttpProxyList.txt and HttpsProxyList.txt files into 3 parts each and store them in the folder called proxyLists.


### Open rotating_proxy_crawler_0, rotating_proxy_crawler_1, and rotating_proxy_crawler_2  (using python 2)

Run these these files simutaneously.

They will test all of the proxy connections and delete all of the bad or slow-connecting proxies and add the filtered oned to the files filtered_http_proxys.txt and filtered_https_proxys.txt

## Scraping Monster

### Open data_scientist.txt in the folder skill_lists

Insert a comma separated list of skills to be searched for in each job description.

### Open MonsterScraper_forEveryState_Refactored.ipynb:  (using python 2)

Run this file.

The program will search the term 'Data Scientist' for a state on Monster.com and gather all of the resume links from the first page.

Then The program will access each resume url, filter the text, and check if the words from the dictionary exist in the text.

When finished, it will store the resume title, the state, and the skills data in the final pandas dataframe in a file called scraped_resume_data_(todays_date).txt scraped_resume_data folder.

## Analyzing the Data

### Open Analysis.ipynb (using python 3)

Run this file from top to bottom.

Read and run each of the cells and the file will show some histograms and network graphs for the data.

The figures that are generated are saved in the figures folder.





