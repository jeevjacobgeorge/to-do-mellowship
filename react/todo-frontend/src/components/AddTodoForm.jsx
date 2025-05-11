import { useState } from 'react';

const AddTodoForm = ({ onAdd }) => {
  const [todo, setTodo] = useState({
    title: '',
    description: '',
    deadline: '',
  });

  const handleChange = (e) => {
    setTodo({
      ...todo,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({
      ...todo,
      deadline: todo.deadline ? new Date(todo.deadline).toISOString() : null,
    });
    setTodo({
      title: '',
      description: '',
      deadline: '',
    });
  };

  return (
    <div className="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Add New Todo</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="block text-gray-700 mb-1">Title*</label>
          <input
            type="text"
            name="title"
            value={todo.title}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 mb-1">Description</label>
          <textarea
            name="description"
            value={todo.description}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            rows="2"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1">Deadline</label>
          <input
            type="datetime-local"
            name="deadline"
            value={todo.deadline}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Add Todo
        </button>
      </form>
    </div>
  );
};

export default AddTodoForm;