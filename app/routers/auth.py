from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_credentials: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Register a new user

    body params:
    :username: user's nickname
    :password: user's password

    returns information about a newly created user or response with status code 403
    when user with given username is already created
    """
    user_query = db.query(models.User).filter(models.User.username == user_credentials.username)
    user = user_query.first()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="There is already a user with given username."
        )

    hashed_password = utils.hash(user_credentials.password)
    user_credentials.password = hashed_password

    new_user = models.User(**user_credentials.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    Authenticate a user

    xxx-wwww-form-urlencoded params:
    :username: user's nickname
    :password: user's password
    """
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    if not utils.verify_hashes(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}
