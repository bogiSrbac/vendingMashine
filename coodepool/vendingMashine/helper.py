
def set_coins(deposit_value, listOfCoins, dict_amount):
    listOfCoins.sort()
    listOfCoins.reverse()
    for d in range(len(listOfCoins)):
        dict_amount[listOfCoins[d]] = 0

    for i in range(len(listOfCoins)):
        coins = deposit_value / listOfCoins[i]
        deposit_value = deposit_value % listOfCoins[i]
        dict_amount[str(listOfCoins[i])] = int(coins)
    return dict_amount

