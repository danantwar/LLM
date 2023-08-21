class Dog:
    species="mammal"
    def __init__(self, name, age):
        self.name=name
        self.age=age
    def description(self):
        return "{} is {} years old".format(self.name, self.age)
    def speak(self, sound):
        return "{} says {}".format(self.name, sound)
    def birthday(self):
        self.age+=1
        
tomy=Dog("Tomy",6)
print(tomy.description())
print(tomy.speak("gruff gruff!"))
tomy.birthday()
print(tomy.description())

    
