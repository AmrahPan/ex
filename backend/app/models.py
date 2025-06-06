from typing import Optional
from sqlmodel import SQLModel, Field

class GlobalSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    guest_price: float = 400
    semi_price: float = 200
    food_cost: float = 140
    agg_fee_pct: float = 0.33
    royalty_pct: float = 0.10
    fixed_cost: float = 400_000

class KitchenBase(SQLModel):
    name: str
    orders_day: int

class Kitchen(KitchenBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class KitchenRead(KitchenBase):
    id: int
    profit_month: Optional[float] = None
    profit_portion: Optional[float] = None

class Dashboard(SQLModel):
    global_settings: GlobalSettings
    kitchens: list[KitchenRead]
    revenue_ceh: float
    cogs_ceh: float
    ebitda_ceh: float
