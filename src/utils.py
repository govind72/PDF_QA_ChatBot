from PyPDF2 import PdfReader
from typing import List, Dict
import re
from chromadb import Client, Settings
from chromadb.utils import embedding_functions



ef = embedding_functions.ONNXMiniLM_L6_V2()
client = Client(settings = Settings(persist_directory="./", is_persistent=True))
collection_ = client.get_or_create_collection(name="test", embedding_function=ef)



def add_text_to_collection(file: str, word_limit: int = 600) -> str:
    docs = load_pdf(file, word_limit)
    document_strings = []
    metadatas = []
    ids = []
    doc_id = 0
    
    for page_no, chunks in docs.items():
        for chunk in chunks:
            document_strings.append(chunk)
            metadatas.append({'page_no': page_no})
            ids.append(str(doc_id))
            doc_id += 1

    collection_.add(
        ids=ids,
        documents=document_strings,
        metadatas=metadatas,
    )
    
    return "Your Document has been processed successfully. Now You can ask Questions...."

def load_pdf(file: str, word_limit: int) -> Dict[int, List[str]]:
    reader = PdfReader(file)
    document_chunks = {}
    
    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no]
        text = page.extract_text()
        text_chunks = get_text_chunks(text, word_limit)
        document_chunks[page_no] = text_chunks

    return document_chunks




def get_text_chunks(text: str, word_limit: int) -> List[str]:
    """
    Divide a text into chunks with a specified word limit while ensuring each chunk contains complete sentences.
    
    Parameters:
        text (str): The entire text to be divided into chunks.
        word_limit (int): The desired word limit for each chunk.
    
    Returns:
        List[str]: A list containing the chunks of texts with the specified word limit and complete sentences.
    """
    # Improved regex to handle different end-of-sentence punctuations.
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', text)
    chunks = []
    current_chunk = []
    current_chunk_word_count = 0

    for sentence in sentences:
        words = sentence.split()
        sentence_word_count = len(words)
        if current_chunk_word_count + sentence_word_count <= word_limit:
            current_chunk.extend(words)
            current_chunk_word_count += sentence_word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = words
            current_chunk_word_count = sentence_word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks



def query_collection(query_text: str, n: int) -> List[str]:
    try:
        result = collection_.query(
            query_texts=query_text,
            n_results=n,
        )
        
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        resulting_strings = []
        
        for metadata, text_chunk in zip(metadatas, documents):
            resulting_strings.append(f"Page {metadata['page_no']}: {text_chunk}")
        
        return resulting_strings
    
    except KeyError as e:
        print(f"KeyError: {e} - Please check the result structure.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
