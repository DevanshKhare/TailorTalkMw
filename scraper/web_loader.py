from utils.seleniumscraper import scraper
from utils.helpers.loader_helpers import save_content_to_file, create_document, split_document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from dotenv import load_dotenv
import os
load_dotenv()

def load(body):
    url = body.url
    deep_scrap = body.deep_scrap
    try:
        if url:
            response = scraper(url, deep_scrap)
            print("Response............",response)
            if len(response) > 0:
                cleaned_response = [item.replace('\n', ' ') + '\n' for item in response]
                save_content_to_file(url, cleaned_response)
                return {"message": "Data extracted & saved and saved to s3 successfully!", "success": True}
            else:
                return {"message": "Something went wrong!", "success": False}
    except Exception as e:
        return {"message": f"Something went wrong!{e}", "success": False}