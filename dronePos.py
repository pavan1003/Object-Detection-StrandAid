import time
import random

def display_matrix(matrix):
    print('-' * (len(matrix[0]) + 2))
    for row in matrix:
        print('|' + ''.join(row) + '|')
    print('-' * (len(matrix[0]) + 2))

def move_roaming_object(matrix, roaming_object_pos, direction):
    x, y = roaming_object_pos
    dx, dy = direction
    if 0 <= x + dx < len(matrix) and 0 <= y + dy < len(matrix[0]) and matrix[x + dx][y + dy] != 'X':
        matrix[x][y] = ' '
        matrix[x + dx][y + dy] = 'O'
        return (x + dx, y + dy), direction
    else:
        direction = (-dx, -dy)
    return roaming_object_pos, direction


def main():
    matrix = [[' ' for _ in range(20)] for _ in range(20)]
    for i in range(10):
        matrix[random.randint(0, 19)][random.randint(0, 19)] = 'X'
    roaming_object_pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    for pos in roaming_object_pos:
        x, y = pos
        matrix[x][y] = 'O'
    direction = [(1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
    while True:
        display_matrix(matrix)
        new_roaming_object_pos = []
        new_direction = []
        for i in range(len(roaming_object_pos)):
            pos, dir = move_roaming_object(matrix, roaming_object_pos[i], direction[i])
            new_roaming_object_pos.append(pos)
            new_direction.append(dir)
        roaming_object_pos = new_roaming_object_pos
        direction = new_direction
        time.sleep(1)

if __name__ == '__main__':
    main()
