#!/bin/bash
# Script de despliegue básico (Ejecutar en la Máquina Virtual)

echo "Construyendo contenedores..."
sudo docker-compose build

echo "Deteniendo contenedores previos..."
sudo docker-compose down

echo "Levantando el proyecto en modo 'detached' (background)..."
sudo docker-compose up -d

echo "¡Despliegue completado con éxito! Revisa los logs con 'sudo docker-compose logs -f'."
