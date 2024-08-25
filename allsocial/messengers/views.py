from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from functions import *
import json

# Create your views here.
@csrf_exempt
def wa_webhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = '12345'
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token') 
        challenge = request.GET.get('hub.challenge')
        
        # Log the received query parameters for debugging
        print("Received query parameters:", request.GET)
        
        if mode is None or token is None or challenge is None:
            print("Missing query parameters:", request.GET)
            return JsonResponse({'error': 'Missing query parameters'}, status=400)
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            print("Token mismatch or mode not subscribe")
            return HttpResponse('error', status=403)
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'object' in data and 'entry' in data:
                if data['object'] == 'whatsapp_business_account':
                    try:
                        for entry in data['entry']:
                            phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                            phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']                        
                            profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                            whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']                        
                            fromId = entry['changes'][0]['value']['messages'][0]['from']                  
                            text = entry['changes'][0]['value']['messages'][0]['text']['body']                            
                            
                            phoneNumber = "+254715729081"
                            message = 'Your message: " {} " '.format(text)
                            sendWhatsappMessage(phoneNumber, message)                    
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        return HttpResponse('error', status=500)
            else:
                print("Invalid POST data:", data)
                return JsonResponse({'error': 'Invalid POST data'}, status=400)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        return HttpResponse('success', status=200)
    else:
        return HttpResponse('Invalid request method', status=405)
    