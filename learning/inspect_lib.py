import inspect


def function():
    pass


class AClass:
    def method(self):
        pass


if __name__ == "__main__":
    print(inspect.ismethod(function))
    print(inspect.ismethod(AClass().method))

