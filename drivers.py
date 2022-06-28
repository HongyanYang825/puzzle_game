'''
    CS5001
    Fall 2021
    Final_Project_Drivers

    Define a bunch of drivers to support the main program in
    puzzle_game

    Hongyan Yang
'''


import turtle
import random
import time

def load_window(window, start_point, horizontal, vertical,
                width = 6, color = "black", speed = 0):
    '''
    Function -- load_window
    Draw a window at preset position with adjustable side_length
    Parameters: window (str)  -- current window to load
                start_point (tuple) -- start position
                horizontal (float) -- window's horizontal length
                vertical (float) -- window's vertical length
                width, color, speed -- default pen information        
    Draw a window at pre-determined position with specific size
    '''
    temp_str = window
    # Create a turtle to draw the window
    locals()[temp_str] = turtle.Turtle(visible = False)
    locals()[temp_str].speed(speed)
    locals()[temp_str].width(width)
    locals()[temp_str].pencolor(color)
    locals()[temp_str].penup()
    locals()[temp_str].goto(start_point)
    locals()[temp_str].pendown()
    for i in range(4):
        if (i % 2):
            locals()[temp_str].forward(vertical)
            locals()[temp_str].right(90)
        else:
            locals()[temp_str].forward(horizontal)
            locals()[temp_str].right(90)
    return locals()[temp_str]

def print_leaders(leader, text, start_point, color = "blue",
                  font=("Arial",16, "bold"), speed = 0):
    '''
    Function -- print_leaders
    Print leader's name and record in the leaders board
    Parameters: leader (str) -- current learder to print
                start_point (tuple) -- start position
                color, font, speed -- default pen information        
    Load a leader and his/her record in the leaderboard
    '''
    temp_str = leader
    # Create a turtle to print the leader
    locals()[temp_str] = turtle.Turtle(visible = False)
    locals()[temp_str].speed(speed)
    locals()[temp_str].pencolor(color)
    locals()[temp_str].penup()
    locals()[temp_str].goto(start_point)
    locals()[temp_str].pendown()
    # Print the leader and his/her record
    locals()[temp_str].write(text, font = font, align="left")

def load_leaders(leaders_file_name: str) -> list:
    '''
    Function -- load_leaders
    Load leaders and record from an input file and load their record in
    an ascending order, each leader loads his/her best personal record
    Parameters: leaders_file_name (str) -- input leaders' info file
    Returns a dictionary with leaders' names and records 
    '''
    with open(leaders_file_name, 'r', encoding='utf-8') as infile:
        temp_dict = {} 
        for line in infile:
            # Extract each line of info and add to the dictionary 
            temp_list = line.split(": ")
            # Each leader loads his/her best personal record
            try:
                if int(temp_list[1]) < temp_dict[temp_list[0].title()]:
                    temp_dict[temp_list[0].title()] = int(temp_list[1])
            except:
                temp_dict[temp_list[0].title()] = int(temp_list[1])
    # Records are sorted in an ascending order
    dict_out = {k: v for k, v in sorted(temp_dict.items(),
                                        key = lambda item: item[1])}
    return list(dict_out.items())

def load_icon(screen, icon_file_name, start_point, speed = 0):
    '''
    Function -- load_icon
    Load specific button icon to the canvas at pre-determined position
    Parameters: screen -- current canvas
                icon_file_name (str) -- gif icon file to load
                start_point (tuple) -- start position
                speed -- default tuple's drawing speed
    Create a specific button on the canvas
    '''
    screen.addshape(icon_file_name) # Register gif icon to canvas
    # Create a turtle to load the icon
    icon = turtle.Turtle(visible = False)
    icon.hideturtle()
    icon.speed(speed)
    icon.shape(icon_file_name)
    icon.penup()
    icon.goto(start_point)
    icon.showturtle()
    return icon

