"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

interface TaskFormProps {
  userId: string;
  onSuccess?: () => void;
  onUpdate?: (title: string, description: string) => void;
  onCancel: () => void;
  initialTitle?: string;
  initialDescription?: string;
  taskId?: string;
  mode?: "create" | "edit";
}

export default function TaskForm({
  userId,
  onSuccess,
  onUpdate,
  onCancel,
  initialTitle = "",
  initialDescription = "",
  taskId,
  mode = "create",
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) {
      setError("Title is required.");
      return;
    }
    setError(null);

    if (mode === "edit" && onUpdate) {
      onUpdate(title.trim(), description);
      return;
    }

    setLoading(true);
    try {
      await apiFetch(`/api/${userId}/tasks`, {
        method: "POST",
        body: JSON.stringify({
          title: title.trim(),
          description: description,
        }),
      });
      onSuccess?.();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to save task.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
    >
      {error && (
        <div className="mb-3 rounded-md bg-red-50 p-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="mb-3">
        <label
          htmlFor="task-title"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          placeholder="What needs to be done?"
        />
      </div>

      <div className="mb-4">
        <label
          htmlFor="task-description"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Description
        </label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={1000}
          rows={3}
          className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          placeholder="Add details (optional)"
        />
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading
            ? "Saving..."
            : mode === "edit"
              ? "Save Changes"
              : "Create Task"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
