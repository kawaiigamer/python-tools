import random,statistics

winrate = 0.51
iterations = 100

games = [0]*iterations
passwinstreak = 5*5 # below Rank 5
for x in range(iterations):
    
    #                 1-10    11-15 => 15 rank
    ladderPosition =  5*10  +  4*5
    winstrek = 0
    
    while True:
        games[x] = games[x] + 1
        if random.random() <= winrate:
            winstreak = winstrek + 1
            ladderPosition = ladderPosition - 1
            if winstrek >= 2 and ladderPosition > passwinstreak:
                ladderPosition = ladderPosition - 1
        else:
            winstreak = 0
            ladderPosition = ladderPosition + 1
        if ladderPosition is 0:
            break
    


print("Total games (mean of " + str(iterations) + " iterations): "+ str(statistics.mean(games)))
input()
