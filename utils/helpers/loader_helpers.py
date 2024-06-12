import datetime
from utils.s3_client import upload_file_to_s3
from services.mongo import add_file_to_queue
def save_content_to_file(url, content):
    try:
        timestamp = datetime.datetime.now().isoformat().replace(':', '_')
        output_file = f"{url.split('://')[1].split('.com')[0].replace('.', '_')}_{timestamp}.txt"
        content_str = "\n".join(content)
        upload_file_to_s3(content_str, output_file)
        add_file_to_queue(output_file)
    except Exception as e:
        return {"message": "File creation failed!"}

def create_document(url, content):
    from langchain.docstore.document import Document
    try:
        joined_content = " ".join(content)
        content_doc = Document(page_content=joined_content, metadata={"source": url})
        return content_doc
    except Exception as e:
        return {"message": "Document creation failed!"}
    
def split_document(document, chunk_size=1000, overlap_size=100):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    try:
        spliter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size)
        #adding comment for future reference : Earlier document was passed in [] because we were getting plain string from scraper
        split_doc = spliter.split_documents(document)
        return split_doc
    except Exception as e:
        return {"message": f"Document splitting failed!{e}"}