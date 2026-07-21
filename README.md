
# Arquitectura de Invocación Remota (RPC, Java RMI & Servicios Heterogéneos)

**Instituto Politécnico Nacional**  
*Escuela Superior de Ingeniería Mecánica y Eléctrica (ESIME Culhuacán)*  
**Materia:** Sistemas Distribuidos | **Grupo:** 8CV22  

---

## 📌 Descripción del Proyecto

Este repositorio contiene la implementación práctica e integradora de tres esquemas de comunicación distribuida y llamadas a procedimientos remotos (RPC):

1. **RPC sobre CGI/FastCGI en Bash & Nginx:** Servicio remoto basado en scripts de Shell procesados a través de `fcgiwrap` y Nginx, ofreciendo procesamiento de peticiones GET/POST, formateo JSON e idempotencia mediante tokens.
2. **Java RMI Seguro con Persistencia Relacional:** Invocación remota de objetos en Java protegida mediante cifrado **SSL/TLS** (certificados X.509 v3 con extensión SAN) y persistencia de transacciones en una base de datos relacional **SQLite**.
3. **Servicios Heterogéneos (Java -> Nginx -> Bash):** Cliente integrador Java (`HttpClient`) que consume gateways REST/CGI de forma asíncrona, desacoplando la lógica de negocio del lenguaje de programación.

---

## 🛠️ Requisitos del Sistema

* **Sistema Operativo:** Fedora Server 44 (o equivalente Linux)
* **Java Development Kit (JDK):** JDK 19 o superior
* **Servidor Web:** Nginx 1.30+ con `fcgiwrap`
* **Base de Datos:** SQLite 3 con driver JDBC
* **Herramientas Auxiliares:** `curl`, `jq`, `tcpdump`, `bc`

---

## 🚀 Guía de Ejecución Rápida

### 1. Invocación Heterogénea (CGI sobre Nginx)
```bash
# Iniciar servicio fcgiwrap y nginx
systemctl start nginx

# Probar endpoint desde terminal
curl -s "http://localhost:8080/cgi-bin/rpc/cotizar.cgi?monto=2500&categoria=premium"

# Ejecutar Cliente Integrador en Java
cd src
javac mx/ipn/esimecu/rpc/ClienteIntegrador.java
java mx.ipn.esimecu.rpc.ClienteIntegrador
2. Java RMI Seguro (SSL/TLS + SQLite)Bash# Compilar clases
./scripts/compilar.sh

# Generar Keystore SSL (en la carpeta security/)
keytool -genkeypair -alias rmikey -keyalg RSA -keysize 2048 \
  -keystore security/keystore.jks -storepass ipn2026 -keypass ipn2026 \
  -dname "CN=ServidorRMI, OU=ESIME, O=IPN, L=CDMX, C=MX" \
  -ext "SAN=dns:localhost,ip:127.0.0.1,ip:192.168.56.103" -validity 365

# Iniciar Servidor RMI
./scripts/iniciar_servidor_rmi.sh 192.168.56.103

# En otro nodo/terminal, iniciar Cliente RMI
./scripts/iniciar_cliente_rmi.sh 192.168.56.103
📊 Arquitectura de Componentes RPCComponente RPCImplementación CGI / BashImplementación Java RMIClientecurl / ClienteIntegrador.javaClienteRMI.javaClient Stublibcurl / HttpClientStub dinámico generado por Naming.lookupRPC RuntimeNginx + fcgiwrap + TCP/IPProtocolo JRMP / SSLSocketFactoryServer StubEncabezados CGI / QUERY_STRINGUnicastRemoteObjectServidorcotizar.cgi / saludo.cgiCalculadoraImpl.java / BitacoraImpl.javaEOF

