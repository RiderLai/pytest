from study.class_test.Dog import Dog


class TestDog(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)
