import ik
import main
import time

current_pos = [0, 0]
i = 0

x_array = [1600,0,800]
y_array = [3200,800,0]

# def coords_to_string(coords):
#     c1, c2 = coords
#     string = f"{c1},{c2}"
#     return string

def test_func(x,y):
    return x, y

# def relative_steps(stored_pos, desired_pos_func, x, y):
#     needed_steps =  
#     return needed_steps

def move_to(x, y, stored_pos, pos_func):
    # Get the actuated steps by comparing the desired position and current position
    actuated_steps = (pos_func(x, y)[0] - stored_pos[0], pos_func(x, y)[1] - stored_pos[1])
    # movement = main.write_read(f"{actuated_steps[0]},{actuated_steps[1]}")
    movement = f"{actuated_steps[0]},{actuated_steps[1]}"
    main.write_read(movement)
    # Update the current_pos by adding the actuated steps
    stored_pos[0] += actuated_steps[0]
    stored_pos[1] += actuated_steps[1]

    return movement

# move_to(1600, 1600, current_pos, test_func)
# move_to(-800, 3200, current_pos, test_func)
# move_to(0, 0, current_pos, test_func)

def full_movement(x_arr, y_arr):
    for x, y in zip(x_arr, y_arr):  # Use zip() to iterate over two lists simultaneously
        move_to(x, y, current_pos, test_func)  # Assuming move_to is a predefined function
        time.sleep(5)  # Pause for 1 second between movements


full_movement(x_array,y_array)