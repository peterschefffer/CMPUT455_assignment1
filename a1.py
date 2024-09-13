# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import random
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
            for point in self.board:
                print("".join([str(x) for x in point]))
        return True
    
    def play(self, args):
        #raise NotImplementedError("This command is not yet implemented.")
        
        legal = self.legal(args, silent=True)

        # # check if legal
        # if not legal:
        #     return False

        formatted_arg = ' '.join([arg if arg.isdigit() else f"{arg}" for arg in args])

        # check for correct number of arguments
        if legal == -3:
            print(f"= illegal move: {formatted_arg} wrong number of arguments")
            return False

        # check that play position is in bounds
        if legal == -4:
            print(f"= illegal move: {formatted_arg} wrong coordinate")
            return False
        
        # if x_pos < 0 or x_pos > self.x_dim - 1 or y_pos < 0 or y_pos > self.y_dim - 1:
        #     print(f"= illegal move: {formatted_arg} wrong coordinate")
        #     return False
        
        # check that digit is in {0,1}
        if legal == -5:
            print(f"= illegal move: {formatted_arg} wrong number")
            return False
        
        #check that board space is not occupied
        # current_board_space = self.board[y_pos][x_pos]
        if legal == -6:
            print(f"= illegal move: {formatted_arg} occupied")
            return False
            
        x_pos = int(args[0])
        y_pos = int(args[1])
        digit = int(args[2])

        if legal == 1:
            self.board[y_pos][x_pos] = digit
            self.change_player()
        elif legal == -1:
            print(f"= illegal move: {x_pos} {y_pos} {digit} three in a row")
            return False
        elif legal == -2:
            print(f"= illegal move: {x_pos} {y_pos} {digit} too many {digit}")
            return False
                
        return True
    
    '''
    Return -1 for a violation of 3 in a row
    Return -2 for a balance violationc  
    Return 1 for legal move
    Return -3 for wrong number of arguments
    Return -4 for wrong coordinate
    Return -5 for wrong number
    Return -6 for occupied

    TODO implement 3 in a row check
    '''
    def legal(self, args, silent = False):

        # formatted_arg = ' '.join([arg if arg.isdigit() else f"{arg}" for arg in args])

        # check for correct number of arguments
        if len(args) != 3:
            # print(f"= illegal move: {formatted_arg} wrong number of arguments")
            if not silent:
                print("no")
            return -3

        # check that play position is in bounds
        if any(not arg.isdigit() for arg in args[:2]):
            if not silent:
                print("no")
            # print(f"= illegal move: {formatted_arg} wrong coordinate")
            return -4
        
        x_pos = int(args[0])
        y_pos = int(args[1])
        
        if x_pos < 0 or x_pos > self.x_dim - 1 or y_pos < 0 or y_pos > self.y_dim - 1:
            # print(f"= illegal move: {formatted_arg} wrong coordinate")
            if not silent:
                print("no")
            return -4
        
        if not args[2].isdigit():
            if not silent:
                print("no")
            return -5
        
        digit = int(args[2])

        # check that digit is in {0,1}
        if not digit in [0,1]:
            # print(f"= illegal move: {formatted_arg} wrong number")
            if not silent:
                print("no")
            return -5
        
        #check that board space is not occupied
        current_board_space = self.board[y_pos][x_pos]
        if current_board_space != ".":
            # print(f"= illegal move: {formatted_arg} occupied")
            if not silent:
                print("no")
            return -6
        
        # 3 in a row X direction violation
        if self.x_dim >= 3:
            if x_pos >= 2:
                if self.board[y_pos][x_pos - 1] == digit and self.board[y_pos][x_pos - 2] == digit:
                    if not silent:
                        print("no")
                    return -1
            if x_pos <= self.x_dim - 3:
                if self.board[y_pos][x_pos + 1] == digit and self.board[y_pos][x_pos + 2] == digit:
                    if not silent:
                        print("no")
                    return -1
            if x_pos >= 1 and x_pos < self.x_dim - 1:
                if self.board[y_pos][x_pos - 1] == digit and self.board[y_pos][x_pos + 1] == digit:
                    if not silent:
                        print("no")
                    return -1
            # if x_pos <= self.x_dim - 2:
            #     if self.board[y_pos][x_pos - 1] == digit and self.board[y_pos][x_pos + 1] == digit:
            #         return -1
        
        # 3 in a row y direction violation
        if self.y_dim >= 3:
            if y_pos >= 2:
                if self.board[y_pos - 1][x_pos] == digit and self.board[y_pos - 2][x_pos] == digit:
                    if not silent:
                        print("no")
                    return -1
            if y_pos <= self.y_dim - 3:
                if self.board[y_pos + 1][x_pos] == digit and self.board[y_pos + 2][x_pos] == digit:
                    if not silent:
                        print("no")
                    return -1
            if y_pos >= 1 and y_pos < self.y_dim - 1:
                if self.board[y_pos - 1][x_pos] == digit and self.board[y_pos + 1][x_pos] == digit:
                    if not silent:
                        print("no")
                    return -1
            # if y_pos <= self.y_dim - 2:
            #     if self.board[y_pos - 1][x_pos] == digit and self.board[y_pos + 1][x_pos] == digit:
            #         return -1

        x_max = int(self.x_dim / 2) + (self.x_dim % 2)
        y_max = int(self.y_dim / 2) + (self.y_dim % 2)

        x_count = 0
        y_count = 0

        # check x balance of digit
        for i in self.board[y_pos]:
            if i == digit:
                x_count += 1       

        if x_count == x_max:
            if not silent:
                print("no")
            return -2
        
        for i in range(self.y_dim):
            if self.board[i][x_pos] == digit:
                y_count += 1

        if y_count == y_max:
            if not silent:
                print("no")
            return -2
        
        if not silent:
            print("yes")
        return 1
    
    def genmove(self, args):
        #raise NotImplementedError("This command is not yet implemented.")


        
        #text needs to be added
        legal_moves = self.check_moves()
        # status  =  self.check_moves()

        if not legal_moves:
            print('resign')
            return True

        rand_move = random.choice(legal_moves)
        x_pos = rand_move[0]
        y_pos = rand_move[1]
        digit = rand_move[2]

        self.board[y_pos][x_pos] = digit
        self.change_player()
        print(x_pos,y_pos,digit)
        # args = []

        # x_pos = random.randint(0,self.x_dim-1)
        # args.append(str(x_pos))
        # y_pos = random.randint(0, self.y_dim-1)
        # args.append(str(y_pos))
        # digit = random.randint(0,1)
        # args.append(str(digit))


        # syntax options when testing
    

        # print(x_pos,y_pos,digit)
        #print(f"@{x_pos} {y_pos} {digit}")
        
        
        # legal = self.legal(args, silent=True)

        # # check if legal
        # if not legal:
        #     return False
            
        # if legal == 1:
        #     self.board[y_pos][x_pos] = digit
        #     self.change_player()

        # elif legal == -1:
        #     print(f"= illegal move: {x_pos} {y_pos} {digit} three in a row")
        #     return False
        # elif legal == -2:
        #     print(f"= illegal move: {x_pos} {y_pos} {digit} too many {digit}")
        #     return False
         
        return True


