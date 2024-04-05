
#JIA YI HE 

class Person:
    def __init__(self, name, age, gender, occupation, nationality):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.nationality = nationality

    def introduce(self):
        print(f"Hello, I'm {self.name}, a {self.age} year old {self.gender}.")
    
    def change_occupation(self, new_occupation):
        self.occupation = new_occupation
        print(f"{self.name}'s occupation is now {self.occupation}.")

person1 = Person("Javier", 16, "Male", "Student", "American")
person2 = Person("Emily", 18, "Female", "Student", "Dominican")

def display_information(person):
    print("\nInformation:")
    person.introduce()

print("Initial Information:")
display_information(person1)
display_information(person2)

person1.age = 24
person1.nationality = "American"

person2.age = 26
person2.nationality = "American"

print("\nAfter Changing Properties:")
display_information(person1)
display_information(person2)

person1.change_occupation("Businessmen")
person2.change_occupation("Doctor")

del person1
del person2
