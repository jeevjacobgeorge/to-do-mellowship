
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
├── react/todo-frontend/  # Frontend (React)
│   ├── src/              # All React components and pages
│   ├── index.html        # Root HTML

````

---

## 🛢️ Start PostgreSQL with Docker

```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=jeev@123 \
  -p 5432:5432 \
  -d postgres
````

This will run a PostgreSQL container with password `jeev@123`.

---

## ⚙️ Backend Setup (FastAPI)

### ✅ Requirements

* Python 3.9+
* PostgreSQL running on port `5432`

### ▶️ Running Locally

```bash
cd fastapi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Ensure your `.env` has the correct DB URL:

```env
DATABASE_URL=postgresql://postgres:jeev@123@localhost:5432/postgres
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

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

App runs on `http://localhost:5173`.

Update `axiosInstance.js` with your backend base URL:

```js
// axiosInstance.js
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000", // FastAPI backend
});
```

---

## 🔐 Features

* 🔐 User authentication (JWT)
* 🗃️ Create, edit, delete todos
* ⏰ Filter by due time/status
* 🎨 Styled with Tailwind CSS
* ⚡ Vite for fast frontend dev

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
