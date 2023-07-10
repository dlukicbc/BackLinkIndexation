import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import datetime
import config_file
from random import uniform

now = datetime.now()
start_time = now.strftime("%H:%M:%S")

output = config_file.output
urlinput = config_file.urlinput
urls = open(urlinput, "r")

user_agent = config_file.user_agent
headers = {'User-Agent': user_agent}

f = open(output, "w+", newline="\n", encoding="utf-8")
writer = csv.writer(f)
writer.writerow(["URL", "Indexed"])


async def check_indexed(session, url):
  query = {'q': 'site:' + url}
  google = "https://www.google.com/search?" + urlencode(query)
  async with session.get(google, headers=headers) as resp:
    data = await resp.text()
    soup = BeautifulSoup(data, "html.parser")
    try:
      check = soup.find_all("div", id="search")[0].find("div")
      length = len(check)
      if length != 0:
        writer.writerow([url, "True"])
        print(url + " is indexed!")
      elif length == 0:
        writer.writerow([url, "False"])
        print(url + " is NOT indexed!")
    except TypeError:
      writer.writerow([url, "False"])
      print(url + " is NOT indexed!")
    except IndexError as ie:
      writer.writerow([url, "RobotCheckError"])
      print(url + "RobotCheckError!")
    await asyncio.sleep(uniform(3, 6))


async def main():
  async with aiohttp.ClientSession() as session:
    tasks = [
      asyncio.ensure_future(check_indexed(session, line.strip()))
      for line in urls
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
  now = datetime.now()
  start_time = now.strftime("%H:%M:%S")
  asyncio.run(main())
  now = datetime.now()
  end_time = now.strftime("%H:%M:%S")
  print(start_time)
  print(end_time)

f.close()
