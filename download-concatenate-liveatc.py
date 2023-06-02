#!/usr/bin/env python3

import pytz
import datetime
import os

import pydub
import requests
# http://pydub.com/
# https://github.com/jiaaro/pydub/

tz = pytz.timezone('America/Los_Angeles')
start_time = tz.localize(datetime.datetime(2023,6,2,9,0,0)).astimezone(pytz.utc)
PREFIX = 'kpdx/KPDX3-'
LOC_LABELS = ['App-Dep-South']
NUM_HOURS = 2

def download_filename(url):
  local_filename = url.split('/')[-1]
  return local_filename

def download_file(url):
  local_filename = url.split('/')[-1]
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192): 
        # If you have chunk encoded response uncomment if
        # and set chunk_size parameter to None.
        #if chunk: 
        f.write(chunk)
  return local_filename


# https://archive.liveatc.net/kgso/KGSO1-App-Dep-South-May-29-2023-0300Z.mp3
# https://archive.liveatc.net/kgso/KGSO1-App-Dep-West-May-29-2023-0230Z.mp3
# https://archive.liveatc.net/kgso/KGSO1-Twr-May-29-2023-0330Z.mp3

for loc_label in LOC_LABELS:
  concat_file = f"{loc_label}_concat.mp3"
  full_file = None
  for i in range(0,NUM_HOURS):
    for j in [0,30]:
      t = start_time + datetime.timedelta(hours=i, minutes=j)
      #print(i)
      pt = t.strftime('%b-%d-%Y-%H%M')
      #print(f"t={pt}")
      url = f'https://archive.liveatc.net/{PREFIX}{loc_label}-{pt}Z.mp3'
      print(url)
      loc_file = download_filename(url)
      if not os.path.exists(loc_file):
        loc_file = download_file(url)
      seg = pydub.AudioSegment.from_mp3(loc_file)
      if not full_file:
        full_file = seg
      else:
        full_file += seg
      full_file.export(concat_file, format="mp3")
      print(concat_file)
#.replace(tzinfo=tz) #.astimezone(pytz.utc)
