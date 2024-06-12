from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQAWithSourcesChain
from dotenv import load_dotenv

load_dotenv()

def get_matching_documents(query):
    try:
        existing_graph = Neo4jVector.from_existing_graph(
            embedding=OpenAIEmbeddings(),
            index_name="document_index",
            node_label="Chunk",
            text_node_properties=["content"],
            embedding_node_property="embedding",
        )

        retriever = existing_graph.as_retriever(kwargs={"top_k": 3})
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            ChatOpenAI(temperature=0), chain_type="stuff", retriever=retriever)
        result = chain.invoke(
            {"question": query},
            return_only_outputs=True,
        )
        return {"answer": result["answer"], "sources": result["sources"], "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}
