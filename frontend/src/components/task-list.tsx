import TaskItem from "./task-item";
import EmptyState from "./empty-state";

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  userId: string;
  onTaskUpdated: () => void;
}

export default function TaskList({
  tasks,
  userId,
  onTaskUpdated,
}: TaskListProps) {
  if (tasks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          userId={userId}
          onTaskUpdated={onTaskUpdated}
        />
      ))}
    </div>
  );
}
