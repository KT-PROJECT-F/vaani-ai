from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from app.agent.graph import run_agent
from app.agent.state import AgentState
from app.schemas.api import ChatIn, ChatOut
from app.tools.pricing import estimate_price

router = APIRouter()


def to_chat_out(state: AgentState) -> ChatOut:
    request = state["request"]
    price = estimate_price(request.service, request.city) if request.city else None
    return ChatOut(
        reply=state["reply"],
        language=state.get("language", "en"),
        request=request,
        safety_steps=state.get("safety_steps", []),
        price_range=price,
    )


@router.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn) -> ChatOut:
    # TODO (Pair 2): use body.session_id as the LangGraph thread_id for multi-turn memory.
    state = await run_in_threadpool(run_agent, body.message)
    return to_chat_out(state)
