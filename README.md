<p align="center">
  <img src="https://github.com/izipay-pe/Imagenes/blob/main/logos_izipay/logo-izipay-banner-1140x100.png?raw=true" alt="Formulario" width=100%/>
</p>

# PopIn-PaymentForm-Python-Django

## Índice

➡️ [1. Introducción](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#%EF%B8%8F-1-introducci%C3%B3n)  
🔑 [2. Requisitos previos](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#-2-requisitos-previos)  
🚀 [3. Ejecutar ejemplo](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#-3-ejecutar-ejemplo)  
🔗 [4. Pasos de integración](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#4-pasos-de-integraci%C3%B3n)  
💻 [4.1. Desplegar pasarela](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#41-desplegar-pasarela)  
💳 [4.2. Analizar resultado de pago](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#42-analizar-resultado-del-pago)  
📡 [4.3. Pase a producción](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#43pase-a-producci%C3%B3n)  
🎨 [5. Personalización](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#-5-personalizaci%C3%B3n)  
📚 [6. Consideraciones](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#-6-consideraciones)

## ➡️ 1. Introducción

En este manual podrás encontrar una guía paso a paso para configurar un proyecto de **[Python]** con la pasarela de pagos de IZIPAY. Te proporcionaremos instrucciones detalladas y credenciales de prueba para la instalación y configuración del proyecto, permitiéndote trabajar y experimentar de manera segura en tu propio entorno local.
Este manual está diseñado para ayudarte a comprender el flujo de la integración de la pasarela para ayudarte a aprovechar al máximo tu proyecto y facilitar tu experiencia de desarrollo.

> [!IMPORTANT]
> En la última actualización se agregaron los campos: **nombre del tarjetahabiente** y **correo electrónico** (Este último campo se visualizará solo si el dato no se envía en la creación del formtoken).

<p align="center">
  <img src="https://github.com/izipay-pe/Imagenes/blob/main/formulario_incrustado/Imagen-Formulario-Incrustado.png?raw=true" alt="Formulario" width="350"/>
</p>

## 🔑 2. Requisitos Previos

- Comprender el flujo de comunicación de la pasarela. [Información Aquí](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/start.html)
- Extraer credenciales del Back Office Vendedor. [Guía Aquí](https://github.com/izipay-pe/obtener-credenciales-de-conexion)
- Para este proyecto utilizamos Python 3.12 o superior
- Para este proyecto utilizamos la herramienta Visual Studio Code.
> [!NOTE]
> Tener en cuenta que, para que el desarrollo de tu proyecto, eres libre de emplear tus herramientas preferidas.

## 🚀 3. Ejecutar ejemplo

### Instalar librerias y paquetes

1. Instalar una versión estable de python.

### Clonar el proyecto
```sh
git clone https://github.com/izipay-pe/PopIn-PaymentForm-Python-Django.git
``` 

### Datos de conexión 

Reemplace **[CHANGE_ME]** con sus credenciales de `API REST` extraídas desde el Back Office Vendedor, revisar [Requisitos previos](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#-2-requisitos-previos).

- Editar el archivo `keys.py` en la ruta `./Keys/keys.py`:
```python
keys = {
  # Identificador de su tienda
  "username": "~ CHANGE_ME_USER_ID ~",
  # Clave de Test o Producción
  "password": "~ CHANGE_ME_PASSWORD ~",
  # Clave Pública de Test o Producción
  "publickey": "~ CHANGE_ME_PUBLIC_KEY ~",
  # Clave HMAC-SHA-256 de Test o Producción
  "HMACSHA256": "~ CHANGE_ME_HMAC_SHA_256 ~"
}
```

### Ejecutar proyecto

1. Mover el proyecto y descomprimirlo.

2. Instala las librerias y paquetes necesarios con el comando `pip install -r requirements.txt`

3. Realizar las migraciones con el comando `python manage.py migrate`.

4. Ejecutar el proyecto con el comando `python manage.py runserver`.

2.  Abrir el navegador web(Chrome, Mozilla, Safari, etc) con el puerto 8000 que abrió el servidor interno de Django : `http://localhost:8000` y realizar una compra de prueba.


## 🔗4. Pasos de integración

<p align="center">
  <img src="https://i.postimg.cc/pT6SRjxZ/3-pasos.png" alt="Formulario" />
</p>

## 💻4.1. Desplegar pasarela
### Autentificación
Extraer las claves de `usuario` y `contraseña` del Backoffice Vendedor, concatenar `usuario:contraseña` y agregarlo en la solicitud del encabezado `Authorization`. Podrás encontrarlo en el archivo `./Demo/views.py` en la linea `36`.
```python
    url = 'https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment'
    auth = 'Basic ' + base64.b64encode(f"{keys["username"]}:{keys["password"]}".encode('utf-8')).decode('utf-8')
    # Configuración de encabezado de la solicitud
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }
```
ℹ️ Para más información: [Autentificación](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/embedded/keys.html)
### Crear formtoken
Para configurar la pasarela se necesita generar un formtoken. Se realizará una solicitud API REST a la api de creación de pagos:  `https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment` con los datos de la compra para generar el formtoken. Podrás encontrarlo en el archivo `./Demo/views.py`.

```python
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
    # Configuración del encabezado de la solicitud
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
    ## Obtenemos el formToken
    formToken = response_data['answer']['formToken']
    return render(request, 'Demo/checkout.html', {'formToken': formToken, 'publickey': keys['publickey']})
```
ℹ️ Para más información: [Formtoken](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/embedded/formToken.html)
### Visualizar formulario
Para desplegar la pasarela, configura la llave `public key` en el encabezado (Header) del archivo `./templates/Demo/checkout.html`. Esta llave debe ser extraída desde el Back Office del Vendedor.

Header: 
Se coloca el script de la libreria necesaria para importar las funciones y clases principales de la pasarela.
```javascript
<script type="text/javascript"
  src="https://static.micuentaweb.pe/static/js/krypton-client/V4.0/stable/kr-payment-form.min.js"
  kr-public-key="{{ publickey }}"
  kr-post-url-success="result" kr-language="es-Es">
</script>

<link rel="stylesheet" href="https://static.micuentaweb.pe/static/js/krypton-client/V4.0/ext/classic.css">
<script type="text/javascript" src="https://static.micuentaweb.pe/static/js/krypton-client/V4.0/ext/classic.js">
</script>
```
Además, se inserta en el body una etiqueta div con la clase `kr-embedded` que deberá tener el atributo `kr-popin` y `kr-form-token`, a este úlitmo incrustarle el `formtoken` generado en la etapa anterior.

Body:
```javascript
<div id="micuentawebstd_rest_wrapper">
  <div class="kr-embedded" kr-popin kr-form-token="{{formToken}}"></div>
</div>
```
ℹ️ Para más información: [Visualizar formulario](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/embedded/formToken.html)

## 💳4.2. Analizar resultado del pago

### Validación de firma
Se configura la función `checkhash()` que realizará la validación de los datos del parámetro `kr-answer` utilizando una clave de encriptacón definida por el parámetro `kr-hash-key`. Podrás encontrarlo en el archivo `./Demo/views.py`.

```python
def checkHash(reqPost, key):
  answerHash = hmac.new(key.encode('utf-8'), reqPost.get("kr-answer").encode('utf-8'), hashlib.sha256).hexdigest()
  hash = reqPost.get('kr-hash')
  return hash == answerHash
```

Se valida que la firma recibida es correcta

```python
if not request.POST: raise Exception("no post data received!")

if not checkHash(request.POST, keys["HMACSHA256"]) : raise Exception("Invalid signature")
```
En caso que la validación sea exitosa, se puede extraer los datos de `kr-answer` a través de un JSON y mostrar los datos del pago realizado.

```python
answer_json = json.loads( request.POST.get('kr-answer') )
json_formatted = json.dumps(answer_json, indent=2)
datos_json = json.dumps(request.POST, indent=4) 

answer_json["orderDetails"]["orderTotalAmount"] = answer_json["orderDetails"]["orderTotalAmount"] / 100

return render(request, 'Demo/result.html', {'answer': answer_json,"answer_json":json_formatted, 'dataPost': datos_json})
```
ℹ️ Para más información: [Analizar resultado del pago](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/kb/payment_done.html)

### IPN
La IPN es una notificación de servidor a servidor (servidor de Izipay hacia el servidor del comercio) que facilita información en tiempo real y de manera automática cuando se produce un evento, por ejemplo, al registrar una transacción.


Se realiza la verificación de la firma utilizando la función `checkhash()` y se devuelve al servidor de izipay un mensaje confirmando el estado del pago. Podrás encontrarlo en el archivo `./Demo/views.py`.

```python
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
```

La IPN debe ir configurada en el Backoffice Vendedor, en `Configuración -> Reglas de notificación -> URL de notificación al final del pago`

<p align="center">
  <img src="https://i.postimg.cc/zfx5JbQP/ipn.png" alt="Formulario" width=80%/>
</p>

ℹ️ Para más información: [Analizar IPN](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/kb/ipn_usage.html)

### Transacción de prueba

Antes de poner en marcha su pasarela de pago en un entorno de producción, es esencial realizar pruebas para garantizar su correcto funcionamiento.

Puede intentar realizar una transacción utilizando una tarjeta de prueba con la barra de herramientas de depuración (en la parte inferior de la página).

<p align="center">
  <img src="https://i.postimg.cc/3xXChGp2/tarjetas-prueba.png" alt="Formulario"/>
</p>

- También puede encontrar tarjetas de prueba en el siguiente enlace. [Tarjetas de prueba](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/kb/test_cards.html)

## 📡4.3.Pase a producción

Reemplace **[CHANGE_ME]** con sus credenciales de PRODUCCIÓN de `API REST` extraídas desde el Back Office Vendedor, revisar [Requisitos Previos](https://github.com/izipay-pe/Readme-Template/tree/main?tab=readme-ov-file#-2-requisitos-previos).

- Editar en `keys.py` en la ruta `./Demo/keys.py`:
```python
keys = {
  # Identificador de su tienda
  "username": "~ CHANGE_ME_USER_ID ~",
  # Clave de Test o Producción
  "password": "~ CHANGE_ME_PASSWORD ~",
  # Clave Pública de Test o Producción
  "publickey": "~ CHANGE_ME_PUBLIC_KEY ~",
  # Clave HMAC-SHA-256 de Test o Producción
  "HMACSHA256": "~ CHANGE_ME_HMAC_SHA_256 ~"
}
```

## 🎨 5. Personalización

Si deseas aplicar cambios específicos en la apariencia de la pasarela de pago, puedes lograrlo mediante la modificación de código CSS. En este enlace [Código CSS - Popin](https://github.com/izipay-pe/Personalizacion/blob/main/Formulario%20Popin/Style-Personalization-PopIn.css) podrá encontrar nuestro script para un formulario popin.

<p align="center">
  <img src="https://github.com/izipay-pe/Imagenes/blob/main/formulario_popin/Imagen-Formulario-Custom-Popin.png?raw=true" alt="Formulario"/>
</p>

## 📚 6. Consideraciones

Para obtener más información, echa un vistazo a:

- [Formulario incrustado: prueba rápida](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/quick_start_js.html)
- [Primeros pasos: pago simple](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/start.html)
- [Servicios web - referencia de la API REST](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/reference.html)
