from typing import Dict, List, Optional
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse

app = FastAPI()

class ResultContext(BaseModel):
    content: str
    document_id: str
    rank: Optional[int] = None
    score: Optional[float] = None
    passage_id: Optional[int] = None

class SynonymResponse(BaseModel):
    term: Dict[str, List[str]]

# Mock search results
MOCK_SEARCH_RESULTS = [
    {
        "content": "Mock content from document 1",
        "document_id": "doc1",
        "rank": 1,
        "score": 18.00,
        "passage_id": 1
    },
    {
        "content": "Mock content from document 2",
        "document_id": "doc2",
        "rank": 2,
        "score": 17.96,
        "passage_id": 2
    }
]


@app.get("/")
async def root(request: Request):
    docs_url = request.url_for("swagger_ui_html")
    return JSONResponse({"message": f"Mock doc search API - see docs at {docs_url}"})

@app.get("/search")
async def search(
    query: str = Query(description="Keywords or search terms to find in documents"),
    k: int = Query(3, description="Number of relevant documents to retrieve"),
):
    # Return k number of mock results, or all if k > len(mock_results)
    return JSONResponse(MOCK_SEARCH_RESULTS[:k])

@app.post("/summarise")
async def summarise(
    query: str = Body(..., description="Your query as a string"),
    results_context: List[ResultContext] = Body(
        ...,
        description="List of search result objects"
    ),
):
    async def stream_mock_answer():
        mock_response = f"Mock summary for query: {query} based on {len(results_context)} documents."
        yield mock_response

    return StreamingResponse(stream_mock_answer(), media_type="text/plain")

@app.get("/search-and-summarise")
async def search_and_summarise(
    query: str = Query(description="Keywords or search terms to find in documents"),
    k: int = Query(3, description="Number of relevant documents to retrieve"),
):
    async def stream_mock_answer():
        mock_response = f"Mock combined search and summary for query: {query} with {k} results."
        yield mock_response

    return StreamingResponse(stream_mock_answer(), media_type="text/plain")

@app.get("/synonyms", response_model=SynonymResponse)
def synonyms(
    query: str = Query(
        ...,
        description="Search phrase to pull synonyms from",
        example="Where can I find basalt"
    )
):
    # Mock synonym response
    mock_synonyms = {
        "basalt": ["igneous rock", "volcanic rock", "mafic rock"]
    }
    return JSONResponse(content={"term": mock_synonyms})

@app.get("/pdfsummary")
async def pdf_summary(
    document_id: str = Query(
        ...,
        description="Id of the document to summarise",
        example="0001930d-ead7-42d1-ad17-50557fdb2489-1.pdf"
    ),
    system_prompt: str = Query("", description="Optional System prompt to provide to the llm"),
    sampling_method: str = Query(
        "truncate",
        description="Sampling method to use if the document size exceeds the rate limit"
    ),
):
    async def stream_mock_summary():
        mock_summary = f"Mock PDF summary for document: {document_id}"
        yield mock_summary

    return StreamingResponse(stream_mock_summary(), media_type="text/plain")

@app.post("/add-to-index")
def add_to_index(
    doc: str = Body(
        ...,
        description="The content of the document as a string",
        example="lorem ipsum dolor sit amet..."
    ),
    id: str = Body(
        ...,
        description="The ID of the document as a string",
        example="9c8f3271-83d4-47ef-80c9-c6805d798422-1.pdf"
    ),
):
    return JSONResponse({
        "message": f"Mock response: Added document {id} to index successfully."
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)