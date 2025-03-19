class Singleton:
    def __new__(cls):
        if(not hasattr(cls, '_instance')):
            cls._instance = super().__new__(cls)
        return cls._instance

o1 = Singleton()
o2 = Singleton()

print(o1 == o2)