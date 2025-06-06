from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from .models import GlobalSettings, Kitchen, KitchenRead, Dashboard
from .database import engine, init_db

init_db()

app = FastAPI()

# helper calculation

def calculate_dashboard():
    with Session(engine) as session:
        gs = session.get(GlobalSettings, 1)
        kitchens = session.exec(select(Kitchen)).all()
        portions_month = sum(k.orders_day for k in kitchens) * 30
        revenue_ceh = gs.semi_price * portions_month
        cogs_ceh = gs.food_cost * portions_month
        margin_ceh = revenue_ceh - cogs_ceh
        ebitda_ceh = margin_ceh - gs.fixed_cost
        kitchen_reads = []
        for k in kitchens:
            gmv = gs.guest_price * k.orders_day * 30
            net = gmv * (1 - gs.agg_fee_pct)
            royalty = net * gs.royalty_pct
            profit = net - gs.semi_price * k.orders_day * 30 - royalty
            p_portion = profit / (k.orders_day * 30) if k.orders_day else 0
            kitchen_reads.append(KitchenRead(id=k.id, name=k.name, orders_day=k.orders_day,
                                            profit_month=profit, profit_portion=p_portion))
        return Dashboard(global_settings=gs, kitchens=kitchen_reads,
                         revenue_ceh=revenue_ceh, cogs_ceh=cogs_ceh, ebitda_ceh=ebitda_ceh)

@app.get('/dashboard', response_model=Dashboard)
def get_dashboard():
    return calculate_dashboard()

@app.put('/global', response_model=GlobalSettings)
def update_global(settings: GlobalSettings):
    with Session(engine) as session:
        gs = session.get(GlobalSettings, 1)
        if not gs:
            gs = GlobalSettings(id=1)
            session.add(gs)
        for field, value in settings.dict(exclude_unset=True).items():
            setattr(gs, field, value)
        session.commit()
        session.refresh(gs)
        return gs

@app.post('/kitchen', response_model=Kitchen)
def create_kitchen(kitchen: Kitchen):
    with Session(engine) as session:
        session.add(kitchen)
        session.commit()
        session.refresh(kitchen)
        return kitchen

@app.put('/kitchen/{kid}', response_model=Kitchen)
def update_kitchen(kid: int, kitchen: Kitchen):
    with Session(engine) as session:
        dbk = session.get(Kitchen, kid)
        if not dbk:
            raise HTTPException(status_code=404, detail='Not found')
        dbk.name = kitchen.name
        dbk.orders_day = kitchen.orders_day
        session.commit()
        session.refresh(dbk)
        return dbk

@app.delete('/kitchen/{kid}')
def delete_kitchen(kid: int):
    with Session(engine) as session:
        dbk = session.get(Kitchen, kid)
        if not dbk:
            raise HTTPException(status_code=404, detail='Not found')
        session.delete(dbk)
        session.commit()
        return {'ok': True}
