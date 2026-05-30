from fastapi import HTTPException


def ai_error(status_code: int, message: str, code: str, details: str | None = None) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            'success': False,
            'message': message,
            'error': {'code': code, 'details': details},
        },
    )
