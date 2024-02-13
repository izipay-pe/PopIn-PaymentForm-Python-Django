# [PopIn-PaymentForm-Python-Django]
##  Índice
* [1. Introducción](#1-introducción)
* [2. Requisitos previos](#2-requisitos-previos)
* [3. Despliegue](#3-despliegue)
* [4. Datos de conexión](#4-datos-de-conexión)
* [5. Transacción de prueba](#5-transacción-de-prueba)
* [6. Implementación de la IPN](#6-implementación-de-la-ipn)
* [7. Personalización](#7-personalización)
* [8. Consideraciones](#8-consideraciones)
## 1. Introducción
En este manual podrás encontrar una guía paso a paso para configurar un proyecto de **[Python - Django]** con la pasarela de pagos de IZIPAY. Te proporcionaremos instrucciones detalladas y credenciales de prueba para la instalación y configuración del proyecto, permitiéndote trabajar y experimentar de manera segura en tu propio entorno local.
Este manual está diseñado para ayudarte a comprender el flujo de la integración de la pasarela para ayudarte a aprovechar al máximo tu proyecto y facilitar tu experiencia de desarrollo.

<p align="center">
  <img src="https://github.com/izipay-pe/Imagenes/blob/main/formulario_popin/formulario_popin.png?raw=true" alt="Formulario" width="250"/>
</p>

<a name="Requisitos_Previos"></a>
 
## 2. Requisitos previos
* Comprender el flujo de comunicación de la pasarela. [Información Aquí](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/start.html)
* Extraer credenciales del Back Office Vendedor. [Guía Aquí](https://github.com/izipay-pe/obtener-credenciales-de-conexion)
* Para este proyecto utilizamos **Python 3.10**
* Para este proyecto utilizamos la herramienta Visual Studio Code.
> [!NOTE]
> Tener en cuenta que, para que el desarrollo de tu proyecto, eres libre de emplear tus herramientas preferidas.

## 3. Despliegue
### Instalar Plugin "Python"
Python, extensión para Visual Studio Code que ofrece soporte completo para el lenguaje Python (para todas las versiones del lenguaje >= 3.7). Para instalarlo:
1. Ingresar a la sección "Extensiones" de Visual Studio Code
2. Buscar "Python"
3. Instalar extensión

<p align="center">
  <img src="https://i.postimg.cc/XYZKRcNJ/Plugin.png" alt="Plugin" width="850"/>
</p>

### Clonar el proyecto:
  ```sh
  git clone [https://github.com/izipay-pe/PopIn-PaymentForm-Python-Django.git]
  ```
  
### Preparar el entorno:
Antes de ejecutar el proyecto, se creará el virtual environment (venv):
1. Presionar `ctrl` + `shift` + `p` para abrir la paleta de comandos y buscar `Python: Select Interpreter`
<p align="center">
  <img src="https://i.postimg.cc/yYpXprHt/Select-Interpreter.png" alt="PanelComandos" width="850"/>
</p>
2. Seleccionar `Create Virtual Environment`
<p align="center">
  <img src="https://i.postimg.cc/43fcJ6sV/Create-Env.png" alt="CreateVenv" width="850"/>
</p>
3. Seleccionar el tipo de venv
<p align="center">
  <img src="https://i.postimg.cc/PJ2zjS8L/Venv.png" alt="SelectVenv" width="850"/>
</p>
4. Seleccionar la versión de Python
<p align="center">
  <img src="https://i.postimg.cc/1RHKw3Y9/Select-Python.png" alt="SelectPython" width="850"/>
</p>
5. Seleccionar archivo de dependencias `requirements.txt`
<p align="center">
  <img src="https://i.postimg.cc/pr2Y4wyb/Requirements.png" alt="SelectRequirements" width="850"/>
</p>
6. Una vez instaladas las dependencias, verificar el venv creado mediante `ctrl` + `shift` + `p`, buscar `Python: Select Interpreter` y seleccionar venv
<p align="center">
  <img src="https://i.postimg.cc/TY3J9vZn/Select-Env.png" alt="SelectInterpreter" width="850"/>
</p>

### Ejecutar proyecto
Para ejecutar el proyecto a través de Visual Studio, abrir una nueva terminar y activar el venv creado:

  ```sh
  .venv\scripts\activate 
  ```
> [!CAUTION]
> En caso de error ejecutar PowerShell como administrador y ejecutar el comando  `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

Realizar las migraciones:
 ```sh
  python manage.py migrate
  ```
Ejecutar el proyecto:
 ```sh
  python manage.py runserver
  ```
## 4. Datos de conexión 

**Nota**: Reemplace **[CHANGE_ME]** con sus credenciales de `API REST` extraídas desde el Back Office Vendedor, ver [Requisitos Previos](#Requisitos_Previos).

* Editar en `Keys/keys.py` :
<p align="center">
  <img src="https://i.postimg.cc/k4NvjJJv/Credentials.pngg" alt="Credentials"/>
</p>

## 5. Transacción de prueba
Antes de poner en marcha su pasarela de pago en un entorno de producción, es esencial realizar pruebas para garantizar su correcto funcionamiento. 

Puede intentar realizar una transacción utilizando una tarjeta de prueba con la barra de herramientas de depuración (en la parte inferior de la página).

<p align="center">
  <img src="https://i.postimg.cc/3xXChGp2/tarjetas-prueba.png" alt="Formulario"/>
</p>

* También puede encontrar tarjetas de prueba en el siguiente enlace. [Tarjetas de prueba](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/kb/test_cards.html)
 
## 6. Implementación de la IPN
> [!IMPORTANT]
> Es recomendable implementar la IPN para comunicar el resultado de la solicitud de pago al servidor del comercio.

La IPN es una notificación de servidor a servidor (servidor de Izipay hacia el servidor del comercio) que facilita información en tiempo real y de manera automática cuando se produce un evento, por ejemplo, al registrar una transacción.
Los datos transmitidos en la IPN se reciben y analizan mediante un script que el vendedor habrá desarrollado en su servidor.
* Ver manual de implementación de la IPN. [Aquí]( https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/kb/payment_done.html)
* Vea el ejemplo de la respuesta IPN con PHP. [Aquí](https://github.com/izipay-pe/Redirect-PaymentForm-IpnT1-PHP)
* Vea el ejemplo de la respuesta IPN con NODE.JS. [Aquí](https://github.com/izipay-pe/Response-PaymentFormT1-Ipn)

## 7. Personalización
Si deseas aplicar cambios específicos en la apariencia de la pasarela de pago, puedes lograrlo mediante la modificación de código CSS. En este enlace [Código CSS - Incrustado](https://github.com/izipay-pe/Personalizacion-PaymentForm-Incrustado) podrá encontrar nuestro script para un formulario incrustado.

## 8. Consideraciones
Para obtener más información, echa un vistazo a:
- [Formulario incrustado: prueba rápida](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/quick_start_js.html)
- [Primeros pasos: pago simple](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/start.html)
- [Servicios web - referencia de la API REST](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/reference.html)
