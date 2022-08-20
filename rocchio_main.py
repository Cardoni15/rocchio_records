#!/usr/bin/env python3.9
from user_interface.user_interface_class import Rocchio_Records_GUI_Object
import warnings
warnings.filterwarnings("ignore")

def main():
    # our function uses two classes to provide the user playlist generation.
    # the Rocchio records GUI class handles all user input
    # Nested in that class is the lyric rocchio filter class. This class executes the filter
    # used for recommending tracks.
    Rocchio_Records_GUI_Object()

if __name__ == '__main__':
    main()