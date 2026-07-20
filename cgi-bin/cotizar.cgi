#!/bin/bash
printf "Content-Type: application/json; charset=utf-8\r\n\r\n"

QUERY_STRING="${QUERY_STRING:-}"
MONTO=$(echo "$QUERY_STRING" | grep -oP 'monto=\K[0-9.]+' || echo "1000")
CATEGORIA=$(echo "$QUERY_STRING" | grep -oP 'categoria=\K[a-zA-Z]+' || echo "estandar")

DESCUENTO=0
if [ "$CATEGORIA" = "premium" ] || [ "$CATEGORIA" = "PREMIUM" ]; then
    DESCUENTO=15
elif [ "$CATEGORIA" = "estudiante" ] || [ "$CATEGORIA" = "ESTUDIANTE" ]; then
    DESCUENTO=20
fi

SUBTOTAL=$(echo "$MONTO" | awk '{print $1}')
IMPUESTO=$(echo "$SUBTOTAL" | awk '{printf "%.2f", $1 * 0.16}')
MONTO_DESC=$(echo "$SUBTOTAL $DESCUENTO" | awk '{printf "%.2f", $1 * ($2 / 100)}')
TOTAL=$(echo "$SUBTOTAL $IMPUESTO $MONTO_DESC" | awk '{printf "%.2f", $1 + $2 - $3}')
FECHA=$(date '+%Y-%m-%d %H:%M:%S')
HOST=$(hostname)

cat <<JSON
{
  "servicio": "Cotizador RPC Heterogéneo IPN",
  "servidor_host": "$HOST",
  "timestamp": "$FECHA",
  "solicitud": {
    "monto_base": $SUBTOTAL,
    "categoria": "$CATEGORIA",
    "porcentaje_descuento": $DESCUENTO
  },
  "cotizacion": {
    "subtotal": $SUBTOTAL,
    "iva_16": $IMPUESTO,
    "descuento_aplicado": $MONTO_DESC,
    "monto_total": $TOTAL
  },
  "estado": "SUCCESS_200"
}
JSON
