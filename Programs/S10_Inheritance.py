class Person:
    description="general person"

    def __init__(self, name, age):
        self.name=name
        self.age=age

    def speak(self):
        print("My name is {} and I am {} years old".format(self.name, self.age))

    def eat(self,food):
        print("{} eats{}".format(self.name, food))

    def action(self):
        print("{} spins".format(self.name))

class Baby(Person):
    description="baby"

    def speak(self):
        print("ma ma")

    def nap(self):
        print("{} takes a nap".format(self.name))

person=Person("John",30)
person.speak()
person.eat("fish")
person.action()

baby=Baby("Vanzel",1)
baby.speak()
baby.eat("Baby food")
baby.action()

print(person.description)
print(baby.description)

print(isinstance(baby, object))
