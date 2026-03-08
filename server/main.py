import os
import json
import uvicorn
from google import genai
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
PORT = int(os.getenv("PORT", "8080"))
DOMAIN = os.getenv("NGROK_URL")
if not DOMAIN:
    raise ValueError("NGROK_URL environment variable not set.")
WS_URL = f"wss://{DOMAIN}/ws"

WELCOME_GREETING = "Hi, HelloMeds calling!"

SYSTEM_PROMPT = """You are HelloMeds, a warm and friendly medication reminder assistant. 
You are calling a patient to remind them to take their medication.
This conversation is happening over a phone call, so your responses will be spoken aloud.

Your personality:
- Warm, caring, and human-feeling — like a call from a trusted friend
- Simple and clear — many users may be elderly or less tech-savvy
- Encouraging and supportive — never clinical, cold, or robotic
- Patient and calm — never rushed or overwhelming

Your role in this call:
- Greet the patient by name warmly
- Remind them which medication to take and how much
- Ask them to confirm whether they have taken it
- Respond kindly based on their answer
- End the call on a positive, encouraging note

Please follow these rules:
1. Keep responses short — one or two sentences only. This is a phone call, not a conversation.
2. Spell out all numbers (e.g., say 'two tablets' not '2 tablets').
3. Do not use any special characters, bullet points, asterisks, hyphens, or emojis.
4. Always sound warm and personal — the patient should feel looked after, not alarmed.
5. Use simple, everyday language — avoid any medical jargon.
6. If the patient confirms they have taken their medication, praise them warmly and wish them a good day, then end the call.
7. If the patient has not taken their medication yet, gently encourage them to do so now and remind them it helps them stay healthy.
8. If the patient seems confused or gives an unclear response, kindly and patiently ask them to simply say yes if they have taken their medication.
9. If the patient seems lonely or wants to chat, be kind but gently guide the conversation back to the medication check, don't say machine like answer such as "Sorry, I had trouble responding.."
10. Never give any medical advice or change any instructions — your only job is to remind, confirm, and encourage, like a caring friend checking in.

The conversation should follow this flow:
Step one: Greet the patient by name and introduce yourself as HelloMeds.
Step two: Tell them which medication to take and remind them of the dose.
Step three: Ask if they have taken it yet.
Step four: Respond warmly based on their answer.
Step five: Say a friendly goodbye and end the call.

Remember: 
You are not a doctor. Never give any medical advice or change any instructions.
Your only job is to remind, confirm, and encourage — like a caring friend checking in."""

# --- Twilio 초기화 ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# --- Gemini 초기화 ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

# --- 세션 저장소 ---
sessions = {}
pending_calls = {}  # { to_number: { patient_name, medication, dose } }

# --- FastAPI 앱 ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request 모델 ---
class CallRequest(BaseModel):
    to_number: str
    patient_name: str
    medication: str
    dose: str


# --- Gemini 응답 ---
def gemini_response(chat_session, user_prompt):
    try:
        response = chat_session.send_message(user_prompt)
        print(f"✅ Gemini 응답 성공: {response.text}")
        return response.text
    except Exception as e:
        print(f"❌ Gemini 응답 실패: {e}")
        return "Sorry, I had trouble responding."


