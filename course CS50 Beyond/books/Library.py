""" Librarian is a collection of Library Books. """

from LibraryBook import Book, LBook


class NotABook(Exception): pass

class InvalidName(Exception): pass


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, item):
        try:
            if type(item) is not Book and type(item) is not LBook:
                raise NotABook(f"{item} is not a Book class.")
            elif type(item) is Book:
                item = LBook(0, item.title, item.author, item.text, item.pages)
            self.books[item.title] = item
        except NotABook as err:
            print("TypeError:", err)

    def show_books(self):
        if len(self.books) > 0:
            print("Content of the library are:")
            for bookname in sorted(self.books):
                print(bookname)
        else:
            print("No books in library yet.")

    def check_out(self, bookname):
        try:
            if bookname in self.books:
                return self.books[bookname]
            else:
                raise InvalidName("There is no book with that name in the Library.")
        except InvalidName as err:
            print(err)

    def __repr__(self):
        return "Library()"

    def __str__(self):
        return "Library"

    def __len__(self):
        return len(self.books)


if __name__ == "__main__":
    pass
