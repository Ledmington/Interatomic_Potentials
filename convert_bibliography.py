import bibtexparser


def surname_for_citation(surname):
    """
    Convert surnames into citation-key format.

    Examples:
        Smith -> Smith
        de Miguel -> DeMiguel
        van der Waals -> VanDerWaals
        De Luca -> DeLuca
    """
    parts = surname.strip().split()
    return "".join(part.capitalize() for part in parts)


def get_first_author_surname(author_field):
    """
    Extract first author's surname from BibTeX author field.
    Examples:
    'Smith, John and Doe, Jane' -> 'Smith'
    'John Smith and Jane Doe' -> 'Smith'
    """
    first_author = author_field.split(" and ")[0]

    if "," in first_author:
        surname = first_author.split(",")[0]
    else:
        surname = first_author.split()[-1]

    return surname.strip()


def format_authors(author_field):
    """
    Convert BibTeX author format:
    'Smith, John and Doe, Jane'
    into:
    'John Smith, Jane Doe'
    """
    authors = author_field.split(" and ")

    formatted = []

    for author in authors:
        if "," in author:
            last, first = author.split(",", 1)
            formatted.append(f"{first.strip()} {last.strip()}")
        else:
            formatted.append(author.strip())

    return ", ".join(formatted)


def format_reference(entry):
    authors = format_authors(entry.get("author", "Unknown author"))

    title = entry.get("title", "Untitled")

    journal = (
        entry.get("journal") or entry.get("booktitle") or entry.get("publisher") or ""
    )

    year = entry.get("year", "")

    doi = entry.get("doi", "")

    # Citation key: Surname + Year
    first_author = get_first_author_surname(entry.get("author", "Unknown"))
    citation_key = f"{surname_for_citation(first_author)}{year}"

    ref = f'**{citation_key}**. {authors}. "{title}"'

    if journal:
        ref += f". *{journal}*"

    if year:
        ref += f", {year}"

    ref += "."

    if doi:
        ref += f" DOI: [{doi}](https://doi.org/{doi})"

    return ref


def generate_bibliography(input_bib):
    with open(input_bib, encoding="utf-8") as f:
        bib = bibtexparser.load(f)

    # Sort entries alphabetically by first author's surname
    bib.entries.sort(
        key=lambda entry: get_first_author_surname(
            entry.get("author", "Unknown")
        ).lower()
    )

    references = []

    for entry in bib.entries:
        references.append(format_reference(entry))

    bibliography = "\n\n".join(references)

    print(bibliography)


if __name__ == "__main__":
    generate_bibliography("main.bib")
