from robot import Robot
from utils import print_progress_matrix, print_matrix
from position import Position
from queue import Queue
from math import fabs


class Sweeper:
    robot = None
    observed_maps = None

    def __init__(self, robot: Robot, maps):
        self.robot = robot
        self.observed_maps = maps
        self.observed_maps[self.robot.position.y][self.robot.position.x] = 1

    def work(self):
        start_position = self.robot.position
        while True:
            path, target_position = self.find_path(self.observed_maps, start_position)
            if target_position == None:
                break
            self.move_robot(path)
            start_position = target_position
            
            #print_progress_matrix(self.observed_maps)
            #print_progress_matrix(self.robot.maps)
            #input('press to continue...')
    
    def find_path(self, maps, from_position: Position):
        adj_queue = Queue()
        visited = dict()
        previous = dict()
        adj_queue.put(from_position)
        target_position = None

        while not adj_queue.empty():
            position = adj_queue.get()
            if not position.pos() in visited.keys():
                visited[position.pos()] = True
                if maps[position.y][position.x] >= 0:
                    target_position = position
                    break
                pos = Position(position.x + 1, position.y)
                if position.x < len(maps[0]) - 1 and maps[position.y][position.x + 1] >= 0 and not pos.pos() in visited.keys():
                    adj_queue.put(pos)
                    previous[pos.pos()] = position

                pos = Position(position.x, position.y + 1)
                if position.y < len(maps) - 1 and maps[position.y + 1][position.x] >= 0 and not pos.pos() in visited.keys():
                    adj_queue.put(pos)
                    previous[pos.pos()] = position
                
                pos = Position(position.x - 1, position.y)
                if position.x > 0 and maps[position.y][position.x - 1] >= 0 and not pos.pos() in visited.keys():
                    adj_queue.put(pos)
                    previous[pos.pos()] = position
                
                pos = Position(position.x, position.y - 1)
                if position.y > 0 and maps[position.y - 1][position.x] >= 0 and not pos.pos() in visited.keys():
                    adj_queue.put(pos)
                    previous[pos.pos()] = position

        path = self.get_path(from_position, target_position, previous)
        
        return path, target_position
    
    def move_robot(self, path):
        while len(path) > 0:
            next_pos = path.pop()
            print(self.robot.position.pos(),'-->',next_pos.pos())
            direction = 0
            if next_pos.x == self.robot.position.x + 1:
                direction = 0
            if next_pos.y == self.robot.position.y + 1:
                direction = 1
            if next_pos.x == self.robot.position.x - 1:
                direction = 2
            if next_pos.y == self.robot.position.y - 1:
                direction = 3
            rotate = direction - self.robot.direction
            if rotate == -1 or rotate == 3:
                self.robot.turn_left()
            elif rotate == 1 or rotate == -3:
                self.robot.turn_right()
            elif fabs(rotate) == 2:
                self.robot.turn_left()
                self.robot.turn_left()
            
            if self.robot.move():
                self.observed_maps[next_pos.y][next_pos.x] += 1
            else:
                print(self.robot.position.pos(), next_pos.pos(), self.robot.maps[next_pos.y][next_pos.x], self.observed_maps[next_pos.y][next_pos.x])
                if (self.robot.position.pos()!=next_pos.pos()):
                    self.observed_maps[next_pos.y][next_pos.x] = -1
                    input('press any key...')

    def get_path(self, from_position, to_position, previous_log):
        path = []
        if to_position != None:
            pos = to_position.pos()
            path.append(to_position)
            while pos in previous_log.keys():
                previous_position = previous_log[pos]
                pos = previous_position.pos()
                if previous_position.x != from_position.x or previous_position.y != from_position.y:
                    path.append(previous_position)
        return path
