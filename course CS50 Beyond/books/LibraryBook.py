""" A library book is an object that has all the properties of a Book,
    but also has special features. """
    
from Book import Book


class NoMoreBooks(Exception): pass

class IncorrectName(Exception): pass


class LBook(Book):
    def __init__(self, inventory, title, author=None, text=None, pages=None):
        super().__init__(title, author, text, pages)
        self.borrowers = []

        try:
            inventory = int(inventory)
            self.inventory = inventory if inventory >= 0 else 0
        except ValueError:
            print("ValueError: First argument must be uint.")

    def take(self, line):
        try:
            if self.inventory <= 0:
                raise NoMoreBooks(f"No exemplar of {self.title} left.")
            name = str(line)
            self.borrowers.append(name)
            self.inventory -= 1
        except NoMoreBooks as msg:
            print(msg)
        except ValueError:
            print("Error: name must be string.")

    def put(self, name=None):
        try:
            if name and name not in self.borrowers:
                raise IncorrectName("Name is Unknown.")
            elif name and name in self.borrowers:
                self.borrowers.remove(name)
            else:
                print("Thanks for adding a new book to our library stock!")
            self.inventory += 1
        except IncorrectName as msg:
            print(msg)

    def left(self):
        s = f"{self.inventory} of {self.title} left."
        if len(self.borrowers) > 0:
            s += "\nBorrowers: "
            s += ', '.join(self.borrowers)
        print(s)


if __name__ == "__main__":
    pass
