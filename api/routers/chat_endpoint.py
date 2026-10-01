from fastapi import APIRouter
from api.schemas import RequestInput, ResponseOutput
from graphs.build import graph

router = APIRouter()


@router.post('/chat', response_model=ResponseOutput)
async def chat_endpoint(request: RequestInput):
    config = {'configurable': {'thread_id': request.user_id}}
    state = {
        "user_id": request.user_id,
        "user_message": request.user_message,
        "matched_memory": [],
        "fact_to_save": {},
        "answer": ""
    }

    result = graph.invoke(state, config=config)
    return ResponseOutput(answer=result['answer'])