activcación del entorno virtual
venv/Scripts/activate

- instalaciones:
pip install fastapi uvicorn pymongo


mkdir app
cd app
mkdir models routers services utils


# Crear archivos principales
- estando parado en app retrocedo a la base del proyecto:
cd .. 

- luego ejecuto los comandos:
echo > app/main.py
echo > app/models/user.py
echo > app/models/subscription.py
echo > app/routers/user.py
echo > app/routers/subscription.py
echo > app/services/user_service.py
echo > app/services/subscription_service.py
echo > app/utils/database.py
echo > .gitignore


- pruebas unitarias
pip install pytest coverage


- correr la app:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

uvicorn main:app --port 8001 --reload

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


- instalar: 
pip install pytest mongomock


pytest app/services/tests/test_subscription_service.py


pip install coverage

- correr las pruebas con coverage:
coverage run -m pytest
coverage report

- instalar: 
pip install pytest-cov


--------------------------------------------------
# Establecer el PYTHONPATH temporalmente en la terminal
export PYTHONPATH=$(pwd)  # En Linux/Mac
set PYTHONPATH=%cd%       # En Windows

# Instalar pytest, coverage y mongomock
pip install pytest coverage mongomock

# Ejecutar todas las pruebas unitarias
pytest tests/

# Ejecutar las pruebas con coverage
coverage run -m pytest tests/

# Generar el informe de cobertura en la terminal
coverage report

# Generar un informe HTML (opcional)
coverage html

# Instalar pytest, pytest-cov y coverage
pip install pytest pytest-cov coverage

# Ejecutar las pruebas con cobertura
pytest --cov=app tests/

# Generar el informe de cobertura en la terminal
coverage report

# Generar un informe HTML (opcional)
coverage html


- librerias:
pip install python-dotenv



# AWS LIBS
pip install fastapi boto3 python-dotenv
pip install boto3

# CALIDAD DEL CODIGO
pip install flake8

# CORS:
pip install fastapi-cors


# generacion del requirement:
pip freeze > requirements.txt

--------------------------------

# Despliegue AWS EC2:

- Ir a la carpeta donde está el archivo Dockerfile
- Crear la imagen de Docker:
docker build -t fastapi-mongo .
- Listar las imágenes de Docker:
docker images ps
- guardar la imagen en un zip:
docker save -o fastapi-mongo.tar fastapi-mongo

- enviar imagen comprimida:
 scp -i "claves_investment_fund.pem" fastapi-mongo.tar ec2-user@52.14.212.18:~/
 scp -i "claves_investment_fund.pem" .env ec2-user@52.14.212.18:~/


- cargar la imagen en docker:
docker load -i fastapi-mongo.tar

- Ejecutar la imagen:
- local
docker run -d -p 8000:8000 --env-file .env fastapi-mongo
- prod
docker run -d -p 8000:8000 --env-file /home/ec2-user/.env fastapi-mongo

- cargar variables de entorno:
export $(cat /home/ec2-user/.env | xargs)

docker stop 79328db21577

- verificar que este detenido:
docker ps -a

