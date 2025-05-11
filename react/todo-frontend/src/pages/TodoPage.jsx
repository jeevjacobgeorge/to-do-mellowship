import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTodos, createTodo, completeTodo, updateTodo, deleteTodo } from '../api/todoApi';
import { useAuth } from '../context/AuthContext';
import TodoCard from '../components/TodoCard';
import AddTodoForm from '../components/AddTodoForm';

const TodoPage = () => {
  const [todos, setTodos] = useState({
    to_be_done: [],
    completed: [],
    time_elapsed: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await getTodos();
      setTodos(data);
      setError('');
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError('Failed to load todos');
      if (err.response?.status === 401) {
        // Token expired
        logout();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (todoData) => {
    try {
      await createTodo(todoData);
      fetchTodos();
    } catch (err) {
      setError('Failed to create todo');
      console.error(err);
    }
  };

  const handleCompleteTodo = async (todoId) => {
    try {
      await completeTodo(todoId);
      fetchTodos();
    } catch (err) {
      setError('Failed to complete todo');
      console.error(err);
    }
  };

  const handleUpdateTodo = async (todoId, todoData) => {
    try {
      await updateTodo(todoId, todoData);
      fetchTodos();
    } catch (err) {
      setError('Failed to update todo');
      console.error(err);
    }
  };

  const handleDeleteTodo = async (todoId) => {
    try {
      await deleteTodo(todoId);
      fetchTodos();
    } catch (err) {
      setError('Failed to delete todo');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading todos...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto mt-8 px-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Todo Dashboard</h1>
        <button
          onClick={logout}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>

      {error && (
        <div className="p-3 mb-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <AddTodoForm onAdd={handleAddTodo} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div>
          <h2 className="text-xl font-bold mb-4">To Be Done</h2>
          {todos.to_be_done.length === 0 ? (
            <p className="text-gray-500">No active todos</p>
          ) : (
            todos.to_be_done.map((todo) => (
              <TodoCard
                key={todo.id}
                todo={todo}
                onComplete={handleCompleteTodo}
                onDelete={handleDeleteTodo}
                onEdit={handleUpdateTodo}
              />
            ))
          )}
        </div>

        <div>
          <h2 className="text-xl font-bold mb-4 text-red-500">Overdue</h2>
          {todos.time_elapsed.length === 0 ? (
            <p className="text-gray-500">No overdue todos</p>
          ) : (
            todos.time_elapsed.map((todo) => (
              <TodoCard
                key={todo.id}
                todo={todo}
                onComplete={handleCompleteTodo}
                onDelete={handleDeleteTodo}
                onEdit={handleUpdateTodo}
              />
            ))
          )}
        </div>

        <div>
          <h2 className="text-xl font-bold mb-4 text-green-500">Completed</h2>
          {todos.completed.length === 0 ? (
            <p className="text-gray-500">No completed todos</p>
          ) : (
            todos.completed.map((todo) => (
              <TodoCard
                key={todo.id}
                todo={todo}
                onComplete={handleCompleteTodo}
                onDelete={handleDeleteTodo}
                onEdit={handleUpdateTodo}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default TodoPage;