import requests
import json

host_port = '127.0.0.1:8000'
host_port = '75.119.142.124:5000' # удалённый запуск
host_port = '0.0.0.0:5000' # локальный


'''
all_request_post = [{
"url": "http://127.0.0.1:8000/post",  # Замените на фактический URL вашего сервера
"url_ext": "example",
"headers": {"Content-Type": "application/json"},
"data": {
    "method": "payment",
    "params": {
        "card_holder_name": "CARDHOLDER NAME",
        "card_number": "4278011111275400",
        "card_expire": "2702",
        "card_cvc": "067",
        "amount": "1000",
        "description": "Month subscription",
        "redirect_url": "https://shop.merchant.com/order/23"
    },
    "id": "85e0cd56-52c9-4709-b558-81203cb4e6ff"
},

}]
for i in all_request_post:
    requests.post(i['url'], headers=i['headers'], data=json.dumps(i['data']))
'''
data = {
    "url": f"http://{host_port}/put",
    "database": "Redis",
    "headers": {"Content-Type": "application/json"},
    "data": {
        "method": "payment",
        "params": {
            "card_holder_name": "CARDHOLDER NAME",
            "card_number": "4278011111275400",
            "card_expire": "2702",
            "card_cvc": "067",
            "amount": "1000",
            "description": "Month subscription",
            "redirect_url": "https://shop.merchant.com/order/23"
        },
        "id": "85e0cd56-52c9-4709-b558-81203cb4e6ffjjjj"
    }
}


data_initial = {
    "url": f"http://{host_port}/post/initial",
    "url_ext": "https://vk.com/",
    "exclude_columns":['id','url'],
    "key_columns":['car_number','card_cvc'],
    "database": "Redis",
    "flag_columns": True,
    "headers":{"Content-Type": "application/json"}

}

data_delete= {
   "url": f"http://{host_port}/delete",
   "url_ext": "https://vk.com/",
   "database": "Redis"
}

def imitate():
    response = requests.post(data_initial["url"], json=data_initial)

    response = requests.put(data["url"], json=data)

    response = requests.delete(data_delete["url"], json=data_delete)


'''
data = {
    "url": "http://127.0.0.1:8000/get",
    "params": {
        "url_ext": "https://vk.com/",
        "headers": {}
    }
}
'''

#response = requests.get(data["url"], params=data["params"])
