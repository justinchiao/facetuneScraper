import requests
import string
import re
import csv
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
import numpy as np
import time
import random
import copy
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

start_time = time.time()

#Opens CSV with subreddit names and search words and sorst into subs and words respectively

def crawlBlog(filters):
    #https://www.facetuneapp.com/blog?a25596b1_page=23

    blogPosts = []
    if 'all' in filters:
        pageNum = 1
        validResults = True
        while validResults == True:
            url = 'https://www.facetuneapp.com/blog?a25596b1_page=' + str(pageNum)
            #Pulls page HTML
            page = requests.get(url)
            #creates soup object
            soupPage = BeautifulSoup(page.content, "html.parser")

            #used to verify if the next page has valid results
            length = len(blogPosts)
            #extracting elements
            for post in soupPage.find_all(class_="cms-item-link w-inline-block"):
                blogPosts = blogPosts + [post.get('href')]

            #print(blogPosts)

            if length == len(blogPosts):
                validResults = False
                break

            pageNum += 1
        return blogPosts
    
    else:
        for i in range(len(filters)):
            url = 'https://www.facetuneapp.com/blog-category/' + filters[i]
            #Pulls page HTML
            page = requests.get(url)
            #creates soup object
            soupPage = BeautifulSoup(page.content, "html.parser")
            for post in soupPage.find_all(class_="cms-item-link w-inline-block"):
                blogPosts = blogPosts + [post.get('href')]
        #print(blogPosts)
        return blogPosts


def scrapePost(url):
    fullurl = 'https://www.facetuneapp.com' + url
    #Pulls page HTML
    page = requests.get(fullurl)
    #creates soup object
    soupPage = BeautifulSoup(page.content, "html.parser")

    title = soupPage.find("title").text
    textList = []
    for bod in soupPage.find_all(['p', 'h2', 'h3']):
            textList = textList + [' ' + bod.text]
    
    if textList[-1] == ' This website is using cookies to improve your user experience. By continuing, you agree to our Cookie Policy.':
              del textList[-1]
    
    text = ''
    for i in range(len(textList)): 
        text = text + textList[i]
    text = textCleaner(text)
    return text
    

def textCleaner(inputString):
    '''returns list of one word strings without any extra spaces, line breaks, or special characters.'''

    #remove punctuation and conver to all lowercase
    noPunc = inputString.translate(str.maketrans('', '', string.punctuation)).lower()

    #removes extra spaces and line breaks
    res = ""
    res2 = ""
    for i in range(len(noPunc)):
        if (noPunc[i] == " " and noPunc[i-1] == " " ) or ord(noPunc[i]) == 10:
            pass
        else:
            res += noPunc[i]
    for i in range(len(res)):
        if (res[i] == " " and res[i-1] == " ") or ord(res[i]) == 10:
            pass
        else:
            res2 += res[i]    
    
    #remove emojis/special char
    wordList = makeList(res2)
    for i in range(len(wordList)):
        if not wordList[i].isalnum():
            newWord=""
            for k in range(len(wordList[i])):
                if wordList[i][k].isalnum():
                    newWord = newWord + wordList[i][k]
            wordList[i] = newWord
    return wordList


def makeList(string):
    return list(string.split(" "))

count = {} #{word,frequency}
def counter(url):
    '''Stores frequency of every word in the main post and comments in dictionary count'''
    allWords = scrapePost(url)
    for i in range(len(allWords)):
        if allWords[i] in count: #if this word has already been encountered add one to its dictionary value
            count[allWords[i]] = count[allWords[i]] + 1
        else: #if this is the first time this word has been encountered, create dictionary item with word as key and value equal to one
            count[allWords[i]] = 1

def countAllPages(list):
    '''Iterates counter on all URLS in list'''
    for i in range(len(list)):
        counter(list[i])

def filterDict(dict):
    '''filters dictionary to exclude unwanted words'''
    with open('noiseWords.csv', newline='') as f:
        search = list(csv.reader(f))
    noiseWords = []
    for i in range(len(search)):
        noiseWords.append(search[i][0])

    keys = list(dict.keys())
    staticKeys = copy.deepcopy(keys)
    for i in range(len(staticKeys)):
        if  keys[i] in noiseWords:
            del dict[staticKeys[i]]


def exportCSV(dict, name):
    '''exports dict as CSV'''

    with open(name, 'w', newline='', encoding = 'utf-8') as csvfile:
        header_key = ['word', 'freq']
        new_val = csv.DictWriter(csvfile, fieldnames=header_key)

        new_val.writeheader()
        for new_k in dict:
            new_val.writerow({'word': new_k, 'freq': dict[new_k]})

def wordCloud(dict):
    '''creates wordcloud using dictioanry keys as words and dictionary value as frequency'''
    text = ''
    key = list(dict.keys())
    for i in range(len(key)):
        text = text + ((key[i] + ' ')* dict[key[i]])

    word_cloud = WordCloud(
        width=3000,
        height=2000,
        random_state=1,
        background_color="black",
        colormap="Pastel1",
        collocations=False,
        stopwords=STOPWORDS,
        ).generate(text)
    
    # Display the generated Word Cloud
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

def main():
    filters = ['all'] #options are: all, lifestyle, social-media, selfie, beauty
    countAllPages(crawlBlog(filters))
    exportCSV(count, "wordFrequency.csv")
    filterDict(count)
    exportCSV(count, "wordFrequencyWordCloud.csv")
    print("--- %s seconds ---" % (time.time() - start_time))
    wordCloud(count)
    #print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()



