import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """ Returns a list of all names of encyclopedia entries. """
    _, filenames = default_storage.listdir("encyclopedia/entries")
    result = sorted(
        re.sub(r"\.md$", "", filename) 
        for filename in filenames 
        if filename.endswith(".md")
    )
    return list(result)


def save_entry(title, content):
    """ Saves an encyclopedia entry, given its title and Markdown content.
        If an existing entry with the same title already exists, it is replaced. """
    filename = f"encyclopedia/entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """ Retrieves an encyclopedia entry by its title.
        If no such entry exists, the function returns None. """
    try:
        f = default_storage.open(f"encyclopedia/entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
