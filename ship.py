from math import sqrt, isclose
import copy

def interpolate(pos1, pos2, t):
  """
  t = 0 -> x1, t = 1 -> x2
  """
  x = (1 - t) * pos1[0] + t * pos2[0]
  y = (1 - t) * pos1[1] + t * pos2[1]
  return [x, y]

def distance(pos1, pos2):
  return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

class CycleUnit:
  def __init__(self):
    self.speed = 0
    self.knot = 0
    self.path = [] #경로
    self.length_list = [] #경로들의 길이
    self.num_path = 0
    self.x = 0
    self.y = 0
    self.num = 0
    self.time = 0
    self.detection_dist = 0
    self.detection_on = 0
    
 
  def test_print(self, x):
    print(x)
  
  def add_path(self, x, y): 
    """
    경로 목록에 [x, y]를 추가함.
    경로 목록은 항상 시작 출발점과 도착점이 같아야함.
    """
    if self.num_path == 0:
      self.path = [[x, y], [x, y]]
    else:
      self.path.insert(self.num_path, [x, y]) #마지막 원소 바로 전에 삽입
    self.num_path = self.num_path + 1

    # 모든 경로의 길이 계산
    if self.num_path > 1:
      self.update_length()
    else:
      self.x = x
      self.y = y

  def update_length(self):
    self.length_list = []
    for i in range(self.num_path):
      self.length_list.append(distance(self.path[i], self.path[(i + 1)%self.num_path]))


  def delete_path(self, path_idx):
    if len(self.path) > 2:
      self.path.remove(self.path[path_idx])
      # for i in range(len(self.path)):
      #   print("{} {}".format(self.path[i][0], self.path[i][1]))
      self.num_path -= 1
      self.update_length()
      return True
    else: return False


  def set_x(self, x):
    self.x = x

  def set_y(self, y):
    self.y = y

  def set_speed(self, speed):
    self.speed = speed

  def set_knot(self, knot):
    self.knot = knot
    self.speed = self.knot / 60

  def set_detection(self, dist):
    self.detection_dist = dist
      
  def get_position(self):
    return [self.x, self.y]


  def get_x(self):
    return self.x


  def get_y(self):
    return self.y


  def get_knot(self):
    return self.knot


  def get_detection_dist(self):
    return self.detection_dist


  def get_path(self):
    return self.path

  def print_position(self):
    print("x = {}, y = {}".format(self.x, self.y))

  def length_to_time(self, length):
    """
    주어진 길이를 속도로 나눠 걸리는 시간을 반환
    """
    return length / self.speed

  def advance(self, time):
    """
    ship 객체를 time 만큼 전진시킴.
    """
    self.time = self.time + time
    self.x, self.y = self.current_pos()
    # print("Position at time {} is".format(self.time), end=' ')
    # print(" {0} {1}".format(self.x, self.y), end='\n')
    return self.x, self.y

  def current_pos(self):
    """
    ship 객체의 전진한 시간을 현재 위치로 반환한다.
    """
    #경로 전체의 길이 합
    sum_path = sum(self.length_list)
    #경로 전체를 한바퀴 도는데 걸리는 시간
    total_time = 1
    total_time = self.length_to_time(sum_path)
    if total_time == 0:
      total_time = 1

    #현재 ship의 시간을 한바퀴 시간으로 나눈 나머지.
    # remain_time = float(Decimal(str(self.time)) % Decimal(str(total_time)))
    remain_time = self.time % float(total_time)
    #경로 index는 0부터 시작함.
    idx = 0

    #남은 시간이 현재 경로의 시간보다 클때,
    while remain_time > self.length_to_time(self.length_list[idx]):
      #남은 시간에 현재 경로의 시간을 차감함.
      remain_time = remain_time - self.length_to_time(self.length_list[idx])
      #경로 index를 1 증가시킴
      idx = (idx + 1) % self.num_path

    #이제 idx는 현재 path의 index임. 시간을 0 ~ 1로 정규화 시킴.
    lt = self.length_to_time(self.length_list[idx])
    if lt != 0:
      unit_time = float(remain_time) / self.length_to_time(self.length_list[idx])
    else:
      unit_time = 0
    #보간 연산을 통해 현재 ship의 위치를 계산함.
    current_pos = interpolate(self.path[idx], self.path[(idx + 1) % self.num_path], unit_time)
    
    return current_pos
  
  def detection(self, target):
    dist = distance(self.get_position(), target.get_position())
    if dist <= self.detection_dist and self.detection_on == 0:
      self.detection_on = 1
      return 1, dist
    elif dist > self.detection_dist and self.detection_on == 1:
      self.detection_on = 0
      return 0, dist
    else:
      return -1, dist


