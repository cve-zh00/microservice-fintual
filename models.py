from pydantic import BaseModel, Field, field_validator

class OptimizeParams(BaseModel):
    risk_level: float = Field(..., alias="risk_level")
    max_weight: float = Field(..., alias="max_weight")

    @field_validator('risk_level', 'max_weight')
    def validate_name(cls, v):
        if v <= 0 or v >= 100:
            raise ValueError("Value can be higher than 0 and lower than 1")
        return v
