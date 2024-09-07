# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }

        self.board = None
        self.current_player = 1
        self.x_dim = 0
        self.y_dim = 0

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def game(self, args):
        #raise NotImplementedError("This command is not yet implemented.")
        if len(args) > 2:
            print("too many arguments")
            return False
        self.x_dim = int(args[0])
        self.y_dim = int(args[1])
        self.board = [["." for x in range(self.x_dim)] for y in range(self.y_dim)]
        self.current_player = 1
        return True
    
    def show(self, args):
        #raise NotImplementedError("This command is not yet implemented.")
        if self.board:
            for i in self.board:
                for j in i:
                    print(j, end=" ")
                print('\n')
        return True
    
    def play(self, args):
        #raise NotImplementedError("This command is not yet implemented.")

        x_pos = int(args[0])
        y_pos = int(args[1])
        digit = int(args[2])
        
        legal = self.legal(args)
        
        if legal == 1:
            self.board[y_pos][x_pos] = digit
            self.change_player()
        elif legal == -1:
            print(f"= illegal move: {x_pos} {y_pos} {digit} three in a row violation")
            return False
        elif legal == -2:
            print(f"= illegal move: {x_pos} {y_pos} {digit} too many {digit}")
            return False
                
        return True
    
    '''
    Return -1 for a violation of 3 in a row
    Return -2 for a balance violation
    Return 1 for legal move

    TODO implement 3 in a row check
    '''
    def legal(self, args):

        x_pos = int(args[0])
        y_pos = int(args[1])
        digit = int(args[2])

        # check for correct number of arguments
        if len(args) > 3:
            print("= illegal move: ", end=" ")
            for i in args:
                print(i, end=" ")
            print("wrong number of arguments")
            return False

        # check that play position is in bounds
        if x_pos < 0 or x_pos > self.x_dim - 1 or y_pos < 0 or y_pos > self.y_dim - 1:
            print(f"= wrong coordinate: {x_pos}, {y_pos} is out of bounds")
            return False
        
        # check that digit is in {0,1}
        if not digit in [0,1]:
            print(f"= wrong number: {digit} is not a playable value")
            return False
        
        #check that board space is not occupied
        current_board_space = self.board[y_pos][x_pos]
        if current_board_space != ".":
            print(f"= occupied: position {x_pos}, {y_pos} has already been played")
            return False


        x_max = int(self.x_dim / 2) + (self.x_dim % 2)
        y_max = int(self.y_dim / 2) + (self.y_dim % 2)

        x_count = 0
        y_count = 0

        # check x balance of digit
        for i in self.board[y_pos]:
            if i == digit:
                x_count += 1        
        if x_count == x_max:
            return -2
        
        for i in range(self.y_dim):
            if self.board[i][x_pos] == digit:
                y_count += 1

        if y_count == y_max:
            return -2

        return 1
    
    def genmove(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def winner(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def change_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()