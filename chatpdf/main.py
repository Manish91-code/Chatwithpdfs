import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import faiss
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplate import css, user_template, bot_template
from langchain.llms import HuggingFaceHub


# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain

# from langchain.llms import HuggingFaceHub

#get textx from pdf
def getpdftext(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        #Read each page
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

#Get text chunks from Rawtext using langChain
def getTextChunks(raw_text):
    text_splitter= CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


# def getVectorStore(text_chunks):
#     #embeddings = OpenAIEmbeddings()
#     embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     vectorStore= faiss.FAISS.from_texts(texts=text_chunks,embedding=embeddings)
#     return vectorStore

def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = faiss.FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def getConversationChain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


# def handleUserInput(user_question):
#     response=st.session_state.conversation({'question':user_question})
#     st.write(response)
#     st.session_state.chat_history=response['chat_history']

#     for i, message in enumerate(st.session_state.chat_history):
#         if i% 2== 0:
#             st.write(user_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
#         else:
#             st.write(bot_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)


def handleUserInput(user_question):
    response=st.session_state.conversation({'question':user_question})
    #st.write(response)
    st.session_state.chat_history=response['chat_history']

    for index, message in enumerate(st.session_state.chat_history):
        if index% 2== 0:
            st.write(user_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)        


def main():
  
    #load environment varialbles
    load_dotenv();

    #Step1
    st.set_page_config(page_title="CHat with multiple pdf",page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation=None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=None
    
    st.header("chat with multiple pdfs :books:")
    
    #Handle chat functionlity
    user_question=st.text_input("Ask a quesrion about your document")
    if user_question:
        handleUserInput(user_question)

   

    st.write(user_template.replace("{{MSG}}","Hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}","Hello Human"), unsafe_allow_html=True)  
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs=st.file_uploader("Upload your pdfs here and click on 'Process'", accept_multiple_files=True)
   
        #handle button click and processing
        if st.button("Process"):
                with st.spinner("Processing"):
                    #get the pdf text
                    raw_text = getpdftext(pdf_docs)

                     #get gets chunks
                    text_chunks=getTextChunks(raw_text)

                     #create vector embedding and store 
                    vectorstore=get_vectorstore(text_chunks)

                    st.session_state.conversation = getConversationChain(vectorstore)

if __name__ == '__main__':
    main()