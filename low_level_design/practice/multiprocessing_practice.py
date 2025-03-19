import multiprocessing

def squares(x):
    return x**2

nums = [1, 2, 3, 4, 5]
with multiprocessing.Pool() as pool:
    result = pool.map(squares, nums)
print(result)