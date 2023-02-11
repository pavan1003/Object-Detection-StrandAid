import random
import time

# Define the main matrix
main_matrix = [[' ' for i in range(22)] for j in range(22)]

# Add borders to the main matrix
for i in range(22):
    main_matrix[i][0] = '|'
    main_matrix[i][21] = '|'
    main_matrix[0][i] = '-'
    main_matrix[21][i] = '-'

# Define the obstacle
for i in range(5):
    x = random.randint(1,20)
    y = random.randint(1,20)
    main_matrix[x][y] = 'X'

# Define the drone swarm as a submatrix
drone_swarm = [['O' for i in range(3)] for j in range(3)]

# Initial position of the drone swarm
swarm_x = 1
swarm_y = 1

# Moving the drone swarm continuously
while True:
    # Clear the previous position of the drone swarm
    for i in range(3):
        for j in range(3):
            main_matrix[swarm_x + i][swarm_y + j] = ' '
    
    # Check if the next move will hit an obstacle or a border
    if main_matrix[swarm_x + 3][swarm_y + 3] != 'X' and main_matrix[swarm_x + 3][swarm_y + 3] != '-' and main_matrix[swarm_x + 3][swarm_y + 3] != '|':
        swarm_x += 1
        swarm_y += 1
    elif main_matrix[swarm_x + 3][swarm_y] != 'X' and main_matrix[swarm_x + 3][swarm_y] != '-':
        swarm_x += 1
    elif main_matrix[swarm_x][swarm_y + 3] != 'X' and main_matrix[swarm_x][swarm_y + 3] != '|':
        swarm_y += 1
    else:
        swarm_x -= 1
    
    # Update the position of the drone swarm
    for i in range(3):
        for j in range():
            main_matrix[swarm_x + i][swarm_y + j] = drone_swarm[i][j]
    
    # Print the main matrix
    for row in main_matrix:
        print(*row)
    print()
    time.sleep(1)