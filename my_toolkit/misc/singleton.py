class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print(f"Object {cls.__name__} init.")
            cls.instance = super(SingletonClass, cls).__new__(cls)
        else:
            print(f"Object {cls.__name__} is already initialized.")
        return cls.instance


class A(SingletonClass):
    def __init__(self):
        print("A.__init__ execution")


class GetInstance:
    instance = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            print(f"Object {cls.__name__} init.")
            cls._instance = super(GetInstance, cls).__new__(cls)
        else:
            print(f"Object {cls.__name__} is already initialized.")

        return cls.instance


class B(GetInstance):
    def __init__(self):
        print("B.__init__ execution")


if __name__ == '__main__':
    # __init__ is called twice
    a1 = A()
    a2 = A()
    print("A()==A() :", a1 is a2)

    # __init__ is called once
    b1 = B()
    b2 = B()
    print("B()==B() :", b1 is b2)

