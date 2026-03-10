# HelloMeds 💊 - Server Setup Guide

## Prerequisites
- Python 3.x
- VS Code
- Twilio Account
- Google AI Studio Account

---

## 1. Clone & Navigate to Server Directory
```bash
cd server
```

## 2. Create Virtual Environment
```bash
python3 -m venv .venv
```

## 3. Activate Virtual Environment
```bash
source .venv/bin/activate
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 5. Environment Variables
Create a `.env` file in the server directory:
```env
GOOGLE_API_KEY="your_google_api_key"
TWILIO_ACCOUNT_SID="your_twilio_account_sid"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
TWILIO_PHONE_NUMBER="your_twilio_phone_number"
PORT_URL="your_forwarded_address"
PORT=8080
```

## 6. Run Server
```bash
python main.py
```

---

## 7. VS Code Port Forwarding
1. Open **PORTS** tab at the bottom of VS Code
2. Add port `8080`
3. Right click → **Port Visibility** → **Public**
4. Copy the forwarded address
5. Update `.env` file — without `https://`
```env
PORT_URL="your-forwarded-address.uks1.devtunnels.ms"
```
6. Restart server
```bash
python main.py
```

---

## 8. Twilio Configuration
1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**
3. Click your phone number
4. **Routing** → `Go to other configurations` → Select **Europe (IE1)**
5. Under **Voice Configuration**:
   - A call comes in: `Webhook`
   - URL: `https://your-forwarded-address/twiml`
   - HTTP: `HTTP POST`
6. Click **Save**

---

## 9. Test
```
https://your-forwarded-address/make-call
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port Forwarding not working | Make sure Visibility is set to **Public** |
| No sound on call | Check Twilio Routing is set to **Europe (IE1)** |
| Gemini quota exceeded | Generate a new API key at [Google AI Studio](https://aistudio.google.com/app/apikey) |
| Module not found | Run `pip install -r requirements.txt` inside `.venv` |