#create helper function for resign in genmove

    def check_moves(self):
        
        legal_moves = []

        for y in range(self.y_dim):
             for x in range(self.x_dim):
                pos =  self.board[y][x]
                if pos == "." :
                    check0 = [str(x),str(y),"0"]
                    if self.legal(check0, silent=True) == 1:
                        legal_moves.append([x, y, 0])

                    check1 = [str(x),str(y),"1"]
                    if self.legal(check1, silent=True) == 1:
                        legal_moves.append([x, y, 1])
                # if pos == "." :
                #     args.clear()
                #     args.append(str(x))
                #     args.append(str(y)) 
                #     args.append("0")
                #     legal = self.legal(args)
                #     if legal == 1 :
                #         return False
                #     args.pop()
                #     args.append("1")
                #     legal = self.legal(args)
                #     if legal == 1 : 
                #         return False


        return legal_moves
        # return True


    
    def winner(self, args):
        
      
        args = []
     
        for y in range(self.y_dim-1):
             for x in range(self.x_dim-1):
                pos =  self.board[y][x]
                if pos == "." :
                    args.clear()
                    args.append(str(x))
                    args.append(str(y)) 
                    args.append("0")
                    legal = self.legal(args)
                    if legal == 1 :
                        print('\nunfinished')
                        return True
                        
                    args.pop()
                    args.append("1")
                    legal = self.legal(args)
                    if legal == 1 : 
                        print('\nunfinished')
                        return True
        

        self.change_player()
        print(self.current_player)

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
