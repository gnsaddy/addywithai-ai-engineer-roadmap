# rag_llamaindex.py: version 3, the same RAG app with LlamaIndex.
#   pip install llama-index-core pypdf
from llama_index.core import (Document, PromptTemplate, Settings,
                              VectorStoreIndex)
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.node_parser import SentenceSplitter
from ingest import load_pdf
from models import embed, chat
from questions import QUESTIONS, SYSTEM

class OurEmbedding(BaseEmbedding):     # plug OUR embed() into LlamaIndex
    def _get_text_embedding(self, text): return embed([text])[0]
    def _get_query_embedding(self, query): return embed([query])[0]
    async def _aget_query_embedding(self, query): return embed([query])[0]

class OurLLM(CustomLLM):               # plug OUR chat() into LlamaIndex
    @property
    def metadata(self): return LLMMetadata(model_name="our-chat")
    @llm_completion_callback()
    def complete(self, prompt, formatted=False, **kw):
        text = chat([{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}])
        return CompletionResponse(text=text)
    def stream_complete(self, prompt, formatted=False, **kw):
        raise NotImplementedError

Settings.embed_model, Settings.llm = OurEmbedding(), OurLLM()
docs = [Document(text=t, metadata={"page": n})
        for n, t in load_pdf("travel-policy.pdf")]
splitter = SentenceSplitter(chunk_size=64, chunk_overlap=0)
index = VectorStoreIndex.from_documents(docs, transformations=[splitter])

QA = PromptTemplate("Sources:\n{context_str}\n\nQuestion: {query_str}")
engine = index.as_query_engine(similarity_top_k=3, text_qa_template=QA)

for q in QUESTIONS:
    print(f"llamaindex | {q}\n           | {engine.query(q)}")
