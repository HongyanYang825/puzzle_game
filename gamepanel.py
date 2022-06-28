'''
    CS5001
    Fall 2021
    Final_Project_Self-Defined_Class

    Define and implement a GamePanel class to conduct puzzle operations
    based on the turtle library

    Hongyan Yang
'''


import turtle

class GamePanel:
    
    def __init__(self, length = 99, interval = 3) -> None:
        '''
        Method -- __init__
        Create a new GamePanel instance by supplying length and interval
        for default tile frame's side length and interval between frames
        Parameters: length (int) -- tile frame's side length
                    interval (int) -- interval between two frames
        Create a new GamePanel instance and set a bunch of default attributes
        '''
        self.turtle = turtle.Turtle()
        self.length = 99
        self.interval = 3
        self.player = ""
        self.location_dict = {}
        self.loc_tile_dict = {}
        self.tile_loc_dict = {}
        self.tile_mem_address_dict = {}
        self.count = 0
        self.chances = 50
        self.diffic = 50
        self.leaders_list = []
        self.err = []
        self.leaderboard_error = 0
        self.puz_num = [4, 9, 16]
        self.puz_list = ["luigi.puz", "smiley.puz", "family.puz",
                         "fifteen.puz", "yoshi.puz", "mario.puz",
                         "malformed_mario.puz"]
        self.puz = ""

    def load_tiles(self, puz_file):
        '''
        Method -- load_tiles
        Extract input_puz file's info into a dictionary and pass values to
        GamePanel's specific attributes
        Parameters: self -- input GamePanel instance
                    puz_file (str) -- input puz file contains puz info
        Set values for a bunch of attributes of a GamePanel instance
        '''
        self.puz = puz_file
        # Potential open_file errors are treated in the main function
        with open(puz_file, 'r', encoding='utf-8') as infile:
                dict_out = {} 
                for line in infile:
                    # Extract each line of info and add to the dictionary 
                    temp_list = line.strip().split(": ")
                    dict_out[temp_list[0]] = temp_list[1]
                self.panel_dict = dict_out
                self.name = self.panel_dict['name']
                self.num = int(self.panel_dict['number'])
                self.size = int(self.panel_dict['size'])
                self.thumbnail = self.panel_dict['thumbnail']