# --- TwiML 엔드포인트 ---
@app.api_route("/twiml", methods=["GET", "POST"])
async def twiml_endpoint(request: Request):
    print("✅ /twiml 호출됨!")
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
    <Connect>
    <ConversationRelay url="{WS_URL}" welcomeGreeting="{WELCOME_GREETING}" ttsProvider="Google" voice="en-US-Journey-F" />
    </Connect>
    </Response>"""
    return Response(content=xml_response, media_type="text/xml")


# --- 전화 걸기 엔드포인트 ---
@app.post("/call")
async def make_call(request: CallRequest):
    try:
        # 환자 정보 저장
        pending_calls[request.to_number] = {
            "patient_name": request.patient_name,
            "medication": request.medication,
            "dose": request.dose,
        }

        call = twilio_client.calls.create(
            to=request.to_number,
            from_=TWILIO_PHONE_NUMBER,
            url=f"https://{DOMAIN}/twiml",
        )
        print(f"📞 전화 걸기 성공! call_sid: {call.sid} to: {request.to_number}")
        return {"success": True, "call_sid": call.sid}

    except Exception as e:
        print(f"❌ 전화 걸기 실패: {e}")
        return {"success": False, "error": str(e)}


# --- 테스트 페이지 ---
@app.get("/make-call")
async def make_call_page():
    html = """
    <html>
    <body>
        <h2>HelloMeds - 전화 테스트</h2>
        <input id="phone" placeholder="+447719143101" style="width:300px;padding:8px"/><br/><br/>
        <input id="name" placeholder="Patient Name" style="width:300px;padding:8px"/><br/><br/>
        <input id="med" placeholder="Medication" style="width:300px;padding:8px"/><br/><br/>
        <input id="dose" placeholder="Dose e.g. two tablets" style="width:300px;padding:8px"/><br/><br/>
        <button onclick="makeCall()" style="padding:10px 20px;font-size:16px">📞 전화 걸기</button>
        <p id="result"></p>
        <script>
            async function makeCall() {
                document.getElementById('result').innerText = '전화 연결 중...';
                const res = await fetch('/call', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        to_number: document.getElementById('phone').value,
                        patient_name: document.getElementById('name').value,
                        medication: document.getElementById('med').value,
                        dose: document.getElementById('dose').value
                    })
                });
                const data = await res.json();
                document.getElementById('result').innerText = data.success
                    ? '✅ 전화 연결 중입니다!'
                    : '❌ 실패: ' + data.error;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


# --- WebSocket 엔드포인트 ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket 연결됨!")
    call_sid = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "setup":
                call_sid = message["callSid"]
                to_number = message.get("to")
                print(f"✅ Setup 완료 - call_sid: {call_sid}, to: {to_number}")

                # 환자 정보 가져오기
                user_info = pending_calls.get(to_number, {})
                patient_name = user_info.get("patient_name", "there")
                medication = user_info.get("medication", "your medication")
                dose = user_info.get("dose", "")
                print(f"👤 환자 정보: {patient_name}, {medication}, {dose}")

                # 개인화 프롬프트
                personalized_prompt = f"""{SYSTEM_PROMPT}

Current patient information for this call:
Patient name: {patient_name}
Medication: {medication}
Dose: {dose}

Start the conversation by greeting {patient_name} and reminding them to take {dose} {medication}."""

                try:
                    sessions[call_sid] = gemini_client.chats.create(
                        model="gemini-2.0-flash",
                        config={"system_instruction": personalized_prompt}
                    )
                    print(f"✅ Gemini 세션 생성 성공 - {patient_name}의 {medication} 알림")

                    # pending_calls 정리
                    if to_number in pending_calls:
                        del pending_calls[to_number]

                except Exception as e:
                    print(f"❌ Gemini 세션 생성 실패: {e}")

            elif message["type"] == "prompt":
                user_prompt = message.get("voicePrompt", "")
                print(f"🎤 사용자 발화: '{user_prompt}'")

                if not call_sid or call_sid not in sessions:
                    print(f"❌ 세션 없음! call_sid: {call_sid}")
                    continue

                response_text = gemini_response(sessions[call_sid], user_prompt)
                payload = json.dumps({"type": "text", "token": response_text, "last": True})
                print(f"📤 Twilio로 전송: {payload}")
                await websocket.send_text(payload)

            elif message["type"] == "interrupt":
                print(f"⚡ 인터럽트 발생 - call_sid: {call_sid}")

            else:
                print(f"❓ 알 수 없는 메시지 타입: {message['type']}")

    except WebSocketDisconnect:
        print(f"🔌 WebSocket 종료 - call_sid: {call_sid}")
        if call_sid and call_sid in sessions:
            sessions.pop(call_sid)

    except Exception as e:
        print(f"❌ 예상치 못한 에러: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print(f"🚀 서버 시작 - 포트: {PORT}")
    print(f"🔗 WebSocket URL: {WS_URL}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="debug")