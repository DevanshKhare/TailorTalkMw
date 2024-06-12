from langchain_community.document_loaders import S3FileLoader
import os
from dotenv import load_dotenv
from utils.helpers.loader_helpers import split_document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from neo4j.exceptions import ClientError
from langchain_community.graphs import Neo4jGraph
from services.mongo import get_file_from_queue, remove_file_from_queue
import re
import boto3
from langchain_community.document_loaders.csv_loader import CSVLoader

load_dotenv()

bucket = os.getenv("S3_BUCKET_NAME")
current_dir = os.getcwd()

s3_client = boto3.Session().client("s3")

def extract_string_without_date(filename):
    base_name = os.path.splitext(filename)[0]
    cleaned_name = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\.\d{6}', '', base_name)
    return cleaned_name


def store_to_neo4j():
    print("Storing data to neo4j........")
    files = get_file_from_queue()
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(current_dir, "temp", "tempcsv.csv")
            s3_client.download_file(bucket, file, file_path)
            loader = CSVLoader(file_path)
        else:
            loader = S3FileLoader(bucket=bucket, key=file)
        content_document = loader.load()
        splits = split_document(content_document)
        embeddings = OpenAIEmbeddings()
        graph = Neo4jGraph()
        node_name = extract_string_without_date(file)
        params = {
            "parent_text": node_name,
            "parent_embedding": embeddings.embed_query(node_name),
            "children": [
            {
                 "chunk_text": c.page_content,
                 "chunk_embedding": embeddings.embed_query(c.page_content),
                 "source": c.metadata["source"],
            }
            for ic, c in enumerate(splits)
            ],
        }
        graph.query(
        """
        MERGE (s:SuperParent {content: "Central"})
        MERGE (p:Parent {content: $parent_text})
        MERGE (p)<-[:HAS_CHILD]-(s)
        SET p.embedding = $parent_embedding
        WITH p
        UNWIND $children AS child
        MERGE (c:Chunk {content: child.chunk_text})
        SET c.embedding = child.chunk_embedding
        SET c.source = child.source
        MERGE (c)<-[:HAS_CHILD]-(p)
        WITH c, child
        RETURN count(*)
        """,
        params
        )
        # Create vector index for child
        try:
            graph.query(
            """CREATE INDEX child_document_idx IF NOT EXISTS FOR (c:Child) ON (c.embedding)"""
            )
        except ClientError:  # already exists
            pass
        # Create vector index for parents
        try:
            graph.query(
            """CREATE INDEX parent_document_idx IF NOT EXISTS FOR (p:Parent) ON (p.embedding)"""
            )
        except ClientError:  # already exists
           pass
        remove_file_from_queue(file)
        if(file.endswith(".csv")):
            os.remove(file_path)
            os.remove("/temp/tempcsv.csv")
    return {"message": "Data saved to neo4j successfully!", "success": True}