def generate_loc(length, interval, num):
    '''
    Function -- generate_loc
    Generate tile frame's position based on number of tiles
    Parameters: length (float) -- tile frame's side-length
                interval (float) -- interval between two frames
                num (int) -- number of puzzle tiles
    Return tile frames' positions as a dictionary
    '''
    dict_out = {}
    side_num = int(num ** 0.5)
    # Make adjustment to ensure positions are always in the center
    adjustment = (((interval - 2) * (side_num - 1) +
                   (length - 98) * side_num) / 2)
    start_point_x, start_point_y = -270 - adjustment, 236.5 + adjustment
    for i in range(num):
        temp_str = "loc_" + str(num - i)
        coord_x =  start_point_x + (i % side_num) * (length + interval)
        coord_y = start_point_y - (i // side_num) * (length + interval)
        dict_out[temp_str] = (coord_x, coord_y)
    return dict_out

def reset_dics(num):
    '''
    Function -- reset_dics
    Reset tile mapping dictionaries to default value
    Parameters: num (int) -- number of puzzle tiles
    Return two tile mapping dictionaries with values reset
    '''
    loc_tile_dict, tile_loc_dict= {}, {}
    for i in range(num - 1):
        loc_tile_dict[("loc_"+ str(num - i))] = ("tile_" + str(num - i))
        tile_loc_dict[("tile_" + str(num - i))] = ("loc_"+ str(num - i))
    loc_tile_dict["loc_1"] = "tile_blank"   # Rename tile_1 to tile_blank
    tile_loc_dict["tile_blank"] = "loc_1"
    return loc_tile_dict, tile_loc_dict

def pre_load_puzzle_tiles(location_dict, length, interval, diffic, num):
    '''
    Function -- pre_load_puzzle_tiles
    Calculate what the tiles mapping should be given a certain difficulty
    level, all calculation steps are processed in the back end
    Parameters: location_dict (dict) -- tile frames' positions dict
                length (float) -- tile frame's side-length
                interval (float) -- interval between two frames
                diffic (num) -- adjustable puzzle difficulty level
                number (int) -- number of puzzle tiles
    Return two tile mapping dictionaries given a certain difficulty level
    '''
    loc_tile_dict, tile_loc_dict = reset_dics(num)
    # Create a list containing all movable tiles at each "move"
    for i in range(diffic):
        move_list = []
        for j in range(num):
            if is_near_blank("loc_" + str(j + 1), location_dict,
                             tile_loc_dict, length, interval):
                move_list.append("loc_" + str(j + 1))
        # "Move" the blank tile to a random movable location
        move_to_loc = move_list[random.randint(0, (len(move_list) - 1))]
        # Make changes accordingly to tiles mapping dictionaries
        blank_loc = tile_loc_dict["tile_blank"]
        moved_tile = loc_tile_dict[move_to_loc]
        tile_loc_dict["tile_blank"] = move_to_loc
        tile_loc_dict[moved_tile] = blank_loc
        loc_tile_dict[move_to_loc] = "tile_blank"
        loc_tile_dict[blank_loc] = moved_tile
    # Keeping calculating if tiles happened to be not mixed, it's recursive
    if (loc_tile_dict, tile_loc_dict) != reset_dics(num):
        return loc_tile_dict, tile_loc_dict
    else:
        return pre_load_puzzle_tiles(location_dict, length,
                                     interval, diffic, num)

def load_puzzle_tiles(nm, screen, location_dict, length, interval,
                      side_length, num, difficulty, width = 1.5):
    '''
    Function -- load_puzzle_tiles
    Load tiles based on calculated mapping dictionaries given a certain
    difficulty level and return updated tiles' mapping dictionaries
    Parameters: nm (str) -- current puzzle's name
                location_dict (dict) -- tile frames' positions dict
                length (float) -- tile frame's side-length
                interval (float) -- interval between two frames
                side_length (float) -- current puzzle tile's side-length
                num (int) -- number of puzzle tiles
                difficulty (num) -- adjustable puzzle difficulty level
                width (float) -- tile frame's pen width
    Return tile mapping dictionaries given a certain difficulty level
    '''
    t = pre_load_puzzle_tiles(location_dict, length, interval, difficulty, num)
    (loc_tile_dict, tile_loc_dict) = t
    tile_mem_address_dict = frame_dict = {}
    for i in range(num): 
        dict_key = "loc_" + str(num - i)
        tile_str = loc_tile_dict[dict_key]
        start_point_x = location_dict[dict_key][0] - (side_length / 2)
        start_point_y = location_dict[dict_key][1] + (side_length / 2)
        value = load_window("frame_" + str(num - i),
                            (start_point_x, start_point_y),
                            side_length, side_length, width)
        frame_dict["frame_" + str(num - i)] = value
        locals()[tile_str] = load_icon(screen,
                                       f"Images/{nm}/{str(tile_str[5:])}.gif",
                                       location_dict[dict_key], speed = 0)
        tile_mem_address_dict[tile_str] = locals()[tile_str]
    return loc_tile_dict, tile_loc_dict, tile_mem_address_dict, frame_dict

def get_loc_name(location_dict, x, y):
    '''
    Function -- get_loc_name
    Get the nearest tile's location name given the position of mouse click
    Parameters: location_dict (dict) -- tile frames' positions dict
                x,y (float) -- position of mouse click
    Return the nearest tile's location name
    '''
    temp_dict = {}
    for each in location_dict.items():
        # Calculate different tile center's distance to mouse click
        distance = (each[1][0] - x) ** 2 + (each[1][1] - y) ** 2
        temp_dict[each[0]] = distance
    distance_dict = {k: v for k, v in
                     sorted(temp_dict.items(), key=lambda item: item[1])}
    nearest_loc = list(distance_dict.keys())[0]
    return nearest_loc
        
def is_near_blank(n_loc, location_dict, tile_loc_dict, length, interval):
    '''
    Function -- is_near_blank
    Check if the tile clicked is near the blank tile
    Parameters: n_loc (str) -- the nearest tile's location name
                location_dict (dict) -- tile frames' positions dict
                tile_loc_dict (dict) -- tile-location mapping dict
                length (float) -- tile frame's side-length
                interval (float) -- interval between two frames
    Return a boolean shows if the tile clicked is near the blank tile
    '''
    pos = location_dict[n_loc]
    blank_pos = location_dict[tile_loc_dict["tile_blank"]]
    distance = (pos[0] - blank_pos[0]) ** 2 + (pos[1] - blank_pos[1]) ** 2
    # Return True iff the tile clicked is next to the blank tile
    if distance == (length + interval) ** 2:
        return True
    else:
        return False

def switch_blank(nearest_loc, location_dict, loc_tile_dict,
                 tile_loc_dict, tile_mem_address_dict):
    '''
    Function -- switch_blank
    Switch the blank tile with a neighboring tile clicked by the mouse 
    Parameters: nearest_loc (str) -- the nearest tile's location name
                location_dict (dict) -- tile frames' positions dict
                loc_tile_dict (dict) -- location-tile mapping dict
                tile_loc_dict (dict) -- tile-location mapping dict
                tile_mem_address_dict (float) -- tile-turtle mapping info
    Return updated tile and location mapping dictionaries
    '''
    cur_loc = nearest_loc
    cur_tile = loc_tile_dict[cur_loc]
    blank_loc = tile_loc_dict['tile_blank']
    # Retrieve the turtle object binded to a certain tile
    cur_tile_obj = tile_mem_address_dict[cur_tile]
    cur_pos = location_dict[cur_loc]
    blank_tile_obj = tile_mem_address_dict['tile_blank']
    blank_pos = location_dict[blank_loc]
    # Switch the blank tile with the neighboring tile 
    cur_tile_obj.goto(blank_pos)
    blank_tile_obj.goto(cur_pos)
    # Update tile and location mapping dictionaries
    loc_tile_dict[cur_loc] = 'tile_blank'
    loc_tile_dict[blank_loc] = cur_tile
    tile_loc_dict['tile_blank'] = cur_loc
    tile_loc_dict[cur_tile] = blank_loc
    return loc_tile_dict, tile_loc_dict

def move_counter(turtle, count, start_point = (-305, -305),
                 color = "black", font=("Arial",18, "bold"), speed = 0):
    '''
    Function -- move_counter
    Update player's move counts after each valid mouse click
    Parameters: turtle -- a turtle writes the counts
                count (int) -- number of player's moves
                start_point, color, font, speed -- default turtle setup
    Move the counter turtle and write number of player's moves
    '''
    text = "Player Moves: " + str(count)
    turtle.speed(speed)
    turtle.pencolor(color)
    turtle.penup()
    turtle.goto(start_point)
    turtle.pendown()
    turtle.write(text, font = font, align="left")
    
def reset_tiles(name, screen, location_dict, loc_tile_dict,
                tile_loc_dict, tile_mem_address_dict, num):
    '''
    Function -- reset_tiles
    Reset puzzle tiles to default status and update tiles mapping info
    Parameters: name (str) -- current puzzle's name
                screen -- current canvas
                location_dict (dict) -- tile frames' positions dict
                loc_tile_dict (dict) -- location-tile mapping dict
                tile_loc_dict (dict) -- tile-location mapping dict
                tile_mem_address_dict (float) -- tile-turtle mapping info
                num (int) -- number of puzzle tiles
    Return updated tile and location mapping dictionaries
    '''
    for i in range(num - 1):
        # Reset tiles position one by one
        switch_blank("loc_" + str(num - i), location_dict, loc_tile_dict,
                     tile_loc_dict, tile_mem_address_dict)
        target_tile_loc = tile_loc_dict["tile_" + str(num - i)]
        switch_blank(target_tile_loc, location_dict, loc_tile_dict,
                 tile_loc_dict, tile_mem_address_dict)
    # Update tile and location mapping dictionaries
    return loc_tile_dict, tile_loc_dict, tile_mem_address_dict

def write_leaders(leaders_list: list, file_out: str) -> None:
    '''
    Function -- write_leaders
    Create an output file with lines of player records
    Parameters: leaders_list (list) -- a list of players' records
                file_out (str) -- an output file records player info
    Create an output file to record players' record
    '''
    try:
        with open(file_out, 'w', encoding='utf-8') as outfile:
            for each in leaders_list:
                # Join elements by ": " for each in input list
                temp_str = each[0] + ": " + str(each[1])
                # Write joined string into outfile as a line of record
                outfile.write(temp_str + "\n")
    except OSError:
        pass

def write_err(error_log: list, file_out: str) -> None:
    '''
    Function -- write_err
    Create an output file with lines of error logs
    Parameters: error_log (list) -- a list of error logs
                file_out (str) -- an output file records error logs
    Create an output file to record error logs
    '''
    try:
        with open(file_out, 'a', encoding='utf-8') as outfile:
            for each in error_log:
                # Join elements by ": " for each in input list
                temp_str = each[0] + ": " + str(each[1])
                # Write joined string into outfile as a line of record
                outfile.write(temp_str + "\n")
    except OSError:
        pass

def load__message(screen, message_file):
    '''
    Function -- load__message
    Create warning messages when errors occur
    Parameters: screen -- current canvas
                message_file (gif) -- warning gif file
    Show warnings when errors occur
    '''
    temp_turtle = load_icon(screen, message_file, (0, 0))
    time.sleep(1.2)
    temp_turtle.shape("classic")
    temp_turtle.hideturtle()
