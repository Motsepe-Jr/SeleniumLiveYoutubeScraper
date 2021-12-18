from selenium  import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
import os
import json

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.headless = True
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver 

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'

  driver.get(YOUTUBE_TRENDING_URL)
  
  video =  driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  
  return video

def parse_video(video):
  # title, url, thumbnail, channel, views, uploaded, (images)
  
  # title
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  
  # url
  url = title_tag.get_attribute('href')

  # thumbnail
  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')
  
  #channelname
  channel_div = video.find_element(By.CLASS_NAME, 
  'ytd-channel-name')
  channel_name = channel_div.text
  
  # descritopm
  description = video.find_element(By.ID, 'description-text').text

  # Views and Posted date
  views_split = video.find_element(By.ID, 'metadata-line').text
  view_list = views_split.split('\n')
  views = view_list[0]
  posted = view_list[1]

  return {
    'title': title, 
    'url': url,
    'thumbnail': thumbnail_url, 
    'Channel': channel_name, 
    'description': description,
    'views': views,
    'posted': posted
  }

def send_email(body):
  
  # Set Global Variables
  gmail_user = os.environ['EMAIL']
  gmail_password =  os.environ['SECRETS']
  # Create Email 
  mail_from = gmail_user
  mail_to = os.environ['EMAIL']
  mail_subject = 'Hello'
  mail_message_body = body

  mail_message = '''\
  From: %s
  To: %s
  Subject: %s
  %s
  ''' % (mail_from, mail_to, mail_subject, mail_message_body)

  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.login(gmail_user, gmail_password)
      server.sendmail(mail_from, mail_to, mail_message)
      server.close()

      print('Email sent!')
  except Exception as e:
      print('Something went wrong...', e)
    

if __name__  == "__main__":
  print('Creating drivers')
  driver = get_driver()

  print("Fetching videos")
  videos = get_videos(driver)

  print('Parsing top ten vidoes')
  videosData = [parse_video(video) for video in videos[:10]]
  
  print("Save to the csv files")
  videos_df = pd.DataFrame(videosData)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)

  print('Send an email with the results')
  body = json.dumps(videosData, indent=2)
  send_email(body)

  print('Finished')

 
 
  

