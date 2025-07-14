#!/bin/bash
PORT=4444
echo "[*] Dinleyici başlatılıyor: nc -lvnp $PORT"
nc -lvnp $PORT
