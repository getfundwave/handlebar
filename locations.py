import tweepy, re, json, os, csv

config = json.loads(open("settings.json").read())

ACCESS_TOKEN = config['keys']['access_token']
ACCESS_SECRET = config['keys']['access_secret']
CONSUMER_KEY = config['keys']['consumer_key']
CONSUMER_SECRET = config['keys']['consumer_secret']

format=config['format']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

all_urls =  config['all_urls']

total_handles = 0

os.makedirs("results", exist_ok=True)

if not ((format==".txt") or (format==".csv")):
    print("Invalid format, Check config file.")
    exit()

for list_url in all_urls:
    file_handles = 0
    components = re.split('; |, |\*|\n|\/|\?',list_url)
    list_name = components[5]
    list_owner = components[3]

    print("Working on " + list_name + " :: " + list_owner)

    file = open("results/"+list_name+"_locations"+format,'w')
    if(format==".csv"):
        writer=csv.writer(file)

    for member in tweepy.Cursor(api.list_members, list_owner, list_name).items():
        user = str("@"+member.screen_name)
        loc = str(member.location)
        if (format == ".txt"):
            file.write('{:<15s}{:>50s}'.format(user,loc))
            file.write("\n")
        elif(format == ".csv"):
            row=[user,loc]
            writer.writerow(row)
        file_handles+=1
    print("Finished " + list_name + " :: " + list_owner)
    print("Handles in file = " + str(file_handles))
    total_handles+=file_handles
    print()
print("Total Handles = " + str(total_handles))
