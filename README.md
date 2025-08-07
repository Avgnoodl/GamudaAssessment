# Football Match Tracker — Full Documentation

> A single Markdown file containing **all** project information: setup, architecture, directory map, and code excerpts for the Gamuda take‑home challenge.

---

## 1 Project Overview

### 1.1 App Summary

Football Match Tracker is a mini full‑stack application that **simulates** a set of ongoing football matches and presents them through a clean, responsive dashboard.  Every 3 seconds the frontend polls the API; the backend may inject a new event (50 % chance per live match) and immediately persists it to PostgreSQL, so multiple browser tabs share the same evolving world in real time.

Key ideas demonstrated:

- **Stateless simulation** – no cron jobs required; each request can mutate data and return an up‑to‑date snapshot.
- **Reactive UI** – Pinia store streams fresh JSON into Vuetify cards, which animate when scores change.
- **UTC‑aware time handling** – matches can be anywhere in the world yet tick reliably.

### 1.2 Main Pages & What They Do

| Page / Route                                          | Purpose                                                                                                      | Notable Components                     |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| **Dashboard** (`/`)                                   | Landing page listing *Live*, *Scheduled*, and *Finished* matches.  Filters by league and kickoff window.     | `MatchCard.vue`, `DateFilter.vue`      |
| **Match Detail** (`/match/:id`)                       | Timeline of **all** events (goals, cards, subs) for a single match.  Auto‑scrolls to newest event on update. | `EventTimeline.vue`                    |
| **League Table** (`/league-table`) *(optional bonus)* | Ranks teams by points & goal difference.  Recomputes on every goal.                                          | `LeagueTable.vue`                      |
| **Team Stats** (`/team-stats`) *(optional bonus)*     | Grid of cards showing P W D L GF GA Pts for each team across the mock season.                                | `TeamStats.vue`                        |
| **About / Help**                                      | Quick explanation of the mock data, keyboard shortcuts, and links to the GitHub repo / live demo.            | Markdown‑rendered via `vite-plugin-md` |



---
### 2 Folder Structure
GAMUDAASSESSMENT/
├── backend/                      # Python FastAPI backend
│   ├── database.py              # DB engine, session, and table creation helpers
│   ├── main.py                  # FastAPI app with endpoints + live match simulator
│   ├── models.py                # SQLAlchemy models: Match + MatchEvent
│   ├── seed_db.py               # Seeds a mock season across 5 major leagues
│   └── requirements.txt         # Backend dependencies
│
├── vuetify-project/             # Vue 3 + Vuetify frontend
│   └── src/
│       ├── assets/              # Fonts, icons, and static images
│
│       ├── components/          # Shared UI elements used across multiple pages
│       │   ├── Header.vue               # Top navbar with logo + title
│       │   ├── Sidebar.vue              # Collapsible navigation drawer
│       │   ├── DateFilter.vue           # Kickoff date selector using <v-date-picker>
│       │   ├── AppFooter.vue            # Optional footer (currently unused)
│       │   └── HelloWorld.vue           # Default template (can be removed)
│
│       ├── layouts/             # Page-level layout wrappers
│       │   └── default.vue              # Base layout with header + sidebar
│
│       ├── pages/               # All routed pages (auto-imported by `vue-router/auto`)
│       │   ├── match/
│       │   │   └── [id].vue             # Match detail page showing event timeline
│       │   ├── dashboard.vue           # Main homepage with match listing + filters
│       │   ├── league-table.vue        # League standings (auto-sorted by points)
│       │   ├── team-stats.vue          # Team cards with W/D/L/Points + view matches
│       │   ├── HelpPage.vue            # Help + keyboard shortcuts
│       │   ├── AboutPage.vue           # Explanation of app scope and mock data
│       │   └── index.vue               # Renders <dashboard.vue> inside hero layout
│
│       ├── plugins/             # Vuetify config, can be expanded for global plugins
│
│       ├── router/              # Router index for Vite auto routes
│
│       ├── stores/              # Pinia stores for global state
│       │   ├── useMatches.ts           # Match polling, storage, and refresh logic
│       │   ├── index.ts                # Pinia setup (if needed later)
│       │   └── app.ts                  # App-wide UI state (e.g., sidebar toggle)
│
│       ├── styles/              # Global style overrides
│       │   └── override-font.css       # CSS for Roboto/Material Icons fallback
│
│       └── app.ts               # App bootstrap + Vuetify setup
│
├── screenshots/                 # Screenshots used in README or documentation
├── README.md                    # Full technical + usage documentation
└── .gitignore                   # Excludes node_modules, .env, etc.

---

## 3 Setup & Installation

### 3.1.1 Backend - Pg admin4 server setup
If you’d like a GUI for browsing tables while the simulator runs:
Install pgAdmin 4 – https://www.pgadmin.org/download/ (macOS, Windows, or Linux).

