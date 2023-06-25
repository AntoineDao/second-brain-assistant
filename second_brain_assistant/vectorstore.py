import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from .llm import embedding_client
from .notion import Notion

vector_client = Chroma(
    persist_directory=".chromadb/",
    embedding_function=embedding_client
)

NOTION_DATABASE_NAME = os.environ.get("NOTION_DATABASE_NAME", "notes")


def load_notion_database():
    notion = Notion()

    db = notion.get_database(NOTION_DATABASE_NAME)
    note_list = notion.get_notes(db.id)

    for i, note in enumerate(note_list.results):
        print(f'Loading note {i} of {len(note_list.results)}',
              end='\r', flush=True)
        try:
            content = notion.get_note_contents(note.id)
            text_splitter = CharacterTextSplitter(
                chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.create_documents(
                texts=[content],
                metadatas=[note.metadata]
            )
            vector_client.add_documents(docs)
            print(f"Added note to vectorstore: {note.id}")
        except Exception as e:
            print(e)
            print(f"Failed to add note to vectorstore: {note.id}")
