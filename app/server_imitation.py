import requests
import json

host_port = '127.0.0.1:5000'
#host_port = '75.119.142.124:5000' # удалённый запуск
#host_port = '0.0.0.0:5000' # локальный


data_post = {
    "url": f"http://{host_port}/post/json",
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
data_put = {
    "url": f"http://{host_port}/put/json",
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

data_xml = '''<request>
    <url>http://127.0.0.1:8000/put</url>
    <database>Redis</database>
    <headers>
        <Content-Type>application/json</Content-Type>
    </headers>
    <data>
        <method>payment</method>
        <params>
            <card_holder_name>CARDHOLDER NAME</card_holder_name>
            <card_number>42780111112700</card_number>
            <card_expire>270</card_expire>
            <card_cvc>067</card_cvc>
            <amount>1000</amount>
            <description>Month subscription</description>
            <redirect_url>https://shop.merchant.com/order/23</redirect_url>
        </params>
        <id>85e0cd56-52c9-4709-b558-81203cb4e6ffjjjj</id>
    </data>
</request>'''

data_initial = {
    "url": f"http://{host_port}/post/initial",
    "url_ext": "https://vk.com/",
    "exclude_columns":['id','url'],
    "key_columns":['car_number','card_cvc'],
    "database": "Redis",
    "use_exclude_columns": True,
    "headers":{"Content-Type": "application/json"}

}

data_delete= {
   "url": f"http://{host_port}/delete",
   "url_ext": "https://vk.com/",
   "database": "Redis"
}
headers = {"Content-Type": "application/xml"}
url_xml = f'http://{host_port}/put'
def imitate():
   # response = requests.post(data_initial["url"], json=data_initial)

    response = requests.post(data_post["url"], json=data_post)
    for i in range(5):
        response = requests.post(data_post["url"], json=data_post)

   # response = requests.put(url_xml,headers=headers, data=data_xml)

   # response = requests.delete(data_delete["url"], json=data_delete)
    pass


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
