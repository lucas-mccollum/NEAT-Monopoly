import Board

outcome = -1
while outcome == -1:
    
    outcome = Board.turn()

if outcome == 0:
    print("0")

elif outcome == 1:
    print("1")
  
elif outcome == 2:
    print("2")

elif outcome == 3:
    print("3")

elif outcome == 10:
    print("Draw")


