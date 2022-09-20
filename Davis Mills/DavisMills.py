from DavisMillsHelper import *

user = input("What Game Would You Like? ")

first = None
second = None

if '-' in user:
    first = int(user[0])
    second = int(user[2:])

    getStats(first, second)
else:
    getStats(int(user), int(user))