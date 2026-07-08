# TestRepo - Queue Management System

A web application for managing users and queued requests with admin and user interfaces.

## Features

### Admin UI
- Manage users (view, edit, delete)
- Manage queued requests (view, approve, reject)

### User UI
- User registration
- User profile management
- Register new queued requests
- View list of queued requests
- Acquire (claim) queued requests
- Complete queued requests and provide points

## Project Structure

```
├── backend/
│   ├── server.js
│   ├── routes/
│   │   ├── auth.js
│   │   ├── users.js
│   │   ├── requests.js
│   │   └── admin.js
│   ├── models/
│   │   ├── User.js
│   │   └── QueuedRequest.js
│   └── package.json
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── admin.js
│   │   └── user.js
│   └── pages/
│       ├── admin.html
│       └── user.html
└── README.md
```

## Installation

1. Install dependencies:
```bash
cd backend
npm install
```

2. Start the server:
```bash
npm start
```

3. Open frontend files in a browser or serve with a static server.

## Technologies

- **Backend**: Node.js, Express.js
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (can be switched to PostgreSQL/MongoDB)
