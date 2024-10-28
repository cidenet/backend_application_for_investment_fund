# Proyecto de Fondos de Inversión con FastAPI

Este proyecto es una API para gestionar fondos de inversión, suscripciones y notificaciones. La API está construida con FastAPI y se conecta a una base de datos MongoDB alojada en MongoDB Atlas. También incluye funcionalidades para enviar notificaciones por email y SMS.

## Estructura de Carpetas
teniendo en cuenta que faltan artefactos en la estructura de carpetas, se propone la siguiente estructura base:

```plaintext
app_fondos_inversion/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fund.py
│   │   ├── subscription.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── fund_repository.py
│   │   ├── mongo_fund_repository.py
│   │   ├── subscription_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fund_service.py
│   │   ├── subscription_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── notification/
│   │   │   ├── __init__.py
│   │   │   ├── email_notification.py
│   │   │   ├── sms_notification.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── fund_router.py
│   │   ├── subscription_router.py
├── tests/
│   ├── __init__.py
│   ├── test_fund_service.py
│   ├── test_subscription_service.py
├── .env
├── .flake8
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md

```
## MANEJO ED EXCEPCIONES
- Se implementa en este proyecto principalmente en los servicios, para manejar errores de validación y de negocio.

## PRUEBAS UNITARIAS
- Se implementan pruebas unitarias para los servicios de fondos y suscripciones.

## COBERTURA DE PRUEBAS
- Se implementa la cobertura de pruebas con el módulo `coverage`.
- Se garantiza
