"""Runtime helpers for invoking the ADK agent from a web API."""

from __future__ import annotations

import uuid
from typing import Optional

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agent import APP_NAME, root_agent


class AgentRuntime:
    def __init__(self) -> None:
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=self._session_service,
        )
        self._sessions: set[str] = set()

    def _ensure_session(self, user_id: str, session_id: str) -> None:
        if session_id in self._sessions:
            return
        self._session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        self._sessions.add(session_id)

    async def send_message(self, message: str, user_id: str | None, session_id: str | None) -> dict:
        user_id = user_id or "demo-user"
        session_id = session_id or str(uuid.uuid4())
        self._ensure_session(user_id, session_id)

        content = types.Content(role="user", parts=[types.Part(text=message)])
        final_text: Optional[str] = None

        async for event in self._runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_text = "".join(
                        part.text for part in event.content.parts if hasattr(part, "text")
                    )

        return {"reply": final_text or "", "session_id": session_id}
