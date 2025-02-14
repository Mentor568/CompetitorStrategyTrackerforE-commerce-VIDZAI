#sample program of fibonanci sequence using recursion
def fibonanci(n):
    if n==0:
        return 0
    if n==1:
        return 1
    else:
        return fibonanci(n-1)+fibonanci(n-2)
for i in range(10):
    print(fibonanci(i))
