import requests
import json
import pandas as pd
import os
import dataframe_image as dfi
import uuid


async def get(login, password, type):
    url = "http://127.0.0.1:5000/finances"

    payload = json.dumps({
        "login": login,
        "password": password,
        "type": int(type)
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        print(response.content)
        return {"message": "Error hapened during data processing."}, True
    res_json = response.json()[0]
    account = {}
    currency = "AED"
    if int(type) == 48:
        currency = "Swipes"

    account["name"] = res_json["name"]
    account["username"] = res_json["username"]
    account["balance"] = f'{res_json["amount"]} {currency}'
    df = pd.DataFrame(res_json["history"])
    if not os.path.exists("img"):
        os.makedirs("img")
    unique_filename = f'./img/{str(uuid.uuid4())}.png'
    dfi.export(df, unique_filename, table_conversion="matplotlib")
    account["image"] = unique_filename

    return account, False