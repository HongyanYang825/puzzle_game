'''
    CS5001
    Fall 2021
    Final_Project_Puzzle_Game

    Implement turtle library to create a solvable "15-puzzle" game
    with difficulty level adjustable

    Hongyan Yang
'''


import turtle
import time
import random
from datetime import datetime
from drivers import *
from gamepanel import *

DEFAULT_PUZ = "mario.puz"
DEFAULT_LEADERBOARD = "leaders.txt"
DEFAULT_ERRORLOG = "5001_puzzle.err"
wn = turtle.Screen()
pl = GamePanel()
pl.turtle.hideturtle()

def screen_setup(wn, width = 800, height = 800):
    '''
    Function -- screen_setup
    Setup the basic screen layout and get player's info and chances
    Parameters: wn -- current canvas
                width (int) -- canvas width
                height (int) -- canvas height
    Returns player's name and chances to move puzzle tiles
    '''
    wn.setup(width = 800, height = 800)
    wn.bgpic("Resources/splash_screen.gif")
    wn.update()
    time.sleep(1.2)
    wn.clearscreen()
    player = wn.textinput("CS5001 Puzzle Slide", "Your Name:")
    while not player:   # Force the player to enter a name 
        load__message(wn, "Resources/name_warning.gif")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pl.err.append((now, f"{player} not a valid player name."))
        player = wn.textinput("CS5001 Puzzle Slide", "Your Name:")
    chances = wn.numinput("5001 Puzzle Slide - Moves",
                          "Enter the number of moves (chances)"\
                          " you want (5-200)?", 50, minval = 5, maxval = 200)
    return player.title(), chances

def loading_splash(wn, duration = 24):
    '''
    Function -- loading_splash
    Create a loading screen to emulate the game loading process
    Parameters: wn -- current canvas
                duration (float) -- game "loading" time
    Load a splash screen "linger" 3-4 seconds before erased
    '''
    # Create a series of "splashes" each with different durations
    splash_interval = [(random.randint(1, 3) * 0.1) for i in range(duration)]
    splash_interval_adjust, step, bar_accum = splash_interval.copy(), 1, 0
    for i in range(len(splash_interval)):
        if splash_interval[i] < 0.2:    # Add short splashes to better emulate
            splash_interval_adjust.insert((i + step), 0.1)
            step += 1
    bar_sum = sum(splash_interval_adjust)
    load_icon(wn, "Resources/loading_box.gif", (0, -94.4))
    # Create a loading bar which syncs the series of splash
    for i in range(len(splash_interval_adjust)): 
        wn.colormode(255)
        splash = turtle.Turtle()
        wn.tracer(False)
        loading_bar = turtle.Turtle()
        loading_bar.pencolor(51, 153, 254)
        loading_bar.width(40)
        loading_bar.hideturtle()
        loading_bar.penup()
        loading_bar.goto(-238, -110)
        loading_bar.pendown()
        loading_bar.forward(bar_accum/ bar_sum * 476)
        wn.tracer(True)
        splash.hideturtle()
        time.sleep(splash_interval_adjust[i])
        bar_accum += splash_interval_adjust[i]   
    wn.clearscreen()
    wn.update()

def loading_windows(wn):
    '''
    Function -- loading_windows
    Setup screen layout and get past players' records
    Parameters: wn -- current canvas
    Return past players' records as a list and report if error occurs
    '''
    wn.bgpic("Resources/emerald.gif")
    load_window("puzzle_window", (-338, 339), 436, 505)
    load_window("button_window", (-338, -237), 678, 102)
    load_window("leaders_window", (117, 339), 222, 505, color = "blue")
    print_leaders("leaders_title", "Leaders:", (128, 298))
    leaders_list = []
    leaderboard_error = 0
    try:
        leaders_list = load_leaders("leaders.txt")
        #   Display a maximum of 14 past players' records in ascending order
        #   Each unique player displays his/her best record
        for i in range(len(leaders_list[:14])):
            name, record = leaders_list[i]
            temp_str = "list_" + str(i)
            print_leaders(temp_str, f"{record}: {name}", (128, 248 - 30 * i))
    except OSError:
        leaderboard_error = 1
    load_icon(wn, "Resources/quitbutton.gif", (286, -288))
    load_icon(wn, "Resources/resetbutton.gif", (98, -288))
    load_icon(wn, "Resources/loadbutton.gif", (193, -288))
    load_icon(wn, "Resources/restartbutton.gif", (8, -288))
    return leaders_list, leaderboard_error

