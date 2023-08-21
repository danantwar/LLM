class Dog:
    species="mammal"
    def __init__(self, name, age):
        self.name=name
        self.age=age
tomy=Dog("Tomy",5)
lili=Dog("Lili",7)
lili.age=8
tomy.species="mouse"
print("{} is {} and {} is {}".format(tomy.name, tomy.age, lili.name, lili.age))
if tomy.species=="mammal":
    print("{} is a {}".format(tomy.name,tomy.species))
    
