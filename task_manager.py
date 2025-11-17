import json
import os

class TaskManager:
    def __init__(self, data_file='tasks.json'):
        self.data_file = data_file
        self.tasks = self._load_tasks()
        self._next_id = max([task['id'] for task in self.tasks]) + 1 if self.tasks else 1

    def _load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def _save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, description):
        task = {
            'id': self._next_id,
            'description': description,
            'completed': False
        }
        self.tasks.append(task)
        self._next_id += 1
        self._save_tasks()
        return task

    def get_tasks(self):
        return sorted(self.tasks, key=lambda x: x['id'])

    def update_task(self, task_id, description=None, completed=None):
        for task in self.tasks:
            if task['id'] == task_id:
                if description is not None:
                    task['description'] = description
                if completed is not None:
                    task['completed'] = completed
                self._save_tasks()
                return task
        return None # Task not found

    def delete_task(self, task_id):
        initial_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        if len(self.tasks) < initial_len:
            self._save_tasks()
            return True
        return False # Task not found

    def flush_completed_tasks(self):
        initial_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task['completed']]
        if len(self.tasks) < initial_len:
            self._save_tasks()
            return True
        return False # No completed tasks to flush
