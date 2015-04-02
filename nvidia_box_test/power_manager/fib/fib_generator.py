import time

"""
Calculates fibonacci numbers up to 5 * (10 ^ 5);
only prints out 5 * (10 ^ 5)th number.

@author: Noah Frazier-Logue (n.frazier.logue@nyu.edu)

"""

def fib(to_n):
    num = 1
    a = 1
    b = 0

    while(num < to_n):
        a, b = a+b, a
        num += 1
    print(a)

def main():
    start_time = time.time()
    num = (5 * (10**5))
    fib(num)
    end_time = time.time() - start_time
    print("Time: ", end_time)

main()
