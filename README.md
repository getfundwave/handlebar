# handlebar

**handlebar** is written in Python and uses the Twitter API and Web Scraping. With **handlebar**, you can obtain the following information (if available) for all the members of the specified Twitter lists:

1. Username
2. Location
3. Bio / Description
4. Website URL
5. Metadata description of above URL

### Prerequisites

You will need API access and Consumer access tokens to make calls to the Twitter API.
These can be obtained by simply signing up on their [developer page](https://developer.twitter.com/en/apply-for-access "Twitter Developer API").

### Installing

1. Clone the repo.

2. Install the python packages mentioned in ```requirements.txt```.

    * Using pip:

    ```python
    pip install -r requirements.txt
    ```

3. Edit the ```settings.json``` file.

    * In the ```keys``` section, fill out your Twitter API credentials.

    ```json
    {
        "access_token": " #ACCESS TOKEN ",
        "access_secret": " #ACCESS SECRET ",
        "consumer_key": " #CONSUMER KEY ",
        "consumer_secret": " #CONSUMER SECRET "
    }
    ```

    * In the ```all_urls``` section, paste the URLs of the lists you would like to work on.

    ```json
    "all_urls": [
                "https://twitter.com/abcd/lists/list1/",                #Example list
                "https://twitter.com/xyz/lists/list2/members/lang=en"   #Example list
                ]
    ```

    * In the ```format``` section, specify the extension the result files should be in.

    ```json
    "format": ".csv"
    ```

    > Currently only ```.txt``` and ```.csv``` formats are supported

    * Set ```count_only: true``` if you wish to only count the total handles from all the lists.
    * Set ```no_metadata: true``` if you do not wish to scrape metadata from URLs obtained from user profiles.

### Usage

Run the script from your terminal:

```python3 main.py```

The script will create a directory (if it doesn't already exist), called ```results``` and save the results of each list in a file corresponding to its name.

Example:
```list1.csv  list2.csv```

## Authors

* **Atieve Wadhwa** -  [AtieveWadhwa](https://github.com/AtieveWadhwa)
