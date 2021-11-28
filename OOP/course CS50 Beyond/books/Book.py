""" Thanks to CS50 on Twitch for inspiration. """


class Book:
    def __init__(self, title, author=None, text=None, pages=None):
        self.title = title
        self.author = author
        self.text = text
        self.pages = pages

    def look(self):
        s = f"The book namely {self.title}"
        if self.author is not None:
            s += f" is written by {self.author}"
        if self.pages is not None:
            s += f", number of pages {self.pages}"
        if self.text is not None:
            s += f"\nText:\n{self.text}"
        print(s)

    def __repr__(self):
        return self.title


if __name__ == "__main__":
    pass
