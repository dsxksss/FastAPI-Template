from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from tortoise.exceptions import DoesNotExist, IntegrityError


class SettingNotFound(Exception):
    pass


async def DoesNotExistHandle(req: Request, exc: DoesNotExist) -> JSONResponse:
    content = dict(
        code=404,
        msg=f"Object has not found, exc: {exc}, query_params: {req.query_params}",
    )
    return JSONResponse(content=content, status_code=404)


async def HttpExcHandle(request: Request, exc: HTTPException):
    if (
        exc.status_code == 401
        and exc.headers
        and "WWW-Authenticate" in exc.headers
    ):
        return Response(status_code=exc.status_code, headers=exc.headers)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": exc.detail, "data": None},
    )


async def IntegrityHandle(request: Request, exc: IntegrityError):
    content = dict(
        code=500,
        msg=f"IntegrityError，{exc}",
    )
    return JSONResponse(content=content, status_code=500)


async def RequestValidationHandle(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    content = dict(code=422, msg=f"RequestValidationError, {exc}")
    return JSONResponse(content=content, status_code=422)


async def ResponseValidationHandle(
    _: Request, exc: ResponseValidationError
) -> JSONResponse:
    content = dict(code=500, msg=f"ResponseValidationError, {exc}")
    return JSONResponse(content=content, status_code=500)
