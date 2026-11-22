from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, engine
from app.models import Order
from app.schemas import OrderCreate, OrderResponse

app = FastAPI(title="Mini Order Service")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico", media_type="image/x-icon")

# 1. Application liveness check
@app.get("/")
def home():
    return {"message": "Mini Order Service is running!"}

@app.get("/health")
def health_check():
    return {"status": "alive"}

# 2 . Database readiness check
@app.get("/ready")
def readiness_check():
	try:
		with engine.connect() as connection:
			connection.execute(text("SELECT 1"))

		return {
			"status": "ready",
			"database": "connected"
		}
	
	except SQLAlchemyError:
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNVAILABLE,
			detail={
				"status": "not_ready",
				"database": "unavailable"
			}
		)

# 3. Create an order
@app.post(
	"/orders",
	response_model=OrderResponse,
	status_code=status.HTTP_201_CREATED
)
def create_order(
	order: OrderCreate,
	db: Session = Depends(get_db)
):
	new_order = Order(
		customer=order.customer,
		item=order.item,
		quantity=order.quantity
	)

	db.add(new_order)
	db.commit()
	db.refresh(new_order)

	return new_order

# 4. Retrieve all orders
@app.get("/orders", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
	orders = db.query(Order).order_by(Order.id.desc()).all()

	return orders
