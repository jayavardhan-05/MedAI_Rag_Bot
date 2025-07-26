from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

app = FastAPI(title="MED AI", description="AI-Powered Medical Research Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and Response models
class QuestionRequest(BaseModel):
    question: str

class SourceDocument(BaseModel):
    content: str
    metadata: Dict[str, Any]

class AnswerResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]

# Global variables for the AI components
db = None
qa_chain = None

@app.on_event("startup")
async def startup_event():
    """Initialize the AI components when the server starts."""
    global db, qa_chain
    
    try:
        # Load the FAISS index
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Check if the FAISS index exists
        index_path = "my_faiss_index"
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        
        db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        
        # Initialize the language model (you'll need to set up Google API key)
        # For now, we'll use a placeholder - in production, set GOOGLE_API_KEY environment variable
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.3,
                convert_system_message_to_human=True
            )
        except Exception as e:
            print(f"Warning: Could not initialize Google Gemini. Using mock responses. Error: {e}")
            llm = None
        
        # Create a custom prompt template
        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Provide a clear and concise answer based on the medical information provided.

        Context: {context}

        Question: {question}
        
        Answer:"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        if llm:
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=db.as_retriever(search_kwargs={"k": 4}),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True
            )
        
        print("✅ MED AI backend initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing MED AI backend: {e}")
        print("Make sure the FAISS index exists and Google API key is set.")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "MED AI Backend is running", "status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Process a medical question and return an AI-generated answer with sources.
    """
    global qa_chain, db
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        if qa_chain is None:
            # Fallback: if QA chain is not available, provide a mock response
            if db is None:
                raise HTTPException(status_code=503, detail="Medical knowledge base not available")
            
            # At least retrieve relevant documents
            docs = db.similarity_search(request.question, k=4)
            sources = [
                SourceDocument(
                    content=doc.page_content,
                    metadata=doc.metadata
                )
                for doc in docs
            ]
            
            return AnswerResponse(
                answer="I apologize, but the AI model is not currently available. However, I've found some relevant source materials that might help answer your question. Please check the source documents for relevant information.",
                sources=sources
            )
        
        # Use the QA chain to get an answer
        result = qa_chain({"query": request.question})
        
        # Extract the answer and sources
        answer = result["result"]
        source_docs = result["source_documents"]
        
        sources = [
            SourceDocument(
                content=doc.page_content,
                metadata=doc.metadata
            )
            for doc in source_docs
        ]
        
        return AnswerResponse(answer=answer, sources=sources)
        
    except Exception as e:
        print(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing your question: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    global db, qa_chain
    
    status = {
        "database_loaded": db is not None,
        "qa_chain_ready": qa_chain is not None,
        "status": "healthy" if (db is not None) else "degraded"
    }
    
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)