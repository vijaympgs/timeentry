import google.generativeai as genai
API_KEY = "AIzaSyA0lR2CRUcFjVgL6JZ96rbo1gK6TK87VkY" 
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()

print("Chat with Gemini! Type 'exit' to quit.") 
while True: 
    user_input = input ("You:  ")
    if user_input.lower() == 'exit': 
        break
    response = chat.send_message(user_input)
    print("Gemini : ",response.text)
    

        
    
