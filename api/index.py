from fastapi import FastAPI, Request
import stripe
import os

app = FastAPI()

# Vercel এ এই কি (Key) সেট করতে হবে
stripe.api_key = os.getenv("STRIPE_KEY")

@app.get("/")
def home():
    return {"status": "API is running"}

@app.post("/check")
async def check_card(request: Request):
    data = await request.json()
    try:
        # কার্ড ভ্যালিডেশন চেক
        stripe.Token.create(
            card={
                "number": data.get('number'),
                "exp_month": data.get('month'),
                "exp_year": data.get('year'),
                "cvc": data.get('cvc'),
            },
        )
        return {"result": "LIVE", "message": "Card is valid"}
    except stripe.error.CardError as e:
        return {"result": "DEAD", "message": e.user_message}
    except Exception as e:
        return {"result": "ERROR", "message": str(e)}
