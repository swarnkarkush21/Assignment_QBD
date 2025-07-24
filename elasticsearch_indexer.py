# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 13:57:38 2025

@author: Kush Swarnkar
"""

from elasticsearch import Elasticsearch, NotFoundError # Using Elasticsearch.
from config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX_NAME

class ElasticsearchIndexer:
    def __init__(self):
        self.es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT, 'scheme': 'http'}])
        self._create_index_if_not_exists()

    def _create_index_if_not_exists(self):
        # Create an Elasticsearch index with a basic mapping if it doesn't exist.
        if not self.es.indices.exists(index=ELASTICSEARCH_INDEX_NAME):
            self.es.indices.create(index=ELASTICSEARCH_INDEX_NAME)
            print(f"Created Elasticsearch index: {ELASTICSEARCH_INDEX_NAME}")

    def index_document(self, file_id, file_name, file_url, content):
        # Index document with extracted content and metadata.
        doc = {
            'file_id': file_id,
            'file_name': file_name,
            'file_url': file_url,
            'content': content
        }
        self.es.index(index=ELASTICSEARCH_INDEX_NAME, id=file_id, document=doc)
        print(f"Indexed document: {file_name}")

    def search_documents(self, query_term):
        # Perform a full-text search in the Elasticsearch index.
        search_body = {
            "query": {
                "multi_match": {
                    "query": query_term,
                    "fields": ["file_name", "content"] # Search both file name and content fields.
                }
            }
        }
        res = self.es.search(index=ELASTICSEARCH_INDEX_NAME, body=search_body)
        return res['hits']['hits']

    def delete_document(self, file_id):
        # Delete document from Elasticsearch by its ID.
        try:
            self.es.delete(index=ELASTICSEARCH_INDEX_NAME, id=file_id)
            print(f"Deleted document from Elasticsearch: {file_id}")
            return True
        except NotFoundError:
            print(f"Document with ID {file_id} not found in Elasticsearch.")
            return False