# monitorVehicleEE-be-fta
# python -m venv .venv
<!-- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -->
<!-- .\.venv\Scripts\Activate.ps1 -->
# pip install opencv-python
# pip install numpy==1.26.4
# driver python cho postgresql: pip install psycopg2-binary
# pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib[bcrypt] python-multipart
# SQLAlchemy async:  pip install sqlalchemy asyncpg
# pip install python-jose passlib[bcrypt]
# pip install email-validator
# pip install bcrypt==4.0.1
# pip install fastapi uvicorn

# run server
uvicorn src.app.main:main --reload --host 0.0.0.0 --port 8000