def loading_tiles(name, wn, length, side_length, interval, num, diffic):
    '''
    Function -- loading_tiles
    Loading puzzle tiles with adjustable difficulty levels in a solvable way,
    and return current tiles' mapping info for future tracking purpose
    Parameters: name -- current puzzle name
                wn -- current canvas
                length -- preset frame length for screen layout
                side_length -- unique tile side length
                interval -- preset interval between two frames
                num -- unique puzzle tiles number
                diffic -- adjustable game difficulty
    Return frames location, "tiles and frames mapping" info as dictionaries
    for future reference and tracking
    '''
    # Generate puzzle tiles location (frames location)
    location_dict = generate_loc(length, interval, num)
    # Loading tiles in a solvable way with adjustable difficulty level
    temp_tuple = load_puzzle_tiles(name, wn, location_dict, length,
                                   interval, side_length, num, diffic)
    # Return 
    loc_tile_dict, tile_loc_dict = temp_tuple[:2]
    tile_mem_address_dict, frame_dict = temp_tuple[2:]
    load_icon(wn, pl.thumbnail, (276, 330)) # Loading thumbnail picture
    # Return frames location, "tiles and frames" mapping info as dictionaries
    return (location_dict, loc_tile_dict, tile_loc_dict,
            tile_mem_address_dict, frame_dict)

