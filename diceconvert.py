

def diceconvert(num):
    num = 2*num
    close_list = [num%5, num%7, num%9, num%11, num%13, num%21]
    min_remainder = 10
    dice_size = 2
    for i, remainder in enumerate(close_list):
        if min_remainder >= remainder: 
            min_remainder = remainder
            dice_size = i*2+2
    dice_num = num//(dice_size/2+0.5)
    return (dice_num, dice_size)