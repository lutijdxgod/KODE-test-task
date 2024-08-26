from passlib.context import CryptContext
import httpx

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_hashes(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def check_for_spelling(title: str, contents: str | None):
    params = {"text": [title]}
    if contents is not None:
        text_list = params["text"]
        text_list.append(contents)
        params.update({"text": text_list})

    request = httpx.get("https://speller.yandex.net/services/spellservice.json/checkTexts", params=params)
    return request.json()
