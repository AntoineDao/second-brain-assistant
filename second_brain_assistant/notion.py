from notion2md.exporter.block import StringExporter
import os
from notion_client import Client
from pydantic import BaseModel, Field
import typing as t


class NotionList(BaseModel):
    object: str
    results: list
    next_cursor: str = Field(None, alias="next_cursor")
    has_more: bool


class NotionDatabase(BaseModel):
    id: str
    created_time: str
    last_edited_time: str
    parent: dict = {}
    properties: dict
    url: str


class NotionPageProperty(BaseModel):
    id: str
    type: str
    formula: dict = Field(None, alias="formula")
    rich_text: list = Field(None, alias="rich_text")
    relation: list = Field(None, alias="relation")
    multi_select: list = Field(None, alias="multi_select")
    checkbox: bool = Field(None, alias="checkbox")
    url: str = Field(None, alias="url")
    rollup: dict = Field(None, alias="rollup")
    relation: list = Field(None, alias="relation")
    title: list = Field(None, alias="title")

    # def _get_first

    @property
    def value(self):
        if self.type == 'formula':
            formula_type = self.formula['type']
            return self.formula[formula_type]
        elif self.type == 'rich_text':
            return next(iter(self.rich_text), {}).get('plain_text', '')
        # elif self.type == 'relation':
        #     return self.relation[0]['id']
        elif self.type == 'multi_select':
            ', '.join([item['name'] for item in self.multi_select])
        elif self.type == 'checkbox':
            return self.checkbox
        elif self.type == 'url':
            return self.url
        # elif self.type == 'rollup':
        #     pass
        elif self.type == 'title':
            return next(iter(self.title), {}).get('plain_text', '')
        return ''

    def __str__(self):
        return str(self.value)


class NotionPage(BaseModel):
    id: str
    parent: dict
    created_time: str
    last_edited_time: str
    archived: bool
    properties: t.Dict[str, NotionPageProperty]
    url: str

    @property
    def metadata(self):
        metadata = {}
        for key, value in self.properties.items():
            string = str(value)
            if value.type == 'multi_select':
                for v in string.split(','):
                    metadata[v] = True
            else:
                metadata[key] = string

        return metadata


class NotionPageList(NotionList):
    results: list[NotionPage]


class Notion:

    def __init__(self):
        self.notion = Client(auth=os.environ["NOTION_TOKEN"])

    def get_database(self, name: str):
        res = self.notion.search(
            **{
                "query": name,
                "filter": {
                    "value": "database",
                    "property": "object",
                },
                "sort": {
                    "direction": "ascending",
                    "timestamp": "last_edited_time",
                },
            }
        )
        return NotionDatabase.parse_obj(res["results"][0])

    def get_notes(self, database_id: str):
        res = self.notion.databases.query(
            **{
                "database_id": database_id,
            }
        )

        return NotionPageList.parse_obj(res)

    def get_note_contents(self, note_id: str):
        return StringExporter(
            block_id=note_id,
        ).export()
