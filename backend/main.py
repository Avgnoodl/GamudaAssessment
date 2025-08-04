from fastapi import *
from model import *
from database import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
create_tables()
db_dependency = Annotated[Session, Depends(get_db)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

security = HTTPBearer()