Register a New Server
Name: Local Postgres
Host: localhost  •  Port: 5432
Username: postgres  •  Password: password.
After the server has been registered, right click on the server and create a new database named "football_db".

### 3.1.2 Backend - Python

```bash
python -m venv env && source env/bin/activate       # create venv
cd backend                                          # change directory into backend
pip install -r requirements.txt                     # install deps
python seed_db.py                                   # seed data into database (postgresql server must be running before this code is run)
uvicorn backend.main:app --reload                   # API → localhost:8000
```

> **requirements.txt**
>
> ```
> fastapi[all]
> uvicorn[standard]
> SQLAlchemy>=2.0
> psycopg2-binary
> python-dotenv
> apscheduler
> ```

### 3.2 Frontend (Node)
Open a new terminal (separate from the previous)
Make sure Node.js is already installed on machine

```bash
cd vuetify-project              # change directory to frontend, which is stored under vuetify-project
npm install                     # installs axios, vue, vuetify, pinia, vite
npm run dev                     # Vite → http://localhost:3000
```

Vite proxy forwards `/api` requests to `localhost:8000` so CORS isn’t an issue in dev.

---

## 4 System Design

### 4.1 Component Layers

| Layer          | Tech                | Responsibility                                                     |
| -------------- | ------------------- | ------------------------------------------------------------------ |
| **UI**         | Vue 3, Vuetify 3    | Render match cards, filter UI, minute ticker, expandable goal list |
| **State**      | Pinia + Axios       | Poll `/api/matches` every **3 s**, store reactive array            |
| **API**        | FastAPI             | Serialise matches, call `maybe_add_event()` for live matches       |
| **Simulation** | Python + SQLAlchemy | 50 % chance per poll to create goal/yellow/sub, auto‑finish at 90′ |
| **DB**         | PostgreSQL 15       | Tables `matches` (1) → `match_events` (∞)                          |

### 4.2 Data‑flow Diagram

```
[Vue SPA]  --(poll 3 s)-->  [/api/matches]  --(SQL)-->  [PostgreSQL]
            <--------------   JSON list   <-------------
```

*Optionally enable APScheduler to push events every second regardless of polling.*

---

## 5 Key Code Snippets

### 5.1 SQLAlchemy Models  (`backend/models.py`)

```python
class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    league = Column(String, nullable=False)
    home_team = Column(String)
    away_team = Column(String)
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    kickoff_time = Column(DateTime(timezone=True))
    status = Column(String, default="live")
    home_players = Column(ARRAY(String))
    away_players = Column(ARRAY(String))
    events = relationship("MatchEvent", back_populates="match", cascade="all, delete-orphan")
```

### 5.2 Simulator Snippet (`backend/main.py`)

```python
EVENT_CHANCE = 0.50  # 50 %

def maybe_add_event(match: DBMatch, db: Session):
    if match.status != "live" or random.random() > EVENT_CHANCE:
        return
    evt = DBMatchEvent(... minute=current_minute(match.kickoff_time))
    match.events.append(evt)      # cascade write
    if evt.type == "goal":
        match.home_score += 1 if evt.team == match.home_team else 0
        match.away_score += 1 if evt.team == match.away_team else 0
```

### 5.3 Pinia Store (`frontend/src/stores/useMatches.ts`)

```ts
export const useMatches = defineStore("matches", {
  state: () => ({ matches: [] as any[] }),
  actions: {
    async fetchAll () {
      const { data } = await axios.get("/api/matches")
      this.matches = data
    },
    startPolling () {
      this.fetchAll()
      setInterval(this.fetchAll, 3000)   // 3 s
    }
  }
})
```

---

## 6 Screenshots
 - screenshots of the application are stored in the screenshots folder

## 7 Short Reflection (Next Features)
Current app limitations:
- Mock Data Feed
- Matches do not auto update
- No Clear UI when update occurs
- League table and Team Stats page have basically the same information, but repackaged differently

While there wasn't much time to make the app, I feel like the following improvements could be made:

- **Real‑time feed** – swap simulator for real apis like API‑Football (not implemented due to time-constraints, and free-plans' low api rate limt).
- **WebSockets push** – The website could be much smoother if Websockets were used instead of polling with axios and hardcoding random server events.
- **League table auto‑update** – recompute points live on each goal.
- **Match page auto-update** - when an update occurs in the db, the match page should automatically update too.
- **Light theme / theming** – automatic via Vuetify’s presets; improve accessibility. Currently only on Dark Mode.
- **Fleshing out Team Stats page** adding more data about each team so that team-stats could have more team-specific data, rather than it's current general form

---

## 8 License

MIT © 2025

