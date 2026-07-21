# Práctica 1: Arquitectura RPC mediante CGI y Shell Script sobre Nginx

**Instituto Politécnico Nacional**  
**Escuela Superior de Ingeniería Mecánica y Eléctrica (Unidad Culhuacán)**  
*Ingeniería en Computación — Sistemas Distribuidos (8.º Semestre)*  

---

## 📌 Descripción General
Implementación de un servicio de llamadas a procedimientos remotos (RPC) invocable mediante el protocolo HTTP, empleando el modelo **Common Gateway Interface (CGI)** sobre GNU Bash. La infraestructura utiliza **Nginx** como servidor web frontal y **fcgiwrap** como puente traductor del protocolo FastCGI a CGI.

---

## 🛠️ Entorno y Prerrequisitos
* **Sistema Operativo:** Fedora Server 44 (x86_64)
* **Servidor Web / FastCGI:** Nginx ≥ 1.18, `fcgiwrap`
* **Intérprete / Lenguaje:** GNU Bash ≥ 5.0
* **Herramientas Auxiliares:** `curl`, `jq`, `bc`

---

## 📁 Estructura del Repositorio

```text
practical-rpc/
├── cgi-bin/
│   ├── saludo.cgi   # Procedimiento remoto básico (GET/POST, salida texto/JSON)
│   └── calc.cgi     # Calculadora distribuida con soporte de idempotencia (bc)
├── nginx/
│   └── rpc-cgi.conf # Configuración de bloque location y parámetros FastCGI para Nginx
└── README.md
🚀 Uso e Invocación de Servicios Remotos1. Invocación de saludo.cgiConsulta GET (Salida Texto):Bashcurl -4 -s "http://localhost/rpc/saludo.cgi?nombre=Mike"
Consulta GET (Salida JSON):Bashcurl -4 -s -H "Accept: application/json" "http://localhost/rpc/saludo.cgi?nombre=Profesor" | jq
Consulta POST:Bashcurl -4 -s -X POST -d "nombre=ESIME" "http://localhost/rpc/saludo.cgi"
2. Invocación de calc.cgi (Calculadora e Idempotencia)Operación de Suma:Bashcurl -4 -s "http://localhost/rpc/calc.cgi?op=suma&a=3.5&b=4.2" | jq
Petición con Encabezado de Idempotencia (Idempotency-Key):Bashcurl -4 -s -H "Idempotency-Key: token-123" "http://localhost/rpc/calc.cgi?op=multiplicacion&a=7&b=8" | jq
📊 Mapeo a los 5 Componentes Clásicos de RPCComponente RPCMapeo en la Práctica 1ClienteHerramienta curl ejecutando peticiones HTTP con parámetros en URL o cuerpo.Stub del ClienteLibrería libcurl que empaqueta los parámetros en QUERY_STRING o POST.RPC RuntimeNginx + fcgiwrap + Pila TCP/IP administrando el transporte e invocación vía socket Unix.Stub del ServidorBloque inicial de saludo.cgi / calc.cgi leyendo variables CGI (REQUEST_METHOD, CONTENT_LENGTH).ServidorLógica en Bash procesando la solicitud (bc) y retornando respuesta en stdout.
