import requests

# example of request
"""
    {
  "id": "some_qr_1",
  "amount": {
    "value": 100,
    "currency": "RUB"
  }
}
"""

# answer
"""
{
"result": "CREATED",
"link": "link_to_qr"
}
"""

# callback
"""
{
  "id": "some_qr_1",
  "status": "PAID"
}

"""


def do_callback(url, response={
                                "id": "some_qr_1",
                                "status": "PAID"
                                }):
    """Если в запросе есть флаг на callback, то отправляем"""

    # save callback into redis? and check if exists then dont make new callback

    return requests.post(url, data=response)
