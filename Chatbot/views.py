from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from .models import Chat
from django.utils import timezone

openai_api_key = 'OPEN_API_KEY'  # Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    chats = Chat.objects.all()

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat( message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'Chatbot/chatbot.html', {'chats': chats})
