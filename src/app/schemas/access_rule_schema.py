from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

RULE_WHITELIST = 0
RULE_BLACKLIST = 1


class AccessRuleCreate(BaseModel):
    plate: str
    rule_type: int  # 0 = WHITELIST, 1 = BLACKLIST
    description: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None

    @field_validator("rule_type")
    @classmethod
    def validate_rule_type(cls, value):
        if value in {RULE_WHITELIST, RULE_BLACKLIST}:
            return value

        raise ValueError("Invalid rule_type")

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, value):
        plate = value.strip().upper()
        if not plate:
            raise ValueError("Plate is required")

        return plate

    @model_validator(mode="after")
    def validate_time_range(self):
        if (
            self.valid_from is not None
            and self.valid_to is not None
            and self.valid_from > self.valid_to
        ):
            raise ValueError("valid_from must be before valid_to")

        return self


class AccessRuleUpdate(BaseModel):
    plate: str | None = None
    rule_type: int | None = None
    description: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    status: int | None = None

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, value):
        if value is None:
            return value

        plate = value.strip().upper()
        if not plate:
            raise ValueError("Plate is required")

        return plate

    @field_validator("rule_type")
    @classmethod
    def validate_rule_type(cls, value):
        if value is None or value in {RULE_WHITELIST, RULE_BLACKLIST}:
            return value

        raise ValueError("Invalid rule_type")

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is None or value in {1, 10}:
            return value

        raise ValueError("Invalid status")

    @model_validator(mode="after")
    def validate_time_range(self):
        if (
            self.valid_from is not None
            and self.valid_to is not None
            and self.valid_from > self.valid_to
        ):
            raise ValueError("valid_from must be before valid_to")

        return self


class AccessRuleResponse(AccessRuleCreate):
    id: int
    status: int
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
