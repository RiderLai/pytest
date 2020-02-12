class SingletonMetaclass(type):
    '''
    单例元类
    '''

    instances = {}

    def __call__(cls, *args, **kwargs):
        '''
        调用方法
        '''
        result = None
        instances = cls.__class__.instances

        if cls in instances:
            result = instances[cls]
        else:
            result = instances[cls] = super().__call__(*args, **kwargs)

        return result


class A(metaclass=SingletonMetaclass):

    def __init__(self):
        self.a = 1
        print('init')

    def test(self):
        print(id(self))

    @classmethod
    def create(cls):
        result = cls()
        result.a = 2
        return result


class B(object):

    def __init__(self):
        print('init')

    def __call__(self, *args, **kwargs):
        print('call')


if __name__ == '__main__':
    # a1 = A()
    # a2 = A()

    a1 = A.create()
    print(a1.a)

    a2 = A()
    print(a1.a)

    print(id(a1))
    print(id(a2))