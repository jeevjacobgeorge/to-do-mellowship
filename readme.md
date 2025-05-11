
---

```markdown
# 📝 ToDo App – FastAPI + React

A modern full-stack ToDo application built using:

- **Backend:** FastAPI + PostgreSQL + JWT Authentication
- **Frontend:** React (Vite) + Tailwind CSS

---

## 📁 Project Structure

```

mellowship/todo/
├── fastapi/              # Backend (FastAPI)
│   ├── app/              # API logic, models, routes
│   ├── main.py           # Entry point for the server
│   
├── react/todo-frontend/  # Frontend (React)
│   ├── src/              # All React components and pages
│   ├── index.html        # Root HTML
│   

````

---

## ⚙️ Backend Setup (FastAPI)

### ✅ Requirements

- Python 3.9+
- PostgreSQL (or SQLite for testing)

### ▶️ Running Locally

```bash
cd fastapi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
````

Make sure your `.env` has the correct DB and JWT settings.

---

## 💻 Frontend Setup (React)

### ✅ Requirements

* Node.js 16+
* Vite

### ▶️ Running Locally

```bash
cd react/todo-frontend
npm install
npm run dev
```

The app runs on `http://localhost:5173` by default.

Update `axios` base URL in `axiosInstance.js` to point to your backend:

```js
// axiosInstance.js
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000", // Adjust as needed
});
```

---

## 🔐 Features

* 🔐 User authentication (JWT)
* 🗃️ Create, edit, delete todos
* ⏰ Filter by due time/status
* 🎨 Styled with Tailwind CSS
* 📦 Built with Vite for fast frontend dev

---

## 🛠 Tech Stack

| Frontend     | Backend  | Auth   |
| ------------ | -------- | ------ |
| React + Vite | FastAPI  | JWT    |
| Tailwind CSS | SQLModel | OAuth2 |

---

## 📄 License

MIT License – free for personal and commercial use.

```

---

```
