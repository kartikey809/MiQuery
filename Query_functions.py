import openai

API = {"key":"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"}

import os
os.environ["OPENAI_API_KEY"] = API['key']

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name='gpt-3.5-turbo', max_tokens=2000)
embeddings = OpenAIEmbeddings()

# db = FAISS.from_texts(['sample'], embeddings)
# with open("Faiss_Schema.txt", "wb") as binary_file:
#     binary_file.write(db.serialize_to_bytes())

# with open("Faiss_Code.txt", "wb") as binary_file:
#     binary_file.write(db.serialize_to_bytes())

def add_to_vectorstore(text,load_type):
  if load_type=='Schema':
    with open("Faiss_Schema.txt", "rb") as binary_file:
        model = FAISS.deserialize_from_bytes(binary_file.read(),embeddings)
    model.add_texts([text])
    with open("Faiss_Schema.txt", "wb") as binary_file:
        binary_file.write(model.serialize_to_bytes())

  if load_type=='Code':
    with open("Faiss_Code.txt", "rb") as binary_file:
        model = FAISS.deserialize_from_bytes(binary_file.read(),embeddings)
    model.add_texts([text])
    with open("Faiss_Code.txt", "wb") as binary_file:
        binary_file.write(model.serialize_to_bytes())

def vectorstore_init(load_type):
  if load_type=='Schema':
    with open("Faiss_Schema.txt", "rb") as binary_file:
        model = FAISS.deserialize_from_bytes(binary_file.read(),embeddings)
  if load_type=='Code':
    with open("Faiss_Code.txt", "rb") as binary_file:
        model = FAISS.deserialize_from_bytes(binary_file.read(),embeddings)
  return model

def vectorstore(num_docs,load_type):
  FAISS_Loader = vectorstore_init(load_type)
  print(FAISS_Loader.similarity_search('sample',10))
  docsearch = FAISS_Loader.as_retriever(search_type="similarity", search_kwargs={"k":num_docs})
  return docsearch

def prompt_manager(prompt_type):
  # With RetrievalQA, LangChain auto populates the {context} and {question} fields based on the search documents and question repectively.
  if prompt_type == 'Code':
    prompt_template = """Use the following context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.
  {context}

  You are a code optimizing bot that only accepts python code. You are to do the only the following, do not print any explanations:
  1. If code can be improved in any way return only the improved code. Only return code do not explain.
  2. Else if code already optimal return the text 'optimal' do not print any other text.  
  3. Else return NA if invalid input

  {question}"""

  if prompt_type == 'Explainer':
    prompt_template = """Use the following context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.
  {context}

  You are a code Explainer bot that only accepts python code. Explain the following code concisely in ~200 words.
  {question}"""

  if prompt_type == 'Search':
    prompt_template = """
  You will look at the following text and the following series of options below the Question:
  Text:
  {question}
  
  Options:
  {context}
  
  You will rank the above options based on if it looks similar sorted from most similar to least similar. Put just the sorted titles seperated with commas so I can process it later"""

  if prompt_type == 'Technical':
    prompt_template = """Use the following context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}

    Answer the following as a Technically sound bot in upto a 100 words.
    {question}"""
  return prompt_template

def retriever_bot(query, num_docs, prompt_type, load_type):  
  # Sets up FAISS retriever - requires in the documents(text list) to be converted to vector store and top x of docs to consider.
  retriever = vectorstore(num_docs, load_type)
  # Sets up prompt template for current run - requires pre-defined prompt-type based on front-end input. 
  prompt_template = prompt_manager(prompt_type)

  PROMPT = PromptTemplate(
      template=prompt_template, input_variables=["context","question"]
  )

  chain_type_kwargs = {"prompt": PROMPT}

  # create the chain to answer questions
  rqa = RetrievalQA.from_chain_type(llm=llm, 
                                    chain_type="stuff", 
                                    retriever=retriever, 
                                    return_source_documents=True,
                                    chain_type_kwargs=chain_type_kwargs)
  
  output = rqa(query)
  return output