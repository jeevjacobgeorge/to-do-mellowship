export default function TodoList({ todos, onComplete, onDelete }) {
  const groups = [
    { key: "to_be_done", label: "To Be Done", color: "blue" },
    { key: "time_elapsed", label: "Time Elapsed", color: "red" },
    { key: "completed", label: "Completed", color: "green" },
  ];

  return (
    <div className="mt-8 space-y-8">
      {groups.map(({ key, label, color }) => (
        <div key={key}>
          <h3 className={`text-xl font-semibold text-${color}-600 mb-4`}>{label}</h3>
          <div className="space-y-2">
            {todos[key]?.map((todo) => (
              <div
                key={todo.id}
                className="flex justify-between items-center p-4 bg-gray-50 rounded-lg shadow-sm"
              >
                <div>
                  <div className="font-medium">{todo.title}</div>
                  <div className="text-sm text-gray-500">{new Date(todo.deadline).toLocaleString()}</div>
                </div>
                <div className="flex space-x-2">
                  {!todo.completed && (
                    <button
                      onClick={() => onComplete(todo.id)}
                      className={`px-3 py-1 text-sm rounded bg-${color}-500 text-white hover:bg-${color}-600 transition`}
                    >
                      Complete
                    </button>
                  )}
                  <button
                    onClick={() => onDelete(todo.id)}
                    className="px-3 py-1 text-sm rounded bg-gray-300 text-gray-800 hover:bg-gray-400 transition"
                  >
                    Delete
                  </button>
                </div>
              </div>
            )) || <p className="text-gray-400">No items</p>}
          </div>
        </div>
      ))}
    </div>
  );
}
