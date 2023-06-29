from pybtex.database import parse_file
from config import bibtex_file

def parse_bibtex():
    entries = parse_file(bibtex_file)
    parsed_data = []

    for entry_key in entries.entries:
        entry = entries.entries[entry_key]
        parsed_entry = {}

        # Parse author(s)
        authors = entry.persons.get('author')
        if authors:
            parsed_entry['author'] = ' and '.join(
                str(author) for author in authors)

        # Parse title
        title = entry.fields.get('title')
        if title:
            parsed_entry['title'] = title

        # Parse year
        year = entry.fields.get('year')
        if year:
            parsed_entry['year'] = year

        # Parse journal
        journal = entry.fields.get('journal')
        if journal:
            parsed_entry['journal'] = journal

        parsed_data.append(parsed_entry)

    return parsed_data