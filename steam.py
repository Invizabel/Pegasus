import argparse
import os
import re
import requests
from collections import Counter
from TheSilent.kitten_crawler import kitten_crawler
from TheSilent.puppy_requests import text
from bs4 import BeautifulSoup

CYAN = "\033[1;36m"

def transform(sentence_hits, word_hits):
    sentence_models = []
    model = {}

    # process data
    count = 0
    for result in sentence_hits:
        count += 1
        tokens = Counter(result).most_common()
        for token_x, token_y in tokens:            
            try:
                valid = bytes(token_x, "ascii")
                if valid and "\\" not in token_x:
                    model[token_x] += int(token_y)

            except KeyError:
                model[token_x] = int(token_y)

            except:
                pass

    # normalize data
    new_model = {}
    for i, j in model.items():
        new_model[i] = j / count

    sentence_models.append(new_model)

    word_models = []
    model = {}

    # process data
    count = 0
    for result in word_hits:
        count += 1
        tokens = Counter(result).most_common()
        for token_x, token_y in tokens:            
            try:
                valid = bytes(token_x, "ascii")
                if valid and "\\" not in token_x:
                    model[token_x] += int(token_y)

            except KeyError:
                model[token_x] = int(token_y)

            except:
                pass

    # normalize data
    new_model = {}
    for i, j in model.items():
        new_model[i] = j / count

    word_models.append(new_model)

    return sentence_models, word_models

def train(crawl_len):
    word_hits = []
    sentence_hits = []

    sites = ["https://abc.com",
             "https://www.amazon.com",
             "https://www.apple.com",
             "https://www.baylor.edu",
             "https://www.bcisd.us",
             "https://www.bisd.us",
             "https://www.cnn.com",
             "https://www.crowdstrike.com",
             "https://duckduckgo.com",
             "https://www.fbi.gov",
             "https://flipperzero.one",
             "https://www.fox.com",
             "https://www.foxnews.com",
             "https://github.com",
             "https://www.google.com",
             "https://hak5.org",
             "https://www.hcisd.org",
             "https://www.hillcollege.edu",
             "https://www.huntress.com",
             "https://www.kali.org",
             "https://www.kaspersky.com",
             "https://www.kwtx.com",
             "https://www.kxxv.com",
             "https://www.laferiaisd.org",
             "https://www.lfcisd.net",
             "https://www.malwarebytes.com",
             "https://www.matix.io",
             "https://www.mcc.edu",
             "https://www.midwayisd.org",
             "https://www.minecraft.net",
             "https://www.nasa.gov",
             "https://www.newcaneyisd.org",
             "https://www.nintendo.com",
             "https://www.nsa.gov",
             "https://www.nytimes.com",
             "https://owasp.org",
             "https://www.pi-isd.net",
             "https://pyga.me",
             "https://www.pygame.org",
             "https://www.riohondoisd.net",
             "https://www.sbcisd.net",
             "https://www.scinary.com",
             "https://www.sentinelone.com",
             "https://www.sfasu.edu",
             "https://www.smisd.net",
             "https://www.srtx.org",
             "https://www.stisd.net",
             "https://www.tamu.edu",
             "https://www.tstc.edu",
             "https://www.uh.edu",
             "https://www.uhcl.edu",
             "https://www.uhd.edu",
             "https://www.uhv.edu",
             "https://www.unt.edu",
             "https://www.untdallas.edu",
             "https://www.unthsc.edu",
             "https://www.uta.edu",
             "https://www.utdallas.edu",
             "https://www.utep.edu",
             "https://www.utexas.edu",
             "https://www.uth.edu",
             "https://www.utmb.edu",
             "https://www.utpb.edu",
             "https://www.utrgv.edu",
             "https://www.utsa.edu",
             "https://www.uttyler.edu",
             "https://www.w3schools.com",
             "https://www.wacoisd.org",
             "https://www.xbox.com",
             "https://www.whitehouse.gov"]
    
    links = []
    for site in sites:
        crawled = kitten_crawler(site, crawl = crawl_len ,ethics = True)
        for i in crawled:
            links.append(i)

    for link in links:
        print(CYAN + f"scraping: {link}")
        try:
            data = text(link)
            soup = BeautifulSoup(data, "html.parser")

            all_text = ""
            for tag in soup.find_all(["del", "em", "i", "ins", "mark", "p", "small", "strong", "sub", "sup"]):
                all_text += tag.get_text() + "\n"


            parse_sentence = re.findall(r"[A-Z]+[\x20-\x7e]+[\.\?\!]+", all_text)
            sentence_hits.append(parse_sentence)

            parse_words = re.findall(r"[\x21-\x7e]+", all_text)
            word_hits.append(parse_words)

        except:
            continue

    return sentence_hits, word_hits

def main():
    os.system("clear")

    crawl_len = {"tiny": 1,
                 "small": 10,
                 "medium": 100,
                 "large": 1000,
                 "infinite": 10000}

    for key, value in crawl_len.items():
        sentence_hits, word_hits = train(value)
        print(CYAN + "transforming data")
        sentence_models, word_models = transform(sentence_hits, word_hits)

        with open(f"model_sentence_{key}.csv", "w") as file:
            file.write("key,vector\n")
            for model in sentence_models:
                for i, j in model.items():
                    file.write(f"{i},{j}\n")
                    
        with open(f"model_word_{key}.csv", "w") as file:
            file.write("key,vector\n")
            for model in word_models:
                for i, j in model.items():
                    file.write(f"{i},{j}\n")

if __name__ == "__main__":
    main()
