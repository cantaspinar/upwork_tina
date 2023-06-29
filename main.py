from bibtex_parser import parse_bibtex
from file_download import download_files_from_parsed_entries
from summerize import summerize_pdf
from qa import ask_question_to_pdf
import csv
from config import pdf_download_path, questions

parsed_entries = parse_bibtex()
selected_entries = download_files_from_parsed_entries(parsed_entries)

with open('data.csv', 'w', encoding='UTF8') as f:

    writer = csv.writer(f)
    header = ['author', 'title', 'year', 'journal', 'summary']

    for question in questions:
        header.append(question)

    writer.writerow(header)
  
    for entry in selected_entries:
        data = []

        author = entry.get('author', 'N/A')
        title = entry.get('title', 'N/A')
        year = entry.get('year', 'N/A')
        journal = entry.get('journal', 'N/A')

        data.append(author)
        data.append(title)
        data.append(year)
        data.append(journal)

        pdf_name = entry.get('file_name')
        pdf_path = f'{pdf_download_path}/{pdf_name}'
        print(f'Generating a summary for "{pdf_name}"...')
        summary = summerize_pdf(pdf_path)
        data.append(summary)

        print(f'Extracting custom information for "{pdf_name}"...')
        for question in questions:
            answer = ask_question_to_pdf(pdf_path, question)
            data.append(answer)

        writer.writerow(data)