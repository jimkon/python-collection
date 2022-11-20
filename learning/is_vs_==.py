
if __name__ == '__main__':
    d1 = {'a': 1}
    d2 = {'a': 2}
    d3 = {'a': 1}

    l = [d1, d2, d3, d1]

    print("== condition")
    print(f"{[i for i, e in enumerate(l) if e == d1]}")
    print(f"Checking the value")

    print("\n'is' condition")
    print(f"{[i for i, e in enumerate(l) if e is d1]}")
    print(f"Checking the pointer")

