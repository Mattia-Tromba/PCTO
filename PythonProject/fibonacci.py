def fibonacci(n):
    a=0
    b=1
    for x in range (n):
        print(a+b)
        a, b= b, a+b
fibonacci(99999999)