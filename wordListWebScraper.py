from bs4 import BeautifulSoup
#import requests
#from requests import async
# import grequests
import re
import requests
import concurrent.futures

def processRequests(html):
    global totalProcessed, words
    print("Processed: " + totalProcessed + " of " + totalUrlLen)
    totalProcessed += 1
    soup = BeautifulSoup(html, 'html.parser')
    allWords = soup.find_all('a', class_='word-box-link')
    if(len(allWords) > 0):
        words.add(re.sub(r'[0-9]', '', allWords[0].text))

# create a set to store the words
words = set()

def get_urls():
    urls = []
    for i in range(ord('a'), ord('z') + 1):
        for j in range(ord('a'), ord('z') + 1):
            word = chr(i) + chr(j)
            print(word)
            urls.append("https://www.morewords.com/pair/" + word)
    return urls

def load_url(url, timeout):
    return requests.get(url, timeout = timeout)

resp_err = 0
resp_ok = 0
totalProcessed = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

    urls = get_urls()
    totalUrlLen = len(urls)
    future_to_url = {executor.submit(load_url, url, 10): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            processRequests(data.text)
        except Exception as exc:
            resp_err = resp_err + 1
        else:
            resp_ok = resp_ok + 1
    print("Done")
    print("Total processed: " + str(totalProcessed))
    print("Total errors: " + str(resp_err))
    print("Total ok: " + str(resp_ok))
# save words set to file
with open('words.txt', 'w') as f:
    for word in words:
        f.write(word + ",")
