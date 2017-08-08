#!/usr/bin/python3

def number_to_base(n, base):
    if n==0:
        return [0]
    digits = []
    while n:
        digits.append(int(n%base))
        n = n // base
    return digits[::-1]

def solution(moves, start, end, *functions):
    for i in range(len(functions)**moves):
        code = number_to_base(i, len(functions))
        code = [0]*(moves-len(code)) + code
        endnumber = start
        for fkey in code:
            endnumber = functions[fkey](endnumber)
        if endnumber == end:
            print('{} returned: {}'.format(code, endnumber))
            return code
    print('no solution found')


def addNumber(number):
    def func(start):
        return int(str(start)+str(number), 10)
    return func

def mult(number):
    def func(start):
        return start*number
    return func

def divide(number):
    return mult(1/number)

def add(number):
    return lambda x : x+number

def remove_char(start):
    return start//10

def reverse(start):
    return int(str(start)[::-1], 10)

#solution(5, 0, 245, add(-3), addNumber(5), mult(4), mult(-1))
#solution(4, 39, 12, mult(-3), mult(1/3), add(9), mult(-1))
#solution(6, 111, 126, mult(3), add(-9), mult(-1), remove_char)
#solution(5, 34, 3, add(-5), add(8), mult(1/7), mult(-1))
#solution(5, 25, 4, add(-4), mult(-4), mult(1/3), mult(-1), mult(1/8))
def handledint(string):
    try:
        return int(string)
    except:
        print('{} is not a number. input a number.'.format(string))
        return handledint(input())
def inputFunction():
    print(':', end='')
    code = handledint(input())
    try:
        number = int(code)
    except:
        print('{} is not valid.'.format(code))
        return inputFunction()
    if number == 6:
        return None
    elif number == 0:
        print('what number to add?', end=' ')
        return addNumber(handledint(input()))
    elif number == 1:
        print('x', end=' ')
        return mult(handledint(input()))
    elif number == 2:
        print('+', end=' ')
        return add(handledint(input()))
    elif number == 3:
        print('/', end=' ')
        return divide(handledint(input()))
    elif number == 4:
        return remove_char
    elif number == 5:
        return reverse
    else:
        print('{} is not valid'.format(number))
        return inputFunction()

while True:
    print('moves:', end=' ')
    moves = handledint(input())
    print('start:', end=' ')
    start = handledint(input())
    print('end:', end=' ')
    end = handledint(input())
    print('''   functions:
    0 - add number to end
    1 - multiply
    2 - add
    3 - divide
    4 - <<
    5 - reverse
    6 - no more functions''')
    functions = [inputFunction()]
    while len(functions) > 0 and functions[-1] is not None:
        print('adding new function...')
        functions.append(inputFunction())
    solution(moves, start, end, *functions[:-1])
