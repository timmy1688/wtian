from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr, field_validator, model_validator

from suanfa.jichu import jiazi_xuhao

BirthStr = constr(pattern=r'^\d{8}\s[0-2][0-9]$')  # 匹配 "YYYYMMDD HH"


class Gender(str, Enum):
    boy = "boy"
    girl = "girl"


class PaipanRequest(BaseModel):
    birth: BirthStr
    is_lunar: bool
    gender: Gender
    is_leap_month: bool = False


class PaipanResponse(BaseModel):
    gender: str  # "boy" 或 "girl"
    old_birth: str
    new_birth: str  # 公历生日
    bazi: list
    shishen: list
    wuxing: dict
    chart: Optional[dict] = None


class FenxiRequest(BaseModel):
    """
    推荐传 birth（可推算大运）；仅传 bazi 为兼容旧版前端，此时无法排大运。
    shishen / wuxing 不再采用，命盘一律由服务端重新推算。
    """
    gender: Gender
    demand: str = "综合运势"
    birth: Optional[BirthStr] = None
    is_lunar: bool = False
    is_leap_month: bool = False
    bazi: Optional[list[str]] = None
    shishen: Optional[list] = None
    wuxing: Optional[dict] = None

    @field_validator("bazi")
    @classmethod
    def check_bazi(cls, value):
        if value is None:
            return value
        if len(value) != 4:
            raise ValueError("bazi must contain four pillars")
        for ganzhi in value:
            if len(ganzhi) != 2:
                raise ValueError(f"invalid pillar: {ganzhi}")
            jiazi_xuhao(ganzhi)
        return value

    @model_validator(mode="after")
    def require_source(self):
        if not self.birth and not self.bazi:
            raise ValueError("either birth or bazi is required")
        return self
