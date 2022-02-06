# import pytest
# from httpx import AsyncClient
#
# from main import app
#
#
# @pytest.mark.anyio
# async def test_root():
#     data = {"username":"Alex","password":"easypassword"}
#     async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/user/1", ) as ac:
#         response = await ac.get("/",json=data)
#     assert response.status_code == 200
#     assert response.json() == {
#     "id": 1,
#     "username": "Dimas23",
#     "email": "1222233@gmail.com",
#     "register_date": "2022-02-06T02:52:49.621645+00:00"
# }
#
#
