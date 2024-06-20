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

dir_name = '211007'

url = 'https://b01-kr-naver-vod.pstatic.net/navertv/a/read/v2/VOD_ALPHA/navertv_2021_10_07_1609/hls/d0773936-276f-11ec-8222-246e963a41ed-000006.ts?_lsu_sa_=6bb561f0c1a76cf680d995166585fabd5e4137c8a90fbf283d472eca57b435b5382e3ac664f5a20df0f4344299382bbfe4969cc76dbf9dd70f15477f76992803cc910492ecd164f51ee389d1fa43b1efac60f4fce26c83e9d10c8c06364a385e3f338262b9285dac1987f8309af8eb785be81db9079e049d1cfcb713b820e5f4248bc146be2d36e9d2faec4782856ee5'
keyword = '.ts'

# keyword를 기준으로 URL을 분리
video_url1, video_url2 = url.split(keyword, 1)

# .ts를 기준으로 나뉜 두 부분 처리
video_url1 = video_url1[:-6]  # 마지막 6글자 (.ts 이전까지) 제거
video_url2 = keyword + video_url2  # .ts 다시 추가

save_video(video_url1, video_url2, 100, dir_name)
merge_videos(dir_name)
#delete_directory_and_file(dir_name)
