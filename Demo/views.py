from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import base64
import json
import requests
import hashlib
import hmac
from django.http import HttpResponse
from Keys.keys import keys


def index(request):
    return render(request,'Demo/index.html')

def checkout(request):
    data = {
        "amount": int(float(request.POST['amount']) * 100),
        "currency": request.POST['currency'],
        "orderId": request.POST['orderId'],
        "customer": {
            "email": request.POST['email'],
            "firstName": request.POST['firstName'],
            "lastName": request.POST['lastName'],
            "phoneNumber": request.POST['phoneNumber'],
            "identityType": request.POST['identityType'],
            "identityCode": request.POST['identityCode'],
            "address": request.POST['address'],
            "country": request.POST['country'],
            "state": request.POST['state'],
            "city": request.POST['city'],
            "zipCode": request.POST['zipCode'],    
        }
    }

    url = 'https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment'
    auth = 'Basic ' + base64.b64encode(f"{keys["username"]}:{keys["password"]}".encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    if response_data['status'] != 'SUCCESS':
        raise Exception
    
    token = response_data['answer']['formToken']
    return render(request, 'Demo/checkout.html', {'token': token, 'publickey': keys['publickey']})

@csrf_exempt
def result(request):
    if not request.POST: raise Exception("no post data received!")

    if not checkHash(request.POST, keys["HMACSHA256"]) : raise Exception("Invalid signature")

    answer_json = json.loads( request.POST.get('kr-answer') )
    json_formatted = json.dumps(answer_json, indent=2)
    datos_json = json.dumps(request.POST, indent=4) 

    answer_json["orderDetails"]["orderTotalAmount"] = answer_json["orderDetails"]["orderTotalAmount"] / 100

    return render(request, 'Demo/result.html', {'answer': answer_json,"answer_json":json_formatted, 'dataPost': datos_json})

@csrf_exempt
def ipn(request):
    if not request.POST: raise Exception("no post data received!")

    if not checkHash(request.POST, keys["password"]) : raise Exception("Invalid signature")
    
    answer = json.loads( request.POST.get('kr-answer') ) 

    transaction = answer['transactions'][0]
    orderStatus = answer['orderStatus']
    orderId = answer['orderDetails']['orderId']
    transactionUuid = transaction['uuid']

    return HttpResponse(status=200, content=f"OK! OrderStatus is {orderStatus} ")

def checkHash(reqPost, key):
    answerHash = hmac.new(key.encode('utf-8'), reqPost.get("kr-answer").encode('utf-8'), hashlib.sha256).hexdigest()
    hash = reqPost.get('kr-hash')
    return hash == answerHash