from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import base64
import json
import requests
import hashlib
import hmac
from django.http import HttpResponse
from Keys.keys import keys

def home(request):
    context = {
    }
    return render(request,'home.html', context)

def formToken(request):
    username = keys["username"]
    password = keys["password"]
    publickey = keys['publickey']

    url = 'https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment'
    auth = 'Basic ' + base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')

    data = {
        "amount": 180,
        "currency": "PEN",
        "orderId": "myOrderId-999999",
        "customer": {
            "email": "sample@example.com"
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    if response_data['status'] == 'SUCCESS':
        token = response_data['answer']['formToken']
        return render(request, 'Demo/formtoken.html', {'token': token, 'publickey': publickey})
    else:
        serialized_data = json.dumps(response_data, indent=4)
        return render(request, 'Demo/error.html', {'serialized_data': serialized_data})

@csrf_exempt
def paidResult(request):
    answer = request.POST.get('kr-answer')
    hash = request.POST.get('kr-hash')

    hash_object = hmac.new(keys['HMACSHA256'].encode('utf-8'), answer.encode('utf-8'), hashlib.sha256)
    answerHash = hash_object.hexdigest()

    answer_json = json.loads(answer)
    orderDetails = answer_json.get('orderDetails')

    if hash == answerHash:
        return render(request, 'Demo/result.html', {'response': answer_json.get('orderStatus'), 'orderTotalAmount': orderDetails.get('orderTotalAmount'), 'orderId': orderDetails.get('orderId')})
    else:
        return render(request, 'Demo/result.html', {'response': 'Error en el pago'})

@csrf_exempt
def ipn(request):
    answer = request.POST.get('kr-answer')
    hash = request.POST.get('kr-hash')

    hash_object = hmac.new(keys['password'].encode('utf-8'), answer.encode('utf-8'), hashlib.sha256)
    answerHash = hash_object.hexdigest()

    answer_json = json.loads(answer)
    print('IPN')
    print(answer_json)
    print('Codigo Hash: ' + answerHash)

    if hash == answerHash:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)