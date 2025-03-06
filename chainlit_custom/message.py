import asyncio
from typing import Dict, List, Optional, Union

from chainlit.action import Action
from chainlit.element import ElementBased
from chainlit.message import Message
from chainlit.telemetry import trace_event
from literalai.observability.step import MessageStepType


class CustomMessage(Message):
    def __init__(
        self,
        content: Union[str, Dict],
        author: Optional[str] = None,
        language: Optional[str] = None,
        actions: Optional[List[Action]] = None,
        elements: Optional[List[ElementBased]] = None,
        type: MessageStepType = "assistant_message",
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        id: Optional[str] = None,
        parent_id: Optional[str] = None,
        created_at: Union[str, None] = None,
    ):
        # Initialize the parent class (Message) with required arguments
        super().__init__(
            content=content,
            author=author,
            language=language,
            actions=actions,
            elements=elements,
            type=type,
            metadata=metadata,
            tags=tags,
            id=id,
            parent_id=parent_id,
            created_at=created_at,
        )

    async def send(self):
        """
        Send the message to the UI and persist it in the cloud if a project ID is configured.
        Return the ID of the message.
        """
        trace_event("send_message")
        await super().send()

        # Create tasks for all actions and elements
        tasks = [action.send(for_id=None) for action in self.actions]
        tasks.extend(element.send(for_id=None) for element in self.elements)

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

        return self