class LineUnit:
  def __init__(self):
    self.speed = 0
    self.knot = 0
    self.path = [] #경로
    self.length_list = [] #경로들의 길이
    self.num_path = 0
    self.x = 0
    self.y = 0
    self.num = 0
    self.time = 0
    self.delay = 0
    
 
  def print_position(self):
    print("x = {}, y = {}".format(self.x, self.y))
  
  def add_path(self, x, y): 
    """
    경로 목록에 [x, y]를 추가함.
    경로는 단방향.
    """
    # if self.num_path == 0:
    #   self.path = [[x, y], [x, y]]
    # else:
    #   self.path.insert(self.num_path, [x, y]) #마지막 원소 바로 전에 삽입
    self.path.append([x,y])
    self.num_path = self.num_path + 1
    # 모든 경로의 길이 계산
    if self.num_path > 1:
      self.length_list = []
      for i in range(self.num_path-1):
        self.length_list.append(distance(self.path[i], self.path[i + 1]))
    else:
      self.x = x
      self.y = y

  def set_speed(self, speed):
    self.speed = speed

  def set_knot(self, knot):
    self.knot = knot
    self.speed = self.knot / 60

  def set_delay(self, delay):
    self.delay = delay 
      
  def get_position(self):
    return [self.x, self.y]

  def get_position2(self):
    return self.x, self.y

  def length_to_time(self, length):
    """
    주어진 길이를 속도로 나눠 걸리는 시간을 반환
    """
    return length / self.speed

  def advance(self, time):
    """
    ship 객체를 time 만큼 전진시킴.
    """
    if self.delay > 0:
      self.x = -999
      self.y = -999
      self.delay -= time
      # print("delay = {} self.time = {} , -= {}".format(self.delay, self.time, self.delay - time))
    else:
      self.x = self.path[0][0]
      self.y = self.path[0][1]
      self.time = self.time + time
      self.x, self.y = self.current_pos()
      # print("Position at time {} is".format(self.time), end=' ')
      # print(" {0} {1}".format(self.x, self.y), end='\n')
      # print(self.time_to_pos())
      return self.x, self.y

  def current_pos(self):
    """
    ship 객체의 전진한 시간을 현재 위치로 반환한다.
    """
    #경로 전체의 길이 합
    sum_path = sum(self.length_list)
    #경로 전체를 한바퀴 도는데 걸리는 시간
    total_time = 1
    total_time = self.length_to_time(sum_path)
    cur_time = copy.deepcopy(self.time)
    idx = 0

    if total_time >= cur_time:
      while cur_time > self.length_to_time(self.length_list[idx]):
        cur_time -=self.length_to_time(self.length_list[idx])
        idx = (idx + 1) % self.num_path
      unit_time = float(cur_time) / self.length_to_time(self.length_list[idx])
      current_pos = interpolate(self.path[idx], self.path[(idx + 1) % self.num_path], unit_time)
    else:
      return [self.x, self.y] 

    return current_pos

if __name__ == "__main__":
  ship = Ship()
  ship.set_speed(4)
  ship.add_path(0, 0)
  ship.add_path(0, 10)
  ship.add_path(20, 10)
  ship.add_path(20, 0)
  
  for _ in range(10):
    ship.advance(2)