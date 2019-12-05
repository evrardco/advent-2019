def has_two_adj_streak(number):
    n = str(number)
    c0 = None
    streak = 0
    for c1 in n:
        if c0 == c1:
            streak = streak + 1
        else:
            if streak == 1:
                return True
            streak = 0
            c0 = c1
    return streak == 1
def does_not_decrease(number):
    n = str(number)
    c0 = '0'
    for c1 in n:
        if int(c1) < int(c0):
            return False
        else:
            c0 = c1
    return True
if __name__ == "__main__":
    ls = []
    for i in range(382345, 843167):
        if has_two_adj_streak(i) and does_not_decrease(i):
            ls.append(i)
    print(ls)
    print("count={}".format(len(ls)))