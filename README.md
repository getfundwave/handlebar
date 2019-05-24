# handlebar
handlebar is written in Python and uses the Tweepy package to go call the Twitter API. With handlebar, you can obtain the twitter handles of all the members of the lists you specify.

### Prerequisites
You will need API access and Consumer access tokens to make calls to the Twitter API.
These can be obtained by simply signing up on their [developer page](https://developer.twitter.com/en/apply-for-access "Twitter Developer API").

You will also need to install the Tweepy package for python to be able to use handlebar

```
pip install tweepy
```

### Installing

After cloning the repo, you will need to edit the ```settings.json``` file. 

In the ```keys``` section, fill out your Twitter API credentials.
```
{
    "access_token": " #ACCESS TOKEN ",
    "access_secret": " #ACCESS SECRET ",
    "consumer_key": " #CONSUMER KEY ",
    "consumer_secret": " #CONSUMER SECRET "
}
``` 

In the ```all_urls``` section, paste the URLs of the lists you would like to work on.
```
 "all_urls": [
              "https://twitter.com/abcd/lists/list1/",                #Example list
              "https://twitter.com/xyz/lists/list2/members/lang=en"   #Example list
             ]
```
In the ```format``` section, specify the extension the result files should be in.
```
"format": ".abc"
```
Currently ```.txt``` and ```.csv``` formats are supported

### Usage

Run the respective script in your terminal

* For names, run: 
```python names.py```

* For locations, run: 
```python locations.py```

The script will create a directory (if it doesn't already exist), called ```results``` and save the results of each list in a file corresponding to its name.

Example:
```list1.abc  list2.abc```

## Authors

* **Atieve Wadhwa** -  [AtieveWadhwa](https://github.com/AtieveWadhwa)

