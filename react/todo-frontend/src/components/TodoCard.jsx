import { useState } from 'react';

const TodoCard = ({ todo, onComplete, onDelete, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTodo, setEditedTodo] = useState({
    title: todo.title,
    description: todo.description || '',
    deadline: todo.deadline ? new Date(todo.deadline).toISOString().slice(0, 16) : '',
  });

  const isOverdue = todo.deadline && new Date(todo.deadline) < new Date() && !todo.completed;

  const handleChange = (e) => {
    setEditedTodo({
      ...editedTodo,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onEdit(todo.id, {
      ...editedTodo,
      deadline: editedTodo.deadline ? new Date(editedTodo.deadline).toISOString() : null,
    });
    setIsEditing(false);
  };

  const cardClass = `p-4 mb-4 rounded-lg shadow ${
    todo.completed ? "bg-green-50 border border-green-200" : 
    isOverdue ? "bg-red-50 border border-red-200" : 
    "bg-white border border-gray-200"
  }`;

  return (
    <div className={cardClass}>
      {isEditing ? (
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <input
              type="text"
              name="title"
              value={editedTodo.title}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-2">
            <textarea
              name="description"
              value={editedTodo.description}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              rows="2"
            />
          </div>
          <div className="mb-4">
            <input
              type="datetime-local"
              name="deadline"
              value={editedTodo.deadline}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Save
            </button>
          </div>
        </form>
      ) : (
        <>
          <div className="flex justify-between items-start mb-2">
            <h3 className={`text-lg font-medium ${todo.completed ? "line-through text-gray-500" : ""}`}>
              {todo.title}
            </h3>
            <div className="flex space-x-2">
              {!todo.completed && (
                <button
                  onClick={() => setIsEditing(true)}
                  className="text-blue-500 hover:text-blue-700"
                >
                  Edit
                </button>
              )}
              {!todo.completed && (
                <button
                  onClick={() => onComplete(todo.id)}
                  className="text-green-500 hover:text-green-700"
                >
                  Complete
                </button>
              )}
              <button
                onClick={() => onDelete(todo.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </div>
          
          {todo.description && (
            <p className="text-gray-600 mb-2">{todo.description}</p>
          )}
          
          {todo.deadline && (
            <div className="text-sm text-gray-500">
              Deadline: {new Date(todo.deadline).toLocaleString()}
              {isOverdue && <span className="ml-2 text-red-500">Overdue!</span>}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default TodoCard;