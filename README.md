# Second Brain Assistant

This is a simple LLM assistant that uses can summarise and compile information from a Notion database.

It uses Langchain to load data from a Notion database of notes and webclips into a Chroma vector database. A Streamlit app is then started up and infers/summarises information from the vector database.

This project is *heavily* inspired by [Chanin Nantasenamat's Ask the Doc app](https://blog.streamlit.io/langchain-tutorial-4-build-an-ask-the-doc-app/).

## Quickstart

### Installation
This project uses Poetry for dependency management. To install the dependencies, run:

```bash
poetry install
```

### Environment Variables
You will need a Notion Token and OpenAI API key. These can be set as environment variables through the `.env` file. Look at the `.env.example` file for more information.


You will need to set up a Notion integration to get the integration token. See [here](https://developers.notion.com/docs/getting-started) for more information. Be sure to give the application access to any databases you want it to retrieve data from.

### Load Data
To load data from Notion into the vector database, run:

```bash
poetry run load_notion_database
```

You should see a new folder in this repository called `.chromadb`. This is where the vector database is stored.

### Run Streamlit App
To run the Streamlit app, run:

```bash
streamlit run app.py
```
