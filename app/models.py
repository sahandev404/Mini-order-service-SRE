from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class Order(Base):
	__tablename__ = "orders"

	id = Column(Integer, primary_key=True, index=True)
	customer = Column(String(100), nullable=False)
	item = Column(String(100), nullable=False)
	quantity = Column(Integer, nullable=False)
	status = Column(String(50), default="pending")
	create_at = Column(
		DateTime(timezone=True),
		server_default=func.now()
	)
