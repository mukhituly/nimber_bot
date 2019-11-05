import random
import time

class CantMove( Exception ) :

    def __init__( self, reason ) : 
      self. __reason = reason

    def __repr__( self ) :
      return "unable to find a move: {}". format( self.__reason )


class Nim :
    def __init__( self, startstate ) :
      self. state = startstate


   # Goal is to be unambiguous : 

    def __repr__( self ):
        index = 0
        string = ''
        for row in self.state:
            string += (str(index + 1) + ": ") 
            row_iterator = 0
            while row_iterator != row:
                string += "1 "
                row_iterator = row_iterator + 1
            if index != len(self.state) - 1:
                string += '\n'
            index = index + 1
        return string

   # Return sum of all rows:

    def sum( self ) :
        count = 0 #will be equal to zero, when sums 1 from row 1
        for i in self.state: #will be filled after joining
            count += i
        return count

   # Return nimber (xor of all rows): 
   
    def nimber( self ) :
        tot_xor = 0
        for i in self.state:
            tot_xor = tot_xor ^ i
        return tot_xor

   # Make a random move, raise a CantMove if
   # there is nothing left to remove. 

    def randommove( self ) :
        if self.sum() == 0:
            raise CantMove(" no sticks left")
        else:
            randomint = random.randrange(len(self.state))
            while   self.state[randomint] == 0:
                randomint = random.randrange(len(self.state))
            randomint2 = random.randrange(1, self.state[randomint] + 1)
            self.state[randomint] -= randomint2
        return self

   # Try to force a win with misere strategy.
   # This functions make a move, if there is exactly
   # one row that contains more than one stick.
   # In that case, it makes a move that will leave
   # an odd number of rows containing 1 stick.
   # This will eventually force the opponent to take the
   # last stick.
   # If it cannot obtain this state, it should raise
   # CantMove( "more than one row has more than one stick" )

    def removelastmorethantwo( self ) :
        count = 0
        emptyrows = 0
        actualrows = 0
        changesmade = False
        for sticks_in_row in self.state:
            if sticks_in_row > 1:
                count += 1
            elif sticks_in_row == 0:
                emptyrows += 1
        actualrows = len(self.state) - emptyrows
        if count != 1:
            raise CantMove(" more than one row has more than one stick")

        elif count == 1 and actualrows % 2 == 0:
            for stick in range(len(self.state)):
                if self.state[stick] > 1:
                    self.state[stick] = 0 
        else:
            for stick in range(len(self.state)):
                if self.state[stick] > 1:
                    self.state[stick] = 1  
        return self

   # Try to find a move that makes the nimber zero.
   # Raise CantMove( "nimber is already zero" ), if the
   # nimber is zero already.

    def makenimberzero( self ) :
        if self.nimber() == 0:
            raise CantMove(" nimber is already zero")
        else:
            Condition = False
            while Condition != True:
                nim = self.nimber()
                random_row = random.randrange(len(self.state))
                if (self.state[random_row] ^ nim) < self.state[random_row]:
                    self.state[random_row] ^= nim
                    Condition = True
        return self

   
 
    def optimalmove( self ) :
        try:
                self.removelastmorethantwo()
        except:
            try: 
                self.makenimberzero()
            except:
                self.randommove()
                return self

   # Let the user make a move. Make sure that the move
   # is correct. This function never crashes, not
   # even with the dumbest user in the world. 
           
    def usermove( self ) : 
        input_true = False

        while input_true != True:
            try:
                user_input_string = input("Please enter the row: ") 
                user_input = int(user_input_string)
                input_true = True
            except ValueError:
                print("Your input is not integer!")

        input_true = False

        while input_true != True:
            if user_input > len(self.state) or self.state[user_input - 1] == 0 or user_input <= 0 :
                print("Invalid input. Try again:")
                user_input_string = input("Please enter the row: ")
                user_input = int(user_input_string)
            else:
                input_true = True

        input_true = False

        while input_true != True:
            try:
                user_input_string2 = input("How many sticks should remain in the row? ") 
                user_input2 = int(user_input_string2)
                input_true = True
            except ValueError:
                print("Your input is not integer!")

        input_true = False

        while input_true != True:
            if user_input2 >= self.state[user_input - 1] or user_input2 < 0 :
                print("Invalid input. Try again:")
                user_input_string2 = input("How many sticks should remain in the row? ")
                user_input2 = int(user_input_string2)
            else:
                input_true = True

        self.state[user_input - 1] = user_input2
        return self

def play():
    st = Nim( [ 1, 2, 3, 4, 5, 6] )
    turn = 'user'
    while st. sum( ) > 1 :
        if turn == 'user' :
            print( "\n" )
            print( st )
            print( "hello, user, please make a move" )
            st. usermove( )
            turn = 'computer'
        else:
            print( "\n" )
            print( st )
            print( "now i will make a move\n" )
            print( "thinking" )
            for r in range( 15 ) :
                print( ".", end = "", flush = True )
                time. sleep( 0.1 )
            print( "\n" )
            st. optimalmove( )
            turn = 'user'
    print( "\n" )
    if turn == 'user' :
        print( "you lost\n" )
    else :
        print( "you won\n" )