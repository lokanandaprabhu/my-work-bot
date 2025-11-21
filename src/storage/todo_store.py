"""
Personal TODO list storage using JSON.
Stores user-specific todos with CRUD operations.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class TodoStore:
    """Manages user todo lists with JSON persistence."""
    
    def __init__(self, storage_path: str = "data/todos.json"):
        """
        Initialize todo storage.
        
        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage directory and file if they don't exist."""
        storage_dir = os.path.dirname(self.storage_path)
        if storage_dir and not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        if not os.path.exists(self.storage_path):
            self._save_data({})
    
    def _load_data(self) -> Dict:
        """Load all todo data from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, data: Dict):
        """Save all todo data to storage."""
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_user_todos(self, user_id: str) -> List[Dict]:
        """Get all todos for a specific user."""
        data = self._load_data()
        return data.get(user_id, {}).get("todos", [])
    
    def _save_user_todos(self, user_id: str, todos: List[Dict]):
        """Save todos for a specific user."""
        data = self._load_data()
        if user_id not in data:
            data[user_id] = {}
        data[user_id]["todos"] = todos
        data[user_id]["updated_at"] = datetime.now().isoformat()
        self._save_data(data)
    
    def add_todo(self, user_id: str, description: str, priority: str = "medium") -> Dict:
        """
        Add a new todo for a user.
        
        Args:
            user_id: Slack user ID
            description: Todo description
            priority: Priority level (high/medium/low)
            
        Returns:
            The created todo
        """
        todos = self._get_user_todos(user_id)
        
        # Generate new ID
        new_id = max([t.get("id", 0) for t in todos], default=0) + 1
        
        new_todo = {
            "id": new_id,
            "description": description,
            "completed": False,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        todos.append(new_todo)
        self._save_user_todos(user_id, todos)
        
        return new_todo
    
    def get_todos(self, user_id: str, include_completed: bool = True) -> List[Dict]:
        """
        Get all todos for a user.
        
        Args:
            user_id: Slack user ID
            include_completed: Whether to include completed todos
            
        Returns:
            List of todos
        """
        todos = self._get_user_todos(user_id)
        
        if not include_completed:
            todos = [t for t in todos if not t.get("completed", False)]
        
        return sorted(todos, key=lambda x: x.get("id", 0))
    
    def get_todo(self, user_id: str, todo_id: int) -> Optional[Dict]:
        """
        Get a specific todo.
        
        Args:
            user_id: Slack user ID
            todo_id: Todo ID
            
        Returns:
            The todo or None if not found
        """
        todos = self._get_user_todos(user_id)
        for todo in todos:
            if todo.get("id") == todo_id:
                return todo
        return None
    
    def update_todo(self, user_id: str, todo_id: int, description: str) -> Optional[Dict]:
        """
        Update a todo's description.
        
        Args:
            user_id: Slack user ID
            todo_id: Todo ID
            description: New description
            
        Returns:
            Updated todo or None if not found
        """
        todos = self._get_user_todos(user_id)
        
        for todo in todos:
            if todo.get("id") == todo_id:
                todo["description"] = description
                todo["updated_at"] = datetime.now().isoformat()
                self._save_user_todos(user_id, todos)
                return todo
        
        return None
    
    def complete_todo(self, user_id: str, todo_id: int) -> Optional[Dict]:
        """
        Mark a todo as completed.
        
        Args:
            user_id: Slack user ID
            todo_id: Todo ID
            
        Returns:
            Updated todo or None if not found
        """
        todos = self._get_user_todos(user_id)
        
        for todo in todos:
            if todo.get("id") == todo_id:
                todo["completed"] = True
                todo["completed_at"] = datetime.now().isoformat()
                todo["updated_at"] = datetime.now().isoformat()
                self._save_user_todos(user_id, todos)
                return todo
        
        return None
    
    def delete_todo(self, user_id: str, todo_id: int) -> bool:
        """
        Delete a todo.
        
        Args:
            user_id: Slack user ID
            todo_id: Todo ID
            
        Returns:
            True if deleted, False if not found
        """
        todos = self._get_user_todos(user_id)
        initial_count = len(todos)
        
        todos = [t for t in todos if t.get("id") != todo_id]
        
        if len(todos) < initial_count:
            self._save_user_todos(user_id, todos)
            return True
        
        return False
    
    def get_stats(self, user_id: str) -> Dict:
        """
        Get statistics for a user's todos.
        
        Args:
            user_id: Slack user ID
            
        Returns:
            Dictionary with stats
        """
        todos = self._get_user_todos(user_id)
        
        total = len(todos)
        completed = len([t for t in todos if t.get("completed", False)])
        active = total - completed
        
        return {
            "total": total,
            "active": active,
            "completed": completed
        }


# Global instance
_todo_store = None

def get_todo_store() -> TodoStore:
    """Get the global todo store instance."""
    global _todo_store
    if _todo_store is None:
        _todo_store = TodoStore()
    return _todo_store

