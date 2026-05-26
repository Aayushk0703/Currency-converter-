from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI(title="Currency Converter")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

FRANKFURTER_URL = "https://api.frankfurter.app/latest"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/convert")
def convert_currency(
    amount: float = Query(..., gt=0),
    from_currency: str = Query(..., min_length=3, max_length=3),
    to_currency: str = Query(..., min_length=3, max_length=3),
    exchange_margin: float = 0,
    fixed_fee: float = 0,
    transaction_fee: float = 0,
):
    try:
        response = requests.get(
            FRANKFURTER_URL,
            params={"from": from_currency, "to": to_currency}
        )

        data = response.json()

        if "rates" not in data:
            raise HTTPException(status_code=400, detail="Invalid currency code")

        rate = data["rates"][to_currency]

        converted = amount * rate
        margin_cost = converted * (exchange_margin / 100)
        transaction_cost = converted * (transaction_fee / 100)

        final_amount = converted - margin_cost - transaction_cost - fixed_fee

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": round(rate, 4),
            "initial_amount": amount,
            "converted_amount": round(converted, 2),
            "exchange_margin_cost": round(margin_cost, 2),
            "transaction_fee_cost": round(transaction_cost, 2),
            "fixed_fee": fixed_fee,
            "final_amount": round(final_amount, 2),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))