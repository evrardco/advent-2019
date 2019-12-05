def has_two_adj(number):
    n = str(number)
    c0 = None
    for c1 in n:
        if c0 == c1:
            return True
        else:
            c0 = c1
    return False
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
        if has_two_adj(i) and does_not_decrease(i):
            ls.append(i)
    print(ls)
    print("count={}".format(len(ls)))