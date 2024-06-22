from imports import *
from classes import *


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


def GetUrl(team_name):
      url = "https://sports.news.naver.com/kbaseball/index"

      # 팀명에 따른 tag
      tag = {"삼성": 'SS',    "롯데": 'LT', 
             "SSG": 'SK',     "키움": 'WO', 
             "한화": 'HH',    "두산": 'OB',
             "NC": 'NC',      "엔씨": 'NC',      
             "KIA": 'HT',     "기아": 'HT',
             "KT": 'KT',      "케이티": 'KT',
             "LG": 'LG',      "엘지": 'LG'}

      try:
            # 웹 페이지 가져오기
            response = requests.get(url)
            
            # HTTP 응답 상태 확인
            response.raise_for_status()
            
            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 모든 a 태그 찾기
            a_tags = soup.find_all('a')
            
            # 정규표현식을 이용하여 '/game/'으로 시작하는 링크만 출력
            #pattern = re.compile(r'^/game/')
            pattern = re.compile(r'/game/\d{8}[A-Z]{4}\d{5}')
              
            for a_tag in a_tags:
                  href = a_tag.get('href')
                  if href and pattern.match(href) and tag[team_name] in href:
                        return "https://m.sports.naver.com" + href
      except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
      except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
            
def GetCurrentMatch(team_name):
      # 현재 날짜와 시간 가져오기
      now = datetime.now()
      
      # 요일 가져오기 (0: 월요일, 1: 화요일, ..., 6: 일요일)
      weekday_number = now.weekday()

      # 현재 시간의 시와 분 가져오기
      current_hour = now.hour
      current_minute = now.minute
      
      # 만약 정수로 사용하고자 한다면, int() 함수를 사용하여 형 변환 가능
      current_hour_int = int(current_hour)
      current_minute_int = int(current_minute)
      
      # 평일 경기 여부 확인
      if weekday_number < 5:
            if current_hour_int > 18 or (current_hour_int == 18 and current_minute_int >= 30):
                  print("경기가 시작되었습니다.")
            else:
                  print("경기 시작 전입니다.")
      # 주말 경기 여부 확인
      else:
            if current_hour_int >= 17:
                  print("경기가 시작되었습니다.")
            else:
                  print("경기 시작 전입니다.")
      
      url = GetUrl(team_name)
      parts = url.split('/')
      if len(parts) == 6:
            # Remove the last part
            base_url_parts = parts[:-1]
            # Join the parts back together with '/'
            url = '/'.join(base_url_parts)
      return url


def setup_driver(url):
      service = Service(ChromeDriverManager().install())
      driver = webdriver.Chrome(service=service)
      driver.get(url)
      return driver


def click_button_and_wait(driver, button_css_selector):
      try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector)))
            button.click()
            time.sleep(2)
            return True
      except TimeoutException:
            print(f"버튼을 찾을 수 없거나 클릭할 수 없습니다: {button_css_selector}")
            return False
      except NoSuchElementException:
            print(f"버튼이 존재하지 않습니다: {button_css_selector}")
            return False
      except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return False


def parse_html(driver):
      page_source = driver.page_source
      soup = BeautifulSoup(page_source, 'html.parser')
      return soup


def process_player_info(player_area, relay_player_info, relay_player_profile, relay_player_name, relay_batting_order, verbose=True):
      player_info = player_area.find(class_=relay_player_info)
      player_profile = player_info.find(class_=relay_player_profile)
      name = player_profile.find(class_=relay_player_name)
      batting_order = player_profile.find(class_=relay_batting_order)
      order_text = int(batting_order.get_text()[:-3])
      if verbose:
            print(f'{order_text}번타자')
      return name.get_text()


def process_main_info(player_area, relay_main_info, relay_text, relay_points, verbose=True):
      result = []
      main_infos = player_area.find_all(class_=relay_main_info)
      for main_info in main_infos:
            main_info_texts = main_info.find_all(class_=relay_text)
            if main_info_texts:
                  for text_element in main_info_texts:
                        if verbose:
                              print(text_element.get_text())
                        result.append(text_element.get_text())
            main_info_points = main_info.find_all(class_=relay_points)
            if main_info_points:
                  for text_element in main_info_points:
                        if verbose:
                              print(f'(득점) {text_element.get_text()}')
                        result.append(text_element.get_text())
      return result
                
                        
def process_history(player_area, relay_history, relay_pitch_num, relay_text, relay_stuff, relay_speed, relay_count, relay_change, verbose=True):
      history_elements = player_area.find_all(class_=relay_history)
      for history in history_elements:
            pitch_nums = history.find_all(class_=relay_pitch_num)
            types = history.find_all(class_=relay_text)
            stuffs = history.find_all(class_=relay_stuff)
            speeds = history.find_all(class_=relay_speed)
            counts = history.find_all(class_=relay_count)
            changes = history.find_all(class_=relay_change)

            max_length = max(len(pitch_nums), len(types), len(stuffs), len(speeds), len(counts))

            # 리스트 길이 맞추기
            while len(pitch_nums) < max_length:
                  pitch_nums.insert(0, None)
            while len(types) < max_length:
                  types.insert(0, None)
            while len(stuffs) < max_length:
                  stuffs.insert(0, None)
            while len(speeds) < max_length:
                  speeds.insert(0, None)
            while len(counts) < max_length:
                  counts.insert(0, None)

            for pitch_num_element, type_element, speed_element, stuff_element, count_element in zip(reversed(pitch_nums), reversed(types), reversed(speeds), reversed(stuffs), reversed(counts)):
                  pitch_num_text = int(pitch_num_element.get_text()[:-1]) if pitch_num_element else 'N/A'
                  type_text = type_element.get_text() if type_element else 'N/A'
                  speed_text = int(speed_element.get_text()[:-4]) if speed_element else 'N/A'
                  stuff_text = stuff_element.get_text() if stuff_element else 'N/A'
                  count_text = count_element.get_text()[4:] if count_element else 'N/A'
                  if verbose:
                        print(f'{pitch_num_text}구 {type_text}: {speed_text}km/h {stuff_text} | {count_text}')

            # changes 처리
            if changes:
                  for change_element in changes:
                        change_text = change_element.get_text()
                        change_text = re.sub(r'교체(?! )', '교체 ', change_text)
                        change_text = re.sub(r'OUT', ' OUT ', change_text)
                        change_text = re.sub(r'IN', ' IN', change_text)
                        change_text = re.sub(r'(\w+):', r'\1 :', change_text)
                        if verbose:
                              print(f'{change_text} ')


def get_history(atbat, player_area, relay_history, relay_pitch_num, relay_text, relay_stuff, relay_speed, relay_count, relay_change, verbose=True):
      history_elements = player_area.find_all(class_=relay_history)
      for hist in history_elements:  # 변경된 변수명 hist 사용
            pitch_nums = hist.find_all(class_=relay_pitch_num)
            types = hist.find_all(class_=relay_text)
            stuffs = hist.find_all(class_=relay_stuff)
            speeds = hist.find_all(class_=relay_speed)
            counts = hist.find_all(class_=relay_count)
            changes = hist.find_all(class_=relay_change)

            max_length = max(len(pitch_nums), len(types), len(stuffs), len(speeds), len(counts))

            # 리스트 길이 맞추기
            while len(pitch_nums) < max_length:
                  pitch_nums.insert(0, None)
            while len(types) < max_length:
                  types.insert(0, None)
            while len(stuffs) < max_length:
                  stuffs.insert(0, None)
            while len(speeds) < max_length:
                  speeds.insert(0, None)
            while len(counts) < max_length:
                  counts.insert(0, None)

            for pitch_num_element, type_element, speed_element, stuff_element, count_element in zip(reversed(pitch_nums), reversed(types), reversed(speeds), reversed(stuffs), reversed(counts)):
                  pitch_num_text = int(pitch_num_element.get_text()[:-1]) if pitch_num_element else 'N/A'
                  type_text = type_element.get_text() if type_element else 'N/A'
                  speed_text = int(speed_element.get_text()[:-4]) if speed_element else 'N/A'
                  stuff_text = stuff_element.get_text() if stuff_element else 'N/A'
                  count_text = count_element.get_text()[4:] if count_element else 'N/A'
                  if verbose:
                        print(f'{pitch_num_text}구 {type_text}: {speed_text}km/h {stuff_text} | {count_text}')
                  pitch_history = PitchHistory(pitch_num_text, type_text, speed_text, stuff_text, count_text)  # 변경된 변수명 pitch_history 사용
                  atbat.add_history(pitch_history)
                               

            # changes 처리
            if changes:
                  for change_element in changes:
                        change_text = change_element.get_text()
                        change_text = re.sub(r'교체(?! )', '교체 ', change_text)
                        change_text = re.sub(r'OUT', ' OUT ', change_text)
                        change_text = re.sub(r'IN', ' IN', change_text)
                        change_text = re.sub(r'(\w+):', r'\1 :', change_text)
                        if verbose:
                              print(f'{change_text} ')


