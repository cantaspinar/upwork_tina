from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from config import drive_folder_id, openai_api_key, pdf_download_path


def download_files_from_parsed_entries(parsed_entries):

    from drive import list_files, download_file

    print("Listing Google Drive folder...")

    drive_files = list_files(drive_folder_id)
    file_count = len(drive_files)

    print(f"Found {file_count} files inside the Drive folder.")

    docs = []
    for drive_file in drive_files:
        file_name = drive_file['name']
        file_id = drive_file['id']
        doc = Document(page_content=file_name, metadata={"id": file_id})
        docs.append(doc)

    print("Embedding file names...")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.from_documents(docs, embeddings)

    print("Checking for similarities...")

    selected_entries = []
    for entry in parsed_entries:
        author = entry.get('author', 'N/A')
        title = entry.get('title', 'N/A')
        query = f"{author}_{title}"
        docs_and_scores = db.similarity_search_with_score(query)
        score = docs_and_scores[0][1]
        file_name = docs_and_scores[0][0].page_content
        file_id = docs_and_scores[0][0].metadata['id']
        if(score < 0.25):
            entry['file_id'] = file_id
            entry['file_name'] = file_name
            selected_entries.append(entry)

    selected_entries_count = len(selected_entries)

    print(f"Found {selected_entries_count} files to download.")

    print("Downloading files...")

    for entry in selected_entries:
        file_id = entry['file_id']
        file_name = entry['file_name']
        download_file(file_id, file_name,pdf_download_path)

    return selected_entries