def get_click(x, y):
    '''
    Function -- get_click
    Setup a click function to pass into the screen.onclick() event function
    Parameters: x -- current click's x coordinate
                y -- current click's y coordinate
    Performs a bunch of functions depending on mouse click position
    '''
    # Click to move tiles when click inside the puzzle window
    if (-323 <= x <= 82) and (-115.5 <= y <= 289.5):
        # Locate the click to the nearest tile
        nearest_loc = get_loc_name(pl.location_dict, x, y)
        # Move tile if it is next to the blank tile
        if is_near_blank(nearest_loc, pl.location_dict, pl.tile_loc_dict,
                         pl.length, pl.interval):
            pl.count += 1
            wn.tracer(False)
            pl.turtle.reset()
            move_counter(pl.turtle, pl.count)
            wn.tracer(True)
            # Switch the tile clicked with the blank tile
            temp_tuple = switch_blank(nearest_loc, pl.location_dict,
                                      pl.loc_tile_dict,
                                      pl.tile_loc_dict,
                                      pl.tile_mem_address_dict)
            pl.loc_tile_dict, pl.tile_loc_dict = temp_tuple
            # Lose if the player used up his/her chances
            if ((pl.loc_tile_dict, pl.tile_loc_dict) != reset_dics(pl.num)
                and pl.count >= pl.chances):
                load__message(wn, "Resources/Lose.gif")
            # Win if the player solved the puzzle with his chances
            if ((pl.loc_tile_dict, pl.tile_loc_dict) == reset_dics(pl.num)
                and pl.count <= pl.chances):
                load__message(wn, "Resources/winner.gif")
                load__message(wn, "Resources/credits.gif")
                # Add the player's name and his record to leaders list
                pl.leaders_list.append((pl.player, pl.count))
                write_leaders(pl.leaders_list, DEFAULT_LEADERBOARD)
                write_err(pl.err, DEFAULT_ERRORLOG)
                wn.bye()
    # Reset tiles if clicked the Reset Button
    if (x - 98) ** 2 + (y + 288) ** 2 <= 1600:
        reset_tiles(pl.name, wn, pl.location_dict, pl.loc_tile_dict,
                    pl.tile_loc_dict, pl.tile_mem_address_dict, pl.num)     
        pl.diffic = 0   # Reset difficulty level to zero
        pl.turtle.reset()   # Reset count
        pl.turtle.hideturtle()
        pl.count = 0
    # Ask the player to load another puzzle when clicked the Reload Button
    if (153 <= x <= 233) and (-328 <= y <= -248):
        t_str = wn.textinput("Load Puzzle","Enter the name of the "\
                             "puzzle you wish to load. Choices are:"\
                             "\nluigi.puz\nsmiley.puz\nfamily.puz"\
                             "\nfifteen.puz\nyoshi.puz\nmario.puz\n"\
                             "malformed_mario.puz")
        temp_pl = GamePanel()
        temp_pl.turtle.hideturtle()
        pl.puz = t_str.lower()
        if pl.puz not in pl.puz_list: # Show warning if error occors
            load__message(wn, "Resources/file_error.gif")
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            pl.err.append((now, f"File {pl.puz} does not exist."))
        else:
            temp_pl.load_tiles(pl.puz)
            if temp_pl.num not in temp_pl.puz_num:
                load__message(wn, "Resources/file_error.gif")
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                pl.err.append((now, f"File {temp_pl.name} is malformed."))
            else:
                for i in range(pl.num):
                    pl.count = 0
                    pl.turtle.reset()
                    pl.turtle.hideturtle()
                    # Make tiles and frames disappear one by one
                    tile_key = pl.loc_tile_dict["loc_" + str(pl.num - i)]
                    frame_key = "frame_" + str(pl.num - i)
                    pl.frame_dict[frame_key].clear()
                    pl.frame_dict[frame_key].hideturtle()
                    pl.tile_mem_address_dict[tile_key].shape("classic")
                    pl.tile_mem_address_dict[tile_key].hideturtle()
                wn.clear()
                wn.tracer(False)
                loading_windows(wn)
                wn.onclick(get_click)
                wn.tracer(True)
                pl.load_tiles(pl.puz)
                pl.diffic = 50
                tp_tuple = loading_tiles(pl.name, wn, pl.length, (pl.size + 1),
                                         pl.interval, pl.num, pl.diffic)
                (pl.location_dict, pl.loc_tile_dict) = tp_tuple[:2]
                (pl.tile_loc_dict, pl.tile_mem_address_dict) = tp_tuple[2:4]
                pl.frame_dict = tp_tuple[4]
    # Restart and Reset Difficulty Level when click the Restart Button
    if (x - 8) ** 2 + (y + 288) ** 2 <= 1600:
        num_input = wn.numinput("Restart& Set Difficulty", "Current hard"\
                                f" level is {pl.diffic}. Please enter an "\
                                "int to set diffic and restart (1-200)",
                                pl.diffic, minval = 1, maxval = 200)
        while not num_input:
            load__message(wn, "Resources/num_warning.gif")
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            pl.err.append((now, f"{num_input} not a valid difficulty level."))
            num_input = wn.numinput("Restart& Set Difficulty", "Current hard"\
                                    f" level is {pl.diffic}. Please enter an "\
                                    "int to set diffic and restart (1-200)",
                                    pl.diffic, minval = 1, maxval = 200)            
        wn.clear()
        wn.tracer(False)
        loading_windows(wn)
        wn.onclick(get_click)
        wn.tracer(True)
        pl.count = 0
        pl.diffic = int(num_input)
        if pl.chances < pl.diffic:  # Adjust chances when too difficult
            pl.chances = pl.diffic
        # Reload tiles with Difficulty Level Reset
        temp_tuple = loading_tiles(pl.name, wn, pl.length, (pl.size + 1),
                                   pl.interval, pl.num, pl.diffic)
        (pl.location_dict, pl.loc_tile_dict) = temp_tuple[:2]
        (pl.tile_loc_dict, pl.tile_mem_address_dict) = temp_tuple[2:4]
        pl.frame_dict = temp_tuple[4]              
    # Exit the puzzle game if click the Quit Button
    if (246 <= x <= 326) and (-328 <= y <= -248):
        load__message(wn, "Resources/quitmsg.gif")
        write_err(pl.err, DEFAULT_ERRORLOG)
        wn.bye()

def main():
    pl.load_tiles(DEFAULT_PUZ) # Load default puzzle-mario at startup
    pl.player, pl.chances = screen_setup(wn)
    loading_splash(wn)
    (pl.leaders_list, pl.leaderboard_error) = loading_windows(wn)

    if pl.leaderboard_error: # Show warning when leaderboard is lost
        load__message(wn, "Resources/leaderboard_error.gif")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pl.err.append((now, "Could not open leaderboard.txt."))
        
    temp_tuple = loading_tiles(pl.name, wn, pl.length, (pl.size + 1),
                               pl.interval, pl.num, pl.diffic)
    pl.location_dict, pl.loc_tile_dict = temp_tuple[:2]
    pl.tile_loc_dict, pl.tile_mem_address_dict = temp_tuple[2:4]
    pl.frame_dict = temp_tuple[4]
    wn.onclick(get_click)
    turtle.done()

   
if __name__ == "__main__":
    main()
