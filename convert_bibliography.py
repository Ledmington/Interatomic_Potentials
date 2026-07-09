import bibtexparser


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


def format_reference(entry, number):
    authors = format_authors(entry.get("author", "Unknown author"))

    title = entry.get("title", "Untitled")

    journal = (
        entry.get("journal") or entry.get("booktitle") or entry.get("publisher") or ""
    )

    year = entry.get("year", "")

    doi = entry.get("doi", "")

    ref = f'{number}. {authors}. "{title}"'

    if journal:
        ref += f". *{journal}*"

    if year:
        ref += f", {year}"

    ref += "."

    if doi:
        ref += f" DOI: [{doi}](https://doi.org/{doi})"

    return ref


def generate_bibliography(input_bib, output_md):
    with open(input_bib, encoding="utf-8") as f:
        bib = bibtexparser.load(f)

    references = []

    for i, entry in enumerate(bib.entries, start=1):
        references.append(format_reference(entry, i))

    print("\n\n".join(references))


if __name__ == "__main__":
    generate_bibliography("main.bib", "bibliography.md")
