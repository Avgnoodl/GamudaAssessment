# Football Match Tracker

A simple web application that displays football matches and their details.

## Architecture

```
+-----------+        HTTP        +-----------+
|  Vue UI   +------------------> |  FastAPI  |
| (Vite &   |  fetch /api/matches|  Backend  |
|  Vuetify) | <----------------- +-----------+
```

- **Frontend:** Vue 3 + Vuetify located in `vuetify-project/`
- **Backend:** FastAPI app in `backend/`

## Setup

### Backend
1. `cd backend`
2. (optional) create a virtual environment
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`

### Frontend
1. `cd vuetify-project`
2. `npm install`
3. `npm run dev`

Visit `http://localhost:5173` in your browser while the backend runs on `http://localhost:8000`.

## Features

- List of mock football matches with score and status
- Match details include goal events and kickoff time
- Filter matches by league

## Future Improvements

- Live score updates
- League tables and team statistics
- Persistence layer using a database or real football API

