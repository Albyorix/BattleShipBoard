

I create a class Boat that contains the information about each boat:
- id: to be able to find it it a list
- position_x: x=cte is the N/S axis
- position_y: y=cte is the E/W axis
- direction: N, S, E, W
- is_wreack: True if the boat was sunk

The Boat object has the following methods:
- rotate_left, rotate_right, move_forward: to move the boat following the rules
- sink: to sink the boat
- __repr__: to get the line string for the output file

	
	
I create a class BattleShipBoard that contains the information:
- size: the board size
- raw_boats: the raw string that defines the boats
- raw_actions: the raw string that defines the actions
- grid: a list of list to find a boat from its position
- new_boats: the usable list to create the boats and place them in the grid
- boats: a list of boats to find a boat by its id

The BattleShipBoard object contains the following methods:
- process_input_strings: to transform the raw strings into usable lists
- move: to move the boat in position_x, position_y following the sequence sequence
- shoot: to shoot & sink a boat if needed
- run: to process all the actions from the list of actions
- save_output: to save the output where needed
- compare_outputs: to compare the output created with the one from the Tests folder
- __repr__: to get the whole representation of the board

	