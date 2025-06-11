# fetch_sources/twitter.py
"""
1. import requests, datetime, config variables

2. Define function fetch_tweets():
     a. Compute `start_time = now - 24h` in ISO 8601
     b. Prepare headers = { "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}" }
     c. Initialize `all_results = []`

     d. For each `query` in TWITTER_QUERIES:
          i. Build `params` dict:
                - "query": query + " lang:en -is:retweet"
                - "start_time": start_time
                - "max_results": str(NUM_TWEETS)
                - "tweet.fields": "created_at,author_id"
                - "expansions": "author_id"
                - "user.fields": "username"
         ii. Make GET request to Twitter Recent Search endpoint with headers, params
        iii. If response.status_code != 200: raise or log error
         iv. Parse JSON body:
                - Extract `data` list (tweets) and `includes.users` (authors)
          v. Build a map from `user_id` → `username`
         vi. For each tweet in `data`:
                • Lookup `username`  
                • Construct `url = f"https://twitter.com/{username}/status/{tweet['id']}"`  
                • Append dict to a `tweets` list:
                  { "id": tweet["id"], "text": tweet["text"], "author": username, "created_at": tweet["created_at"], "url": url }
        vii. Append `{ "query": query, "tweets": tweets }` to `all_results`

     e. Return `all_results`

3. End of module
"""