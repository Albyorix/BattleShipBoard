
class Boat:

    def __init__(self, boat, boat_id):
        self.boat_id = boat_id
        self.position_x = int(boat[0])
        self.position_y = int(boat[1])
        self.direction = boat[2]
        self.is_wreck = False

    def rotate_left(self):
        if self.direction == 'N':
            self.direction = 'W'
        elif self.direction == 'W':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'N'
        else:
            raise Exception('Boat direction was changed with ' + str(self.direction))

    def rotate_right(self):
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'W':
            self.direction = 'N'
        elif self.direction == 'S':
            self.direction = 'W'
        elif self.direction == 'E':
            self.direction = 'S'
        else:
            raise Exception('Boat direction was changed with ' + str(self.direction))

    def move_forward(self):
        if self.direction == 'N':
            self.position_y += 1
        elif self.direction == 'W':
            self.position_x -= 1
        elif self.direction == 'S':
            self.position_y -= 1
        elif self.direction == 'E':
            self.position_x += 1
        else:
            raise Exception('Boat direction was changed with ' + str(self.direction))

    def sink(self):
        self.is_wreck = True

    def __repr__(self):
        output_string = '(' + str(self.position_x)
        output_string += ', ' + str(self.position_y)
        output_string += ', ' + self.direction + ')'
        if self.is_wreck:
            output_string += ' SUNK'
        output_string += '\n'
        return output_string


class BattleShipBoard:

    def __init__(self, path):
        f = open(path)
        self.size = int(f.readline()[:-1])
        if self.size <= 0:
            raise Exception('Board game size has to be strictly positive')
        self.raw_boats = f.readline()
        self.raw_actions = f.read()
        f.close()
        self.process_input_strings()
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.boats = [] # This is a list to access the boats by id number
        for i in range(len(self.new_boats)):
            # boats ids are 0, 1 ... len(boats)-1
            self.boats.append(Boat(self.new_boats[i], i))
            if (self.boats[-1].position_x >= self.size
                    or self.boats[-1].position_y >= self.size
                    or self.boats[-1].position_x < 0
                    or self.boats[-1].position_y < 0):
                raise Exception('It is forbidden to place a boat outside the board')
            elif not self.grid[self.boats[-1].position_x][self.boats[-1].position_y] is None:
                raise Exception('It is forbidden to place two boats on the same square')
            else:
                self.grid[self.boats[-1].position_x][self.boats[-1].position_y] = self.boats[-1]

    def process_input_strings(self):
        # Replace : "(0, 0, N) (1, 1, E)\n"
        # With : [['0','0','N'],['1','1','E']]
        self.new_boats = self.raw_boats.replace(' ', '')
        self.new_boats = self.new_boats.replace('(', '')
        self.new_boats = self.new_boats.split(')')
        self.new_boats = self.new_boats[:-1]
        for i in range(len(self.new_boats)):
            self.new_boats[i] = self.new_boats[i].split(',')
        # Replace : "(0, 0) RR\n(0, 0)\n(1, 1) M"
        # with : [[['0','0'],'RR'],[['0','0'],''],[['1','1'],'M']]
        tmp_actions = self.raw_actions.replace('(', '')
        tmp_actions = tmp_actions.replace(' ', '')
        self.actions = tmp_actions.split('\n')
        if self.actions[-1] == '':
            self.actions = self.actions[:-1]
        for i in range(len(self.actions)):
            self.actions[i] = self.actions[i].split(')')
            self.actions[i][0] = self.actions[i][0].split(',')

    def move(self, position_x, position_y, sequence):
        if self.grid[position_x][position_y] is None:
            raise Exception('There is no boat in this position: ' + str((position_x, position_y)))
        else:
            boat = self.grid[position_x][position_y]
            self.grid[position_x][position_y] = None
            for i in sequence:
                if i == 'L':
                    boat.rotate_left()
                elif i == 'R':
                    boat.rotate_right()
                elif i == 'M':
                    boat.move_forward()
                    if (boat.position_x < 0
                            or boat.position_x >= self.size
                            or boat.position_y < 0
                            or boat.position_y >= self.size):
                        raise Exception('Move forbidden, the boat cannot exit the grid')
                else:
                    raise Exception('Movement %s not defined' % i)
            if self.grid[boat.position_x][boat.position_y] is None:
                self.grid[boat.position_x][boat.position_y] = boat
            else:
                raise Exception('There is already a boat in this position: ' + str((boat.position_x, boat.position_y)))

    def shoot(self, position_x, position_y):
        if self.grid[position_x][position_y] is None:
            pass  # There was no boat : nothing happens
        else:
            # The boat is sink and disappear from the grid
            self.grid[position_x][position_y].sink()
            self.grid[position_x][position_y] = None

    def run(self):
        for action in self.actions:
            if action[1] == '':
                self.shoot(int(action[0][0]), int(action[0][1]))
            else:
                self.move(int(action[0][0]), int(action[0][1]), action[1])

    def save_output(self, path):
        f = open(path, 'w')
        f.write(self.__repr__())
        f.close()

    def compare_outputs(self, path, test_number):
        f = open(path)
        true_output = f.read()
        f.close()
        output = self.__repr__()
        if true_output == output:
            print "The test %i was cleared" % test_number
        elif true_output + "\n" == output:  # test if there is just a missing line
            print "The test %i was cleared" % test_number
        else:
            print "The test %i failed" % test_number

    def __repr__(self):
        output_string = str(self.size) + '\n'
        for boat in self.boats:
            output_string += boat.__repr__()
        return output_string


if __name__ == "__main__":

    # 8 Tests that should work:
    for i in range(1, 9):
        test_path = 'Tests/Tests/test_' + str(i) + '.txt'
        my_battleship_board = BattleShipBoard(test_path)
        my_battleship_board.run()
        save_path = 'Tests/Results/output_' + str(i) + '.txt'
        my_battleship_board.save_output(save_path)
        output_path = 'Tests/Tests/output_' + str(i) + '.txt'
        my_battleship_board.compare_outputs(output_path, i)

    # 5 Tests that should fail:
    for i in range(1, 6):
        test_path = 'Tests/Error_tests/test_' + str(i) + '.txt'
        try:
            my_battleship_board = BattleShipBoard(test_path)
            my_battleship_board.run()
        except:
            print "The fail test %i was cleared" % i

