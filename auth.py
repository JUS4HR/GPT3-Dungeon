import json as __j
import os as __o
import random as __r
"""
    json example:
    [
        {
            "uid": 1234567890,
            "uname": "test",
            "passwd": "some password",
            "token": "64 random characters"
        },
        ...
    ]
"""
jsonPath = "config/auth.json"


def __checkPasswd(uname: str, passwd: str):
    with open(jsonPath, "r") as f:
        data = __j.load(f)
        for user in data:
            if user["uname"] == uname and user["passwd"] == passwd:
                return {
                    "success": "True",
                    "uid": user["uid"],
                    "token": user["token"]
                }
    return {"success": "False"}


def __checkAuth(uid: str, token: str):
    with open(jsonPath, "r") as f:
        data = __j.load(f)
        for user in data:
            if user["uid"] == uid and user["token"] == token:
                return {"success": "True"}
    return {"success": "False"}


def __addAuth(uname: str, password: str):
    if not __o.path.exists(jsonPath):
        with open(jsonPath, "w") as f:
            f.write("[]")
    currentUidList = []
    currentTokenList = []
    currentUnameList = []
    with open(jsonPath, "r") as f:
        data = __j.load(f)
        for user in data:
            currentUidList.append(user["uid"])
            currentTokenList.append(user["token"])
            currentUnameList.append(user["uname"])
    if uname in currentUnameList:
        return {"success": "False", "reason": "User name already exists"}
    udi = 0
    while udi in currentUidList or udi == 0:
        udi = __r.randint(1000000000, 9999999999)
    token = ""
    while token == "" or token in currentTokenList:
        token = ""
        for i in range(64):
            token += __r.choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
    data = []
    with open(jsonPath, "r") as f:
        data = __j.load(f)
    data.append({
        "uid": udi,
        "uname": uname,
        "passwd": password,
        "token": token
    })
    with open(jsonPath, "w") as f:
        __j.dump(data, f)
    return {"success": "True", "uid": udi, "token": token}


def authTokenCallback(input: dict) -> dict:
    return __checkAuth(input["uid"], input["token"])


def authPasswordCallback(input: dict) -> dict:
    return __checkPasswd(input["uname"], input["pass"])
