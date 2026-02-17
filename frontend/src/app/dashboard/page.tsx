"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import { apiFetch } from "@/lib/api";
import TaskForm from "@/components/task-form";
import TaskList from "@/components/task-list";

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskListResponse {
  tasks: Task[];
}

export default function DashboardPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const userId = session?.user?.id;

  const fetchTasks = useCallback(async () => {
    if (!userId) return;
    try {
      setError(null);
      const data = await apiFetch<TaskListResponse>(
        `/api/${userId}/tasks`,
      );
      setTasks(data.tasks);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load tasks.",
      );
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/signin");
      return;
    }
    if (userId) {
      fetchTasks();
    }
  }, [isPending, session, userId, fetchTasks, router]);

  async function handleSignOut() {
    await signOut();
    router.push("/signin");
    router.refresh();
  }

  async function handleTaskCreated() {
    setShowForm(false);
    await fetchTasks();
  }

  async function handleToggleComplete(taskId: string) {
    const prev = tasks;
    setTasks((t) =>
      t.map((task) =>
        task.id === taskId ? { ...task, completed: !task.completed } : task,
      ),
    );
    try {
      await apiFetch(`/api/${userId}/tasks/${taskId}/complete`, {
        method: "PATCH",
      });
    } catch {
      setTasks(prev);
      setError("Failed to update task.");
    }
  }

  async function handleDeleteTask(taskId: string) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this task?",
    );
    if (!confirmed) return;

    const prev = tasks;
    setTasks((t) => t.filter((task) => task.id !== taskId));
    try {
      await apiFetch(`/api/${userId}/tasks/${taskId}`, {
        method: "DELETE",
      });
    } catch {
      setTasks(prev);
      setError("Failed to delete task.");
    }
  }

  async function handleUpdateTask(
    taskId: string,
    title: string,
    description: string,
  ) {
    const prev = tasks;
    setTasks((t) =>
      t.map((task) =>
        task.id === taskId ? { ...task, title, description } : task,
      ),
    );
    try {
      await apiFetch(`/api/${userId}/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify({ title, description }),
      });
    } catch {
      setTasks(prev);
      setError("Failed to update task.");
    }
  }

  if (isPending) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="mx-auto min-h-screen max-w-2xl px-4 py-8">
      <header className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-bold">My Tasks</h1>
        <button
          onClick={handleSignOut}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100"
        >
          Sign Out
        </button>
      </header>

      {error && (
        <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="mb-6">
        {showForm ? (
          <TaskForm
            userId={userId!}
            onSuccess={handleTaskCreated}
            onCancel={() => setShowForm(false)}
          />
        ) : (
          <button
            onClick={() => setShowForm(true)}
            className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Add Task
          </button>
        )}
      </div>

      {loading ? (
        <p className="text-gray-500">Loading tasks...</p>
      ) : (
        <TaskList
          tasks={tasks}
          userId={userId!}
          onToggle={handleToggleComplete}
          onDelete={handleDeleteTask}
          onUpdate={handleUpdateTask}
        />
      )}
    </div>
  );
}
