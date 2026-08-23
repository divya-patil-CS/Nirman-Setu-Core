from app.services.chatbot_service import chat_step

profile = {}
result = chat_step("Namaste, mera naam Ramesh hai", profile, language="Hindi")
print(result)