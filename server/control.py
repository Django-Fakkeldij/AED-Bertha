import ik
# import main

current_pos = [0, 0]
i = 0

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

    # Update the current_pos by adding the actuated steps
    stored_pos[0] += actuated_steps[0]
    stored_pos[1] += actuated_steps[1]

    return actuated_steps

print(move_to(5, 10, current_pos, test_func))
print(move_to(20, 30, current_pos, test_func))
print(move_to(-10, 0, current_pos, test_func))