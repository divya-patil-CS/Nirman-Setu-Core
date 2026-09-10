from app.services.chatbot_service import chat_step

profile = {}
history = []

messages = [
    "Namaste, mera naam Ramesh hai",
    "Meri age 45 hai aur janm tareekh 12 March 1980 hai",
    "Main kisan hoon",
    "Haan, meri ek beti hai, umar 15 saal",
    "Bas itna hi, koi aur nahi hai"
]

for msg in messages:
    result = chat_step(msg, profile, history, language="Hindi")
    print(f"User: {msg}")
    print(f"Bot: {result['reply']}")
    print(f"Profile: {result['profile']}")
    print(f"Complete: {result['profile_complete']}")
    print("---")
    profile = result["profile"]
    history = result["history"]