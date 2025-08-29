import asyncio
from typing import Optional, Union, Any
from uuid import UUID
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult


class QueueCallBackHandler(AsyncCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self.final_answer_seen = False

    async def __aiter__(self):
        while True:
            print("token async for ile getirildi")
            if self.queue.empty():
                print("queue empty")
                await asyncio.sleep(0.1)
                continue

            token_or_done = await self.queue.get()
            print(f"QUEUE : {token_or_done}")
            if token_or_done == "<<DONE>>":
                print("done çalıştı")
                return
            else:
                yield token_or_done

    async def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[list[str]] = None,
            **kwargs: Any,
    ) -> None:
        #print(chunk)
        if tool_calls := chunk.message.additional_kwargs.get("tool_calls"):
            if tool_name := tool_calls[0]["function"]["name"] == "final_answer":
                self.final_answer_seen = True
        self.queue.put_nowait(chunk)
        #print(f"QUEUE {self.queue}")

    async def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[list[str]] = None,
            **kwargs: Any,
    ) -> None:
        try:
            if finish_because_tool_calls := response.generations[0][0].message.response_metadata.get(
                    "finish_reason") == "tool_calls":
                print(self.final_answer_seen)
                if self.final_answer_seen:
                    self.queue.put_nowait("<<DONE>>")
                    return
                else:
                    self.queue.put_nowait("<<STEP_END>>")
            else:
                self.queue.put_nowait("<<DONE>>")
                return
                # TODO SORUN BURADA
            print(f"QUEUE : {self.queue}")
        except Exception as e:
            print(f"EXCEPTİON : {e}")


    def copy(self):
        return QueueCallBackHandler(queue=self.queue)

    async def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[list[str]] = None,
            metadata: Optional[dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        pass
