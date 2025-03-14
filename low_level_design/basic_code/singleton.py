class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

singleton_obj = Singleton()
another_singleton_obj = Singleton()

print(singleton_obj is another_singleton_obj)