from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class OrderCreate(BaseModel):
	customer: str = Field(min_length=1, max_length=100)
	item: str = Field(min_length=1, max_length=100)
	quantity: int = Field(gt=0)

class OrderResponse(BaseModel):
	id: int
	customer: str
	item: str
	quantity: int
	status: str
	create_at: datetime

	model_config = ConfigDict(from_attributes=True)
