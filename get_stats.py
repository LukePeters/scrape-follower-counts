from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import sqlite3

def save_data(youtube, twitter, instagram):

  # Prepare data for saving
  record = {
    'date': int(datetime.now().strftime('%s')),
    'youtube': youtube,
    'twitter': twitter,
    'instagram': instagram
  }

  # Connect to the database
  con = sqlite3.connect('followers.db')
  cur = con.cursor()

  cur.execute('''
    CREATE TABLE IF NOT EXISTS monthly_stats (
      date INTEGER, youtube TEXT, twitter TEXT, instagram TEXT
    )
  ''')

  insert = cur.execute(
    'INSERT INTO monthly_stats VALUES (%s, "%s", "%s", "%s")' % (
      record['date'], record['youtube'], record['twitter'], record['instagram']
    )
  )

  con.commit()
  con.close()

# BROWSER AUTOMATION

# Setup webdriver
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path='./geckodriver', options=options)
driver.implicitly_wait(10)

# Get YouTube subscribers
driver.get('https://www.youtube.com/channel/UC6Oowe4rpbQXo6AmRHmDMYg')
youtube_count = driver.find_element_by_id('subscriber-count').text.split(' ')[0]

# Get Twitter followers
driver.get('https://twitter.com/MoonlightLuke')
twitter_count = driver.find_element_by_css_selector('a[href="/MoonlightLuke/followers"] > span > span').text

# Get Instagram followers
driver.get('https://www.picuki.com/profile/lukepeterscodes')
instagram_count = driver.find_element_by_css_selector('.followed_by').text

# Close webdriver
driver.close()

# Save the data
save_data(youtube_count, twitter_count, instagram_count)