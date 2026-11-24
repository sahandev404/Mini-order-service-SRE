import logging
import time
from urllib import request, response

from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, engine
from app.models import Order
from app.schemas import OrderCreate, OrderResponse
from app.logging_config import setup_logging
from app.metrics import HTTP_REQUESTS, HTTP_ERRORS, HTTP_REQUEST_DURATION, ORDERS_CREATED

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="Mini Order Service")
app.mount("/static", StaticFiles(directory="static"), name="static")

#Enable Promethues metrics
Instrumentator().instrument(app).expose(app)

# Expose metrics endpoint for Prometheus
@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(
		content=generate_latest(),
		media_type=CONTENT_TYPE_LATEST
	)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico", media_type="image/x-icon")

@app.get("/test-error")
async def test_error():
	raise ValueError("This is a test exception")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	logger.error(
		"Unhandled exception on %s %s",
		request.method,
		request.url.path,
		exc_info=(type(exc), exc, exc.__traceback__)
	)
	return JSONResponse(
		status_code=500,
		content={"detail": "Internal server error"}
	)

@app.middleware("http")
async def collect_metrics(request: Request, call_next):
	start_time = time.perf_counter()
	logger.info(
		"Incoming request: %s %s",
        request.method,
        request.url.path
	)
	try:
		response = await call_next(request)
		duration = time.perf_counter() - start_time

		logger.info(
					"Request completed: %s %s | Status: %s | Duration: %.3fs",
					request.method,
					request.url.path,
					response.status_code,
					duration
				)
		
		status_code = response.status_code
		method = request.method
		HTTP_REQUESTS.labels(
			method=method,
			status_code=str(status_code)
		).inc()
		if status_code >= 400:
			HTTP_ERRORS.labels(
    			method=method,
    			status_code=str(status_code)
            ).inc()
		return response

	except Exception:
		duration = time.perf_counter() - start_time
		logger.exception(
			"Request failed: %s %s | Duration: %.3fs",
			request.method,
			request.url.path,
			duration
		)
		method = request.method
		HTTP_REQUESTS.labels(
			method=method,
			status_code="500"
		).inc()
		HTTP_ERRORS.labels(
			method=method,
			status_code="500"
    	).inc()
		raise
	finally:
		HTTP_REQUEST_DURATION.labels(
			method=request.method
		).observe(time.perf_counter() - start_time)

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
			status_code=503,
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

	ORDERS_CREATED.inc()

	return new_order

# 4. Retrieve all orders
@app.get("/orders", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
	orders = db.query(Order).order_by(Order.id.desc()).all()

	return orders

# # 5. High latency endpoint for testing
# @app.get("/slow")
# async def slow_endpoint():
# 	await time.sleep(5)  # Simulate a slow response
# 	return {"message": "This is a slow endpoint."}

# # 6. Heavy load endpoint for testing
# @app.get("/cpu-heavy")
# def cpu_heavy():
#     result = 0
#     for i in range(50_000_000):
#         result += i * i
#     return {"result": result}

# # 7. Simulate memory consumption
# memory_storage = []

# @app.get("/memory-heavy")
# def memory_heavy():
# 	memory_storage.append(bytearray(10*1024*1024))
# 	return {
# 		"message": "Allocated 10 MB",
# 		"total_allocations": len(memory_storage)
# 	}
