import uuid
from fastapi import APIRouter, HTTPException, Depends, Header
from tortoise.expressions import Q
from ..models.models import User
from ..schemas import user_schemas
from ..dependencies import role_depends
from ..utils import str_to_selt_sha256


router = APIRouter(tags=['登录'])


@router.post('/login', response_model=user_schemas.LoginResponse, summary='登录')
async def login(body: user_schemas.UserLogin):
    # 支持账号/邮箱登录
    db_user = await User.filter(Q(account=body.account) | Q(email=body.account)).first()
    if not db_user: # 账号/邮箱登录失败
        raise HTTPException(status_code=400, detail='Account or password is incorrect')
    elif not db_user.status: # 账户已停用
        raise HTTPException(status_code=400, detail='Account is disabled')
    elif db_user.password == str_to_selt_sha256(body.password, db_user.password.split('$')[2]): # 密码正确，更新token
        await User.filter(id=db_user.id).update(access_token=uuid.uuid4())
        return {"code": 200, "message": "success", "data": await User.filter(id=db_user.id).first()}
    else:
        raise HTTPException(status_code=400, detail='Account or password is incorrect')


@router.delete('/logout', summary='退出登录', dependencies=[Depends(role_depends())])
async def logout(X_Token: str=Header(None)):
    if X_Token: # 清空token
        await User.filter(access_token=X_Token).update(access_token=None)
    return {"code": 200, "message": "success"}
