import random

#素数を列挙する
def PrimeNumber():
    primeNumbers = []

    #2から999までの数字を走査する
    for i in range(2, 1000):
        n = 0

        #約数を調べる
        for j in range(1, i+1):
            if i % j == 0:
                n += 1
        
        #約数の個数が2個の場合, リストに格納する(素数)
        if n == 2:
            primeNumbers.append(i)

    return primeNumbers


#素因数分解する
def PrimeFac(num):
    PrimeNumbers = PrimeNumber()
    i = num
    PrimeFac_list = []
    while True:

        #素数で割る
        for prinum in PrimeNumbers:

            #素数で割りきれる場合, iの値を更新する
            if i % prinum == 0:
                i = i / prinum
                PrimeFac_list.append(prinum)
                break
        
        #iの値が1の場合, 終了する
        if i == 1:
            break
    
    PrimeFac_join = "×".join(map(str, PrimeFac_list))
    return PrimeFac_join


for i in range(0, 10):
    num = random.randint(2, 1000)
    print("{}の素因数分解は{}".format(num, PrimeFac(num)))

        
        



