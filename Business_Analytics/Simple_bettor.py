import random
import matplotlib
import matplotlib.pyplot as plt

'''
Define a function, which will randomly generate an integer from the (1,100)
range. If that number is from the range [51,99] then you win, else you loose.
Comparing to the Roulette game, <51 can be considered as the black patterns,
[51,99] as the red, and 100 as the green one.
'''

def rollDice():
    roll = random.randint(1,100)
    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll > 50:
        return True

'''
Now let's use the function above to create a "Simple bettor". The latter always
bets the same amount of money (bet_amount) for several periods (periods).
'''

def simple_bettor(budget,bet_amount,periods):
    value = budget
    bet = bet_amount

    # let's create values for the axis of the plot
    # which are empty lists now, and will receive values while loop
    # X axis value is the number of periods
    X_axis = []
    # Y axis value is the budget
    Y_axis = []

    currentPeriod = 1

    # change this to, less or equal.
    while currentPeriod <= periods:
        if rollDice():
            value += bet
        else:
            value -= bet
        # append values to the axis lists
        X_axis.append(currentPeriod)
        Y_axis.append(value)
        currentPeriod += 1

    #print budget on different periods
    plt.plot(X_axis,Y_axis)

# now, apply the same strategy for several independent times,
# to get the monte carlo simulation plot
x = 0
trials = input("Please, input the number of periods ")
while x < 100:
    simple_bettor(10000,100,trials)
    x += 1

# add labels to the plot and show it
plt.ylabel('Budget')
plt.xlabel('Periods')
plt.show()
