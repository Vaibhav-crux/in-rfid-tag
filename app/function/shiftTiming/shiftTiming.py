# app/function/shiftTiming/shiftTiming.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
from datetime import datetime
from app.config.db_config import engine
from app.model.shiftTiming import ShiftTiming

def create_session():
    """Create a new database session."""
    session = sessionmaker(bind=engine)
    return session()

def get_current_shift():
    """Fetches the shift name based on the current time."""
    current_time_obj = datetime.now().time()

    session = create_session()
    try:
        # Fetch the shift that matches the current time
        shift = session.query(ShiftTiming).filter(
            and_(
                ShiftTiming.from_time <= current_time_obj,
                ShiftTiming.to_time >= current_time_obj
            )
        ).first()

        # Handle shifts that span midnight (e.g., C Shift)
        if not shift:
            shift = session.query(ShiftTiming).filter(
                and_(
                    ShiftTiming.from_time > ShiftTiming.to_time,  # Indicates spanning midnight
                    or_(
                        ShiftTiming.from_time <= current_time_obj,
                        ShiftTiming.to_time >= current_time_obj
                    )
                )
            ).first()

        return shift.shift_name if shift else "No Shift Found"
    finally:
        session.close()
