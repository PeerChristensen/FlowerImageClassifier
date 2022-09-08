from genericpath import exists
import os, requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

import pandas as pd

queries_df = pd.read_csv("flower_names.csv")

queries = queries_df.latin.values
folder_names = queries_df.folder_name.values

def serpapi_get_google_images(queries, folder_names):
    
    count = 0
    for f, q in zip(folder_names, queries):
        
        count += 1
        print(f"Species #{count}..")
        
        image_results = []
        
        folder = f"data/{f}"
        
        if os.path.exists(folder):
            continue
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": q,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            "api_key": "10fefce8a6606142af79c5053fcb22fda2cb149c65291ce3b906fc873a69f811" # os.getenv("API_KEY")   # your serpapi api key
            # other query parameters: hl (lang), gl (country), etc  
        }
    
        search = GoogleSearch(params)         # where data extraction happens
    
        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary
    
            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if image["original"] not in image_results:
                        image_results.append(image["original"])
                
                # update to the next page
                params["ijn"] += 1
            else:
                images_is_present = False
                print(results["error"])
    
    
    # -----------------------
    # Downloading images

            for index, image in enumerate(results["images_results"], start=1):
                
                if index <= len(results["images_results"]):
                    print(f"Downloading {q} image #{index} out of {len(results['images_results'])}...")

                    try:
                        opener=urllib.request.build_opener()
                        opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
                        urllib.request.install_opener(opener)

                        urllib.request.urlretrieve(image["original"], f"{folder}/{index}.jpg")
                    
                    except:
                        print("Timed out")
                        pass
                    
                else:
                    #print(json.dumps(image_results, indent=2))
                    #print(len(image_results))
                    break    
            break        


serpapi_get_google_images(queries=queries, folder_names=folder_names)