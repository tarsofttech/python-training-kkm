"""
Chat Session Manager - Multi-turn Conversation Management

This module provides a ChatSessionManager class that handles:
- Creating and managing chat sessions
- Maintaining conversation history
- Using CondensePlusContextChatEngine for context-aware responses
"""

from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from typing import Dict, List, Optional


class ChatSessionManager:
    """
    Manages multiple chat sessions with conversation memory.
    
    Each session maintains its own conversation history and chat engine,
    allowing multiple users to have independent conversations.
    """
    
    def __init__(self):
        """Initialize the chat session manager."""
        self.sessions: Dict[str, CondensePlusContextChatEngine] = {}
        print("💬 Chat Session Manager initialized")
    
    def create_session(self, session_id: str, index) -> None:
        """
        Create a new chat session.
        
        Args:
            session_id: Unique identifier for the session
            index: VectorStoreIndex to use for retrieval
        """
        if session_id in self.sessions:
            print(f"⚠️  Session {session_id} already exists, will be replaced")
        
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        
        chat_engine = CondensePlusContextChatEngine.from_defaults(
            index.as_retriever(),
            memory=memory,
            verbose=True
        )
        
        self.sessions[session_id] = chat_engine
        
        print(f"✅ Created chat session: {session_id}")
    
    def get_or_create(self, session_id: str, index) -> CondensePlusContextChatEngine:
        """
        Get an existing session or create a new one.
        
        Args:
            session_id: Unique identifier for the session
            index: VectorStoreIndex to use if creating new session
        
        Returns:
            CondensePlusContextChatEngine: The chat engine for this session
        """
        if session_id not in self.sessions:
            self.create_session(session_id, index)
        
        return self.sessions[session_id]
    
    async def chat(self, session_id: str, message: str, index) -> dict:
        """
        Send a message in a chat session and get a response.
        
        Args:
            session_id: Unique identifier for the session
            message: User's message
            index: VectorStoreIndex for retrieval
        
        Returns:
            dict: Contains response, sources, and session_id
        """
        chat_engine = self.get_or_create(session_id, index)
        
        print(f"💬 [{session_id}] User: {message}")
        
        response = await chat_engine.achat(message)
        
        sources = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                source_name = node.metadata.get('file_name', 'Unknown')
                score = node.score if hasattr(node, 'score') else 0.0
                sources.append(f"{source_name} (score: {score:.2f})")
        
        print(f"🤖 [{session_id}] Assistant: {str(response)[:100]}...")
        
        return {
            "session_id": session_id,
            "response": str(response),
            "sources": sources
        }
    
    def get_history(self, session_id: str) -> List[dict]:
        """
        Get the conversation history for a session.
        
        Args:
            session_id: Unique identifier for the session
        
        Returns:
            List[dict]: List of messages with role and content
        """
        if session_id not in self.sessions:
            return []
        
        chat_engine = self.sessions[session_id]
        
        messages = []
        
        if hasattr(chat_engine, 'memory') and hasattr(chat_engine.memory, 'get_all'):
            chat_history = chat_engine.memory.get_all()
            
            for msg in chat_history:
                messages.append({
                    "role": msg.role.value if hasattr(msg.role, 'value') else str(msg.role),
                    "content": msg.content
                })
        
        return messages
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session.
        
        Args:
            session_id: Unique identifier for the session
        
        Returns:
            bool: True if session was deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"🗑️  Deleted session: {session_id}")
            return True
        
        print(f"⚠️  Session not found: {session_id}")
        return False
    
    def list_sessions(self) -> List[str]:
        """
        Get a list of all active session IDs.
        
        Returns:
            List[str]: List of session IDs
        """
        return list(self.sessions.keys())
    
    def get_session_count(self) -> int:
        """
        Get the number of active sessions.
        
        Returns:
            int: Number of active sessions
        """
        return len(self.sessions)
