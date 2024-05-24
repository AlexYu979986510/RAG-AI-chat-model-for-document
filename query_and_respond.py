"""
Created on Thu Apr 25 16:54:26 2024

@author: AlexYu
"""
"""
To perform a specific text-based query against a vector database and use the results to generate a response using 
an AI-driven chat model
"""
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os 

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Please be a bank industry system expert and Answer the question based on the above context: {question}
"""

def main():
    # Your OpenAI API key
    api_key = "Your OpenAI API key"  # Replace this with your actual API key

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key=api_key)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    #########################################################################################################
    query_text = "does covered call supports put option? explain in detail" # Your query text here
    #########################################################################################################
    
    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=8) # Control your chunks for inquiry here
    if len(results) == 0 or results[0][1] < 0.7:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Initialize the model and generate response
    model = ChatOpenAI(openai_api_key=api_key)
    response_text = model.predict(prompt)


    # Collect and print sources, preserving order and removing duplicates
    seen = set()
    sources = []
    for doc, _score in results:
        source = os.path.basename(doc.metadata.get("source", ""))
        if source not in seen:
            seen.add(source)
            sources.append(source)

    formatted_response = f"Response: \n{response_text}\n\nSources: {sources}"
    print(formatted_response)

if __name__ == "__main__":
    main()
