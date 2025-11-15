from fastapi import Depends
from typing import Annotated
from ..db.db import get_session ,AsyncSession




db_dependency = Annotated[AsyncSession, Depends(get_session)]





