# NOTES APP (KODE test task)

This small FastAPI application allows you to manage your notes and check them for misspellings or typos. (featuring Яндекс.Спеллер)

Full list of endpoints:
- POST /auth/register: Register a new user
- POST /auth/login: Log into your account
- POST /notes/create: Create a new note if it doesn't have any erros(otherwise it will tell you)
- GET /notes/: Get all your notes

## FEATURES
- Integration with Яндекс.Спеллер for typo checking.
- Docker support for easy deployment.

## RUNNING THE APP
1. Clone the repo
2. Make sure that Docker engine is running
3. Change environment variables in docker-compose.yml to suit yourself.
4. docker-compose up -d
