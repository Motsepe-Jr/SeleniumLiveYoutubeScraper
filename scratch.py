import requests
from bs4 import BeautifulSoup

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

# Does not execute Javascript / or you can try to use select method /or use selenium
response = requests.get(YOUTUBE_TRENDING_URL)


with open("trending.html", "w") as f:
  f.write(response.text)


  doc = BeautifulSoup(response.text, "html.parser")


  print("Page Title", doc.title)


# find all the videos divs
video_divs = doc.find_all('div', 
class_='ytd-video-renderer')

print(f"found {len(video_divs)} videos")
