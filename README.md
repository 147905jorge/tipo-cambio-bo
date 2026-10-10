# tipo-cambio-bo

Sincroniza diariamente (01:00 Bolivia, UTC-4) el tipo de cambio oficial
USD/BOB publicado por el Banco Central de Bolivia y lo expone como
`tipo-cambio.json` en este repo, listo para consumir con CORS abierto
via:

```
https://raw.githubusercontent.com/147905jorge/tipo-cambio-bo/main/tipo-cambio.json
```

Usado por el sitio de Oriental SRL para la calculadora de tributos
aduaneros, sin depender de ningun backend propio.
