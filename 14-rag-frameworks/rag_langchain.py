# rag_langchain.py: version 2, the same RAG app with LangChain (LCEL chain).
#   pip install langchain-core langchain-text-splitters pypdf
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingest import load_pdf
from models import embed, chat
from questions import QUESTIONS, SYSTEM

class OurEmbeddings(Embeddings):     # plug OUR embed() into LangChain
    def embed_documents(self, texts): return embed(texts)
    def embed_query(self, text): return embed([text])[0]

ROLES = {"system": "system", "human": "user", "ai": "assistant"}
def our_chat(prompt_value):           # plug OUR chat() into LangChain
    return chat([{"role": ROLES[m.type], "content": m.content}
                 for m in prompt_value.to_messages()])
llm = RunnableLambda(our_chat)

docs = [Document(page_content=t, metadata={"page": n})
        for n, t in load_pdf("travel-policy.pdf")]
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
splits = splitter.split_documents(docs)
store = InMemoryVectorStore.from_documents(splits, OurEmbeddings())
retriever = store.as_retriever(search_kwargs={"k": 3})

def format_docs(found):
    return "\n".join(f"[{i}] (page {d.metadata['page']}) {d.page_content}"
                     for i, d in enumerate(found, 1))

prompt = ChatPromptTemplate.from_messages([("system", SYSTEM),
    ("human", "Sources:\n{context}\n\nQuestion: {question}")])
chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()}
         | prompt | llm | StrOutputParser())

for q in QUESTIONS:
    print(f"langchain  | {q}\n           | {chain.invoke(q)}")
