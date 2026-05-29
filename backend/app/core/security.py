from jose import jwt


ALGORITHM = "HS256"


def create_access_token(subject: str, secret: str) -> str:
    return jwt.encode({"sub": subject}, secret, algorithm=ALGORITHM)
