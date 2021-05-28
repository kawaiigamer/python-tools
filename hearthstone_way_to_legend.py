import random
import statistics

WINRATE = 0.51
ITERATIONS = 100
WINSTREAK_ALLOWED_UNTIL = 5 * 5  # below Rank 5

games = [0] * ITERATIONS
for x in range(ITERATIONS):
    #                  1-10    11-15 => Starting at 15 Rank
    ladder_position = 5 * 10 + 4 * 5
    winstreak = 0
    
    while True:
        games[x] = games[x] + 1
        if random.random() <= WINRATE:
            winstreak += 1
            ladder_position -= 1
            if winstreak >= 2 and ladder_position > WINSTREAK_ALLOWED_UNTIL:
                ladder_position -= 1
        else:
            winstreak = 0
            ladder_position += 1
        if ladder_position == 0:
            break
    
print("Total games (mean of %d iterations): %f" % (ITERATIONS, statistics.mean(games)))
input("Press Enter to continue...")
