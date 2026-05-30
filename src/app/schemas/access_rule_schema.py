from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccessRuleCreate(BaseModel):
    plate: str
    rule_type: str  # WHITELIST | BLACKLIST
    description: str | None = None

class AccessRuleResponse(AccessRuleCreate):
    id: int
    status: int
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
