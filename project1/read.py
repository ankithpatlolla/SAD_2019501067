import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"gsqeDQgf6khhxMPVqY3VA": "KEY", "isbns": "9781632168146"})
print(res.json())