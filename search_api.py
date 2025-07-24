# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 13:58:46 2025

@author: Kush Swarnkar
"""

from flask import Flask, request, jsonify # Flask framework for APIs.
from elasticsearch_indexer import ElasticsearchIndexer
from config import ELASTICSEARCH_INDEX_NAME

app = Flask(__name__)
indexer = ElasticsearchIndexer()

@app.route('/search', methods=['GET'])
def search_documents():
    query_term = request.args.get('q') # Get search term from URL query parameter.
    if not query_term:
        return jsonify({"error": "Search term 'q' is required"}), 400

    hits = indexer.search_documents(query_term)
    results = []
    for hit in hits:
        results.append({
            'file_name': hit['_source']['file_name'],
            'file_url': hit['_source']['file_url']
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)