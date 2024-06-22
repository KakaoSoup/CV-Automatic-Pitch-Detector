class AtBat:
      def __init__(self, pitcher, batter, main_info):
            self.pitch_histories = []
            self.main_info = main_info
            self.pitcher = pitcher
            self.batter = batter

      def add_history(self, history):
            self.pitch_histories.append(history)

      def add_info(self, pitcher, batter, main_info):
            self.pitcher = pitcher
            self.batter = batter
            self.main_info = main_info

      def __str__(self):
            return f"AtBat: Pitcher={self.pitcher}, Batter={self.batter}, Main Info={self.main_info}, Pitch Histories={self.pitch_histories}"


class PitchHistory:
      def __init__(self, pitch_num, type, stuff, speed, count):
            super().__init__()
            self.pitch_num = pitch_num
            self.type = type
            self.stuff = stuff
            self.speed = speed
            self.count = count

      def __str__(self):
            return f"PitchHistory: Pitch Num={self.pitch_num}, Type={self.type}, Stuff={self.stuff}, Speed={self.speed}, Count={self.count}"


class BatterInfo:
      def __init__(self, order, name, team, position, hand):
            self.order = order
            self.name = name
            self.team = team
            self.position = position
            self.hand = hand
            self.atbat = []

      def add_atbat(self, atbat):
            self.atbat.append(atbat)

      def __str__(self):
            return f"BatterInfo: Order={self.order}, Name={self.name}, Position={self.position}, Hand={self.hand}, AtBats={self.atbat}"


class PitcherInfo:
      def __init__(self, name, hand):
            self.name = name
            self.hand = hand
            self.atbat = []
            self.pitch_cnt = 0
            self.strikes = 0
            self.balls = 0

      def add_atbat(self, atbat):
            self.atbat.append(atbat)
            self.pitch_cnt += len(atbat.pitch_histories)

      def __str__(self):
            return f"PitcherInfo: Name={self.name}, Hand={self.hand}, Pitch Count={self.pitch_cnt}, Strikes={self.strikes}, Balls={self.balls}, AtBats={self.atbat}"


class Team:
      def __init__(self, name):
            self.name = name
            self.pitchers = []
            self.batters = []
            self.current_pitcher = None;

      def __str__(self):
            return f"Team: Name={self.name}, Pitchers={self.pitchers}, Batters={self.batters}"
      
      def set_pitcher(self, pitcher):
            self.pitchers.append(pitcher)
            self.current_pitcher = pitcher
      
      def set_lineup(self, lineup):
            for player in lineup:
                  player = player.replace(', ', ' ')
                  player_info = player.split(' ')
                  if player_info[0] == '선발':
                        self.set_pitcher(PitcherInfo(player_info[1], player_info[2]))
                  else:
                        self.batters.append(BatterInfo(player_info[0], player_info[1], self.name, player_info[2], player_info[3]))
                        
      def find_batter_by_name(self, name):
            for batter in self.batters:
                  if batter.name == name:
                        return batter
            return None
      






