def extract_players(soup, lineup_list_class, lineup_item_class, verbose=True):
      converted_players_away = []
      converted_players_home = []
      
      team_names = soup.find_all(class_='Lineup_lineup_title__1WigY')
      converted_players_away.append(team_names[0].get_text()[:-2])
      converted_players_home.append(team_names[1].get_text()[:-2])
    
      # lineup_list_class에 해당하는 모든 리스트를 찾습니다.
      lineup_lists = soup.find_all(class_=lineup_list_class)
      
      for lineup_list in lineup_lists:
            lineup_items = lineup_list.find_all(class_=lineup_item_class)
            for lineup_item in lineup_items:
                  if lineup_item == lineup_items[0]:
                        # 첫 번째 리스트의 경우 선수 순서를 나타내는 클래스를 찾습니다.
                        lineup_orders = lineup_item.find_all(class_='Lineup_text__2lYRS')
                  else:
                        # 첫 번째 리스트 이후의 리스트는 다른 클래스로 선수 순서를 나타내므로 다른 클래스를 찾습니다.
                        lineup_orders = lineup_item.find_all(class_='Lineup_order__1-EPy')
                  
                  # 각 리스트에서 선수 이름과 포지션을 찾습니다.
                  lineup_names = lineup_item.find_all(class_='Lineup_name__jV19m')
                  lineup_positions = lineup_item.find_all(class_='Lineup_position__265hb')
                  
                  # 선수들의 정보를 추출하여 변환합니다.
                  for order, name, position in zip(lineup_orders, lineup_names, lineup_positions):
                        order_text = order.get_text().strip()
                        name_text = name.get_text().strip()
                        position_text = position.get_text().strip()
                        
                        # 변환된 선수 정보를 첫 번째 리스트와 그 외 리스트로 분리합니다.
                        player_info = f"{order_text} {name_text} {position_text}"
                        if lineup_list == lineup_lists[0]:
                              converted_players_away.append(player_info)
                        else:
                              converted_players_home.append(player_info)
            
      return converted_players_away, converted_players_home


def ReadLineUp(url, verbose=True):
      try:
            driver = setup_driver(url + '/lineup')
            soup = parse_html(driver)
            
            Lineup_List = 'Lineup_lineup_list__1_CNQ'
            Lineup_Item = 'Lineup_lineup_item__32s4M'
            
            away, home = extract_players(soup, Lineup_List, Lineup_Item, verbose)
            
            """for player in converted_players:
                  print(player)"""
                  
            return away, home
                  
      except Exception as e:
            print(f'Error: {str(e)}')
      finally:
            driver.quit()

"""
def ReadRelay(url):
      driver = setup_driver(url + '/relay')

      try:
            for num in range(1, 10):
                  button_css_selector = f"#content > div > div.Home_main_section__y9jR4 > section.Home_game_panel__97L_8 > div.Home_game_contents__35IMT > div > div.SetTab_tab_list__1HLl0 > div > div > button:nth-child({num})"
                  if click_button_and_wait(driver, button_css_selector):
                        print(f'*************** {num}회 ***************\n')
                        soup = parse_html(driver)

                        player_areas = soup.find_all(class_=relay_player_area)
                        for player_area in reversed(player_areas):
                              process_player_info(player_area, relay_player_info, relay_player_profile, relay_player_name, relay_batting_order)
                              process_main_info(player_area, relay_main_info, relay_text, relay_points)
                              process_history(player_area, relay_history, relay_pitch_num, relay_text, relay_stuff, relay_speed, relay_count, relay_change)

                        print('\n')

      except Exception as e:
            print(f'Error: {str(e)}')
      finally:
            driver.quit()
"""

def ReadRelay(url, verbose=True):
      away = None
      home = None
      
      try:
            # 선발투수 정보를 얻기 위해 먼저 URL로부터 가져옴
            lineup1, lineup2 = ReadLineUp(url)
            away = Team(lineup1[0])
            home = Team(lineup2[0])

            away.set_lineup(lineup1[1:])
            home.set_lineup(lineup2[1:])

            driver = setup_driver(url + '/relay')

            for inning in range(1, 10):
                  button_css_selector = f"#content > div > div.Home_main_section__y9jR4 > section.Home_game_panel__97L_8 > div.Home_game_contents__35IMT > div > div.SetTab_tab_list__1HLl0 > div > div > button:nth-child({inning})"
                  if click_button_and_wait(driver, button_css_selector):
                        if verbose:
                              print(f'*************** {inning}회 ***************\n')
                        soup = parse_html(driver)

                        player_areas = soup.find_all(class_=relay_player_area)
                        for player_area in reversed(player_areas):
                              batter_atbat = process_player_info(player_area, relay_player_info, relay_player_profile, relay_player_name, relay_batting_order, verbose)

                              # Find batter in away or home team
                              batter = away.find_batter_by_name(batter_atbat)
                              if batter is None:
                                    batter = home.find_batter_by_name(batter_atbat)

                              if batter:
                                    if batter.team == away.name:
                                          pitcher = home.current_pitcher
                                    else:
                                          pitcher = away.current_pitcher

                                    main_info = process_main_info(player_area, relay_main_info, relay_text, relay_points, verbose)

                                    # Check if main_info is valid
                                    if main_info:
                                          # AtBat 객체 생성
                                          atbat = AtBat(pitcher, batter, main_info)
                                          
                                          # 히스토리 가져오기
                                          get_history(atbat, player_area, relay_history, relay_pitch_num, relay_text, relay_stuff, relay_speed, relay_count, relay_change, verbose)
                                          pitcher.add_atbat(atbat)
                                          batter.add_atbat(atbat)
                                    else:
                                          print(f"Main info not found or invalid for {batter_atbat}")
                              else:
                                    print(f"Batter {batter_atbat} not found in either team")
                        if verbose: 
                              print('\n')

            print(away)
            print(home)

      except Exception as e:
            print(f'Error in ReadRelay: {str(e)}')
      finally:
            driver.quit()









