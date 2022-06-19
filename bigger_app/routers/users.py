from fastapi import APIRouter, Depends

from ..dependencies import get_token_header

router = APIRouter(
  prefix="",
  tags=["user"],
  dependencies=[Depends(get_token_header)],
  responses={404: {"description": "Not found"}}
)

@router.get("/users")
async def read_users():
    return [{"username": "foo"}, {"username": "bar"}]
