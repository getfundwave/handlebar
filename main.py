import tweepy, re, json, os

config = json.loads(open("settings.json").read())

ACCESS_TOKEN = config['keys']['access_token']
ACCESS_SECRET = config['keys']['access_secret']
CONSUMER_KEY = config['keys']['consumer_key']
CONSUMER_SECRET = config['keys']['consumer_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

all_urls =  config['all_urls']

total_handles = 0

os.makedirs("results", exist_ok=True)

for list_url in all_urls:
    file_handles = 0
    components = re.split('; |, |\*|\n|\/|\?',list_url)
    list_name = components[5]
    list_owner = components[3]

    print("Working on " + list_name + " :: " + list_owner)

    file = open("results/"+list_name+".csv",'w')

    for member in tweepy.Cursor(api.list_members, list_owner, list_name).items():
        file.write("@" + member.screen_name + ", ")
        file_handles+=1
    print("Finished " + list_name + " :: " + list_owner)
    print("Handles in file = " + str(file_handles))
    total_handles+=file_handles
    print()
print("Total Handles = " + str(total_handles))
