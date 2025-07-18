import os
import json
import requests
import google.generativeai as genai
from django.db import transaction
from dotenv import load_dotenv
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from PyPDF2 import PdfReader
from docx import Document
from django.views.decorators.http import require_POST
from django.core.files.uploadedfile import UploadedFile
load_dotenv()

STUDYBUDDY_SYSTEM_PROMPT = """
# StudyBuddy - Your Learning Assistant

**Specialized Subjects:**
- **STEM** (Math, Physics, Programming)
- **Humanities** (History, Literature, Philosophy)
- **Languages** (Grammar, Writing, Vocabulary)

**Teaching Methodology:**
1. **Break down** complex topics into steps
2. Provide **real-world examples**
3. Adjust explanations to the user's level
4. Use **clear formatting**:
   - Headers (`##`) for sections
   - **Bold** for key terms
   - Bullets for steps

**Example Response Style:**
## Quadratic Equations
To solve **ax² + bx + c = 0**:
1. Identify coefficients (a=__, b=__, c=__)
2. Apply the quadratic formula:  
   `x = [-b ± √(b²-4ac)] / 2a`
3. *Practice example*: Solve 2x² - 4x - 6 = 0

What concept would you like to explore?"""

@csrf_exempt
@require_POST
def file_upload_api(request):
    uploaded_file: UploadedFile = request.FILES.get("file")
    session_id = request.POST.get("session_id", "")

    if not uploaded_file:
        return JsonResponse({'response': "No file was uploaded."}, status=400)

    try:
        # Determine file type and extract content
        content = ""
        if uploaded_file.name.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif uploaded_file.name.endswith('.docx'):
            doc = Document(uploaded_file)
            content = "\n".join([para.text for para in doc.paragraphs])
        elif uploaded_file.name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
        else:
            return JsonResponse({'response': "Unsupported file type."}, status=415)

        if not content.strip():
            return JsonResponse({'response': "The file is empty or could not be read."})

        # Send to AI
        ai_response = generate_google_gemini_response(f"Please summarize or explain this content:\n\n{content[:5000]}")

        # Optionally log this
        if request.user.is_authenticated:
            save_chat_message(
                user=request.user,
                session_id=session_id,
                user_message=f"[Uploaded file: {uploaded_file.name}]",
                ai_response=ai_response
            )

        return JsonResponse({'response': ai_response})

    except Exception as e:
        print(f"[File Upload Error] {str(e)}")
        return JsonResponse({'response': f"An error occurred while processing the file."}, status=500)
    
@transaction.atomic
def save_chat_message(user, session_id, user_message, ai_response):
    """Enhanced with validation and logging"""
    try:
        if not user or not user.is_authenticated:
            raise ValueError("Invalid user")
            
        if not user_message or not ai_response:
            raise ValueError("Empty message content")
            
        return ChatMessage.objects.create(
            user=user,
            session_id=session_id[:1000],
            user_message=user_message[:10000],
            ai_response=ai_response[:10000]
        )
    except Exception as e:
        print(f"Database Error: {str(e)}")
        raise

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            print("\n=== New Request Received ===")
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id', '')
            
            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            print("Attempting OpenRouter connection...")
            ai_response = generate_google_gemini_response(user_message)
            
            if request.user.is_authenticated:
                save_chat_message(
                    user=request.user,
                    session_id=session_id,
                    user_message=user_message,
                    ai_response=ai_response
                )

            return JsonResponse({
                'response': ai_response, 
                'status': 'success',
                'char_count': len(ai_response)
            })
            
        except Exception as e:
            print(f"!!! TOP-LEVEL ERROR: {str(e)}")
            return JsonResponse({
                'error': str(e) if settings.DEBUG else "Request failed",
                'status': 'error'
            }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def generate_google_gemini_response(message):
    try:
        # Configure the client
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Use Gemini 1.5 Flash for faster responses (or Pro for more accuracy)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Send the prompt with system instruction
        convo = model.start_chat(history=[])
        prompt = f"{STUDYBUDDY_SYSTEM_PROMPT}\n\nUser: {message}"
        response = convo.send_message(prompt)

        # Return the generated content
        response_text = response.text.strip()
        print(f"📝 Gemini generated {len(response_text)} characters")
        return response_text

    except Exception as e:
        print(f"⚠️ Gemini API Error: {str(e)}")
        return "Sorry, I encountered a problem connecting to the AI service. Try again shortly."
    
def chat_page(request):
    return render(request, "chatbot/chat.html")

@login_required
def chat_history(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, "chatbot/history.html", {"messages": messages})