"use client";

import { useState } from "react";
import TaskForm from "./task-form";

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  userId: string;
  onToggle: (taskId: string) => void;
  onDelete: (taskId: string) => void;
  onUpdate: (taskId: string, title: string, description: string) => void;
}

export default function TaskItem({
  task,
  userId,
  onToggle,
  onDelete,
  onUpdate,
}: TaskItemProps) {
  const [editing, setEditing] = useState(false);

  if (editing) {
    return (
      <TaskForm
        userId={userId}
        taskId={task.id}
        mode="edit"
        initialTitle={task.title}
        initialDescription={task.description}
        onUpdate={(title, description) => {
          setEditing(false);
          onUpdate(task.id, title, description);
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  return (
    <div
      className={`flex items-start gap-3 rounded-lg border bg-white p-4 shadow-sm ${
        task.completed ? "border-gray-200 opacity-60" : "border-gray-200"
      }`}
    >
      <button
        onClick={() => onToggle(task.id)}
        className={`mt-0.5 h-5 w-5 flex-shrink-0 rounded border-2 ${
          task.completed
            ? "border-green-500 bg-green-500 text-white"
            : "border-gray-300 hover:border-blue-500"
        }`}
        aria-label={
          task.completed ? "Mark as incomplete" : "Mark as complete"
        }
      >
        {task.completed && (
          <svg
            className="h-full w-full"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={3}
              d="M5 13l4 4L19 7"
            />
          </svg>
        )}
      </button>

      <div className="min-w-0 flex-1">
        <h3
          className={`font-medium ${
            task.completed ? "text-gray-400 line-through" : "text-gray-900"
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p
            className={`mt-1 text-sm ${
              task.completed ? "text-gray-300 line-through" : "text-gray-600"
            }`}
          >
            {task.description}
          </p>
        )}
      </div>

      <div className="flex gap-1">
        <button
          onClick={() => setEditing(true)}
          className="rounded px-2 py-1 text-sm text-gray-500 hover:bg-gray-100 hover:text-gray-700"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="rounded px-2 py-1 text-sm text-red-500 hover:bg-red-50 hover:text-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
