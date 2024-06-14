import urllib.request
import re
import os
import shutil

def save_video(url1, url2, num_videos, dir_name):
      if os.path.exists(dir_name):
            pass
      elif dir_name:
            os.mkdir(dir_name)
      try:
            for num in range(num_videos + 1):
                  save_name = os.path.join(dir_name, f'{str(num).zfill(6)}.ts')
                  real_video_url = f'{url1}{str(num).zfill(6)}{url2}'
                  urllib.request.urlretrieve(real_video_url, save_name)
                  print(f'{str(num).zfill(6)}.ts Downloaded,')
      except:
            print('No file or The end')
      print('Download complete.')

def merge_videos(dir_name):
      video_list = sorted(os.listdir(dir_name), key=lambda x:(len(x), x))
      #print(video_list)
      print('Merge Start')
      with open(f'{dir_name}.mp4', 'wb') as f1:
            for t in video_list:
                  with open(os.path.join(dir_name, t), 'rb') as f2:
                        shutil.copyfileobj(f2, f1)
      print('Merge complete')
            
def delete_directory_and_file(dir_name):
      print('Delete Start')
      try:
            for video in os.listdir(dir_name):
                  video_path = os.path.join(dir_name, video)
                  #print(f'Delete {video_path}')
                  os.remove(video_path)
      except:
            print(f'Error - Cannot delete file {video}')

      try:
            os.rmdir(dir_name)
      except:
            print(f'Error - Cannot delete directory')
      print('Delete Complete')


video_url1 = 'https://b01-kr-naver-vod.pstatic.net/navertv/a/read/v2/VOD_ALPHA/navertv_2021_10_07_1609/hls/d0773936-276f-11ec-8222-246e963a41ed-'
video_url2 = '.ts?_lsu_sa_=6dd531f881356ec682d695526fe51ab4cead3d08a706bfa432378bc1c7c43b25562ebaa96cf5b503903331c2153d9b09aede819eab6bd62191f9da472ee397b39d090c9689cf22b95fcf30c438e77306c83bb763e071b6c6966b7c3ed0405ad7ceafd65582b27f19320e3199664d31ea45cd8abba1cfe9a5c5cb1872c54442387be1ce4f626ffdc8e6438591e84d8fe6'
dir_name = '211007'

save_video(video_url1, video_url2, 999999, dir_name)
merge_videos(dir_name)
delete_directory_and_file(dir_name)
