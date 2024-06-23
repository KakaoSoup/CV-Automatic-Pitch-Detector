from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import time
import re
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# 클래스명 상수 정의
relay_player_area = 'RelayList_player_area__2ur0q'
relay_player_info = 'RelayList_player_info__380QS'
relay_player_profile = 'RelayList_profile_info__2n-fN'
relay_player_name = 'RelayList_name__1THfS'
relay_batting_order = 'RelayList_position__M6m4z'
relay_result_area = 'RelayList_result_area__2j4GI'
relay_main_info = 'RelayList_main_info__zGpeF'
relay_points = 'RelayList_point__1IjBt'
relay_history = 'RelayList_history_list__13jzg'
relay_pitch_num = 'RelayList_pitch_number__YlthP'
relay_pitch = 'RelayList_history_item__UEQst RelayList_type_pitch__3jVsu'
relay_stuff = 'RelayList_stuff__cpnw5'
relay_text = 'RelayList_text__tFNjV'
relay_speed = 'RelayList_speed__xA-Qw'
relay_count = 'RelayList_ball_count__2D8Rd'
relay_change = 'RelayList_history_item__UEQst RelayList_type_change__2Zxlf'