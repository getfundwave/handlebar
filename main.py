import re
import tweepy
import json
import os
import csv
import requests
import progressbar
import time
from bs4 import BeautifulSoup

config = json.loads(open("settings.json").read())

ACCESS_TOKEN = config['keys']['access_token']
ACCESS_SECRET = config['keys']['access_secret']
CONSUMER_KEY = config['keys']['consumer_key']
CONSUMER_SECRET = config['keys']['consumer_secret']

extension = config['format']
only_count = config['count_only']
metadata_toggle = config['no_metadata']
combine_files = config['combine_files']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
widgets = [progressbar.Percentage(), progressbar.Bar()]
all_urls =  config['all_urls']

total_handles = 0

os.makedirs("results", exist_ok=True)

if not ((extension==".txt") or (extension==".csv")):
    print("Invalid format, Check config file.")
    exit()

print()
print("Calculating total handles to extract...")
print()

todo=0
counter = 0

todobar = progressbar.ProgressBar(widgets=widgets, max_value=len(all_urls)).start()
for list_url in all_urls:
    components = re.split(r'; |, |\*|\n|\/|\?',list_url)
    list_name = components[5]
    list_owner = components[3]
    
    try:
        response = requests.get(list_url,headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="html.parser")
        for el in soup.find_all('ul',attrs={"class":"stats"}):
            for i in el.find_all("li"):
                txt = str(i)
                if("Members" in txt):
                    comma = re.search('<strong>(.*)</strong>',txt)
                    comma = comma.group(1)
                    number = int(comma.replace(',',''))
                    todo+=number
    except Exception as e:
        print("Something is wrong with list URL")
        print(list_url + " -- " + str(e))
        continue
    counter+=1
    todobar.update(counter)

todobar.finish()
print()
print("Total handles to fetch: " + str(todo))
print()

if(only_count):
    print("Count mode only. Exitting now.")
    exit()

errfile = open("results/log.txt",'w')

print("Extracting now")
print()
print("Progress:")

done = 0
all_files=[]

donebar = progressbar.ProgressBar(widgets=widgets, max_value=todo).start()
for list_url in all_urls:
    components = re.split(r'; |, |\*|\n|\/|\?',list_url)
    list_name = components[5]
    list_owner = components[3]

    errfile.write("Log for " + list_name + " :: " + list_owner + " @ " + list_url + "\n")

    filename = "results/"+list_name+extension
    file = open(filename,'w')
    all_files.append(filename)

    if(extension==".csv"):
        writer=csv.writer(file)

    for member in tweepy.Cursor(api.list_members, list_owner, list_name).items():
        user = str("@"+member.screen_name)
        name = str(member.name)
        loc = str(member.location)
        bio = str(member.description)
        url = str(member.url)
        metadata=""

        if(not metadata_toggle):
            try:
                response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()
                soup = BeautifulSoup(response.text, features="html.parser")
                metas = soup.find_all('meta')
                metadata = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ][0]
            except Exception as e:
                errfile.write(url + " -- " + str(e))

        if (extension == ".txt"):
            file.write('{:<15s}{:^50s}{:^50s}{:^150s}{:^50s}{:>150s}'.format(user,name,loc,bio,url,metadata))
            file.write("\n")
        elif(extension == ".csv"):
            row=[user,name,loc,bio,url,metadata]
            writer.writerow(row)

        done+=1
        donebar.update(done)
    
donebar.finish()
print()
print("Total extracted handles = " + str(done))
print()

files_done=0
if combine_files:
    print("Combining into 1 file")
    print()
    combinebar = progressbar.ProgressBar(widgets=widgets, max_value=len(all_urls)).start()
    with open('combined_file.'+extension, 'w') as outfile:
        for fname in all_files:
            with open(fname) as infile:
                outfile.write(infile.read())
            files_done+=1
            combinebar.update(files_done)
    combinebar.finish()

print("Check 'results/errors.log' for details")
