#!/usr/bin/env bash
# calc.cgi
# Procedimiento remoto: Calculadora distribuida con Idempotencia
set -euo pipefail

#--- 1) Subsistema de Idempotencia (Lectura de llave) ---
idemp="${HTTP_IDEMPOTENCY_KEY:-}"
cache_dir="/var/tmp"

if [ -n "$idemp" ] && [ -f "$cache_dir/$idemp" ]; then
    printf 'Content-Type: application/json; charset=UTF-8\r\n\r\n'
    cat "$cache_dir/$idemp"
    exit 0
fi

#--- 2) Unmarshalling de parámetros (QUERY_STRING) ---
op=$(echo "${QUERY_STRING:-}" | sed -n 's/.*op=\([^&]*\).*/\1/p')
a=$(echo "${QUERY_STRING:-}" | sed -n 's/.*a=\([^&]*\).*/\1/p')
b=$(echo "${QUERY_STRING:-}" | sed -n 's/.*b=\([^&]*\).*/\1/p')

if [ -z "$op" ] || [ -z "$a" ] || [ -z "$b" ]; then
    printf 'Status: 400 Bad Request\r\n'
    printf 'Content-Type: application/json; charset=UTF-8\r\n\r\n'
    echo '{"error": "Faltan parametros. Uso: op, a y b"}'
    exit 0
fi

#--- 3) Ejecución del procedimiento local con bc ---
resultado=""
case "$op" in
    suma)           resultado=$(echo "$a + $b" | bc -l) ;;
    resta)          resultado=$(echo "$a - $b" | bc -l) ;;
    multiplicacion) resultado=$(echo "$a * $b" | bc -l) ;;
    division)
        if [ "$b" = "0" ] || [ "$b" = "0.0" ]; then
            printf 'Status: 422 Unprocessable Entity\r\n'
            printf 'Content-Type: application/json; charset=UTF-8\r\n\r\n'
            echo '{"error": "Division entre cero detectada"}'
            exit 0
        fi
        resultado=$(echo "$a / $b" | bc -l)
        ;;
    *)
        printf 'Status: 400 Bad Request\r\n'
        printf 'Content-Type: application/json; charset=UTF-8\r\n\r\n'
        echo '{"error": "Operacion no soportada"}'
        exit 0
        ;;
esac

#--- 4) Marshalling y almacenamiento en caché ---
respuesta="{\"operacion\":\"$op\",\"operando_a\":$a,\"operando_b\":$b,\"resultado\":$resultado,\"servidor\":\"$(hostname -s)\"}"

if [ -n "$idemp" ]; then
    echo "$respuesta" > "$cache_dir/$idemp"
fi

printf 'Content-Type: application/json; charset=UTF-8\r\n\r\n'
echo "$respuesta"
