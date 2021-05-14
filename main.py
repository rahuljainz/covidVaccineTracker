import time

from handler import lambda_handler

if __name__ == '__main__':
    event = {
        "locations": [
            {
                "state": "delhi"
            },
            {
                "state": "haryana",
                "district": "gurgaon"
            }
        ],
        "days": 2,
        "vaccine": "COVISHIELD",
        "age": 50,
        "IFTTT_WEBHOOK_EVENT_NAME": "*****",
        "IFTTT_WEBHOOK_KEY": "*******"
    }
    while True:
        lambda_handler(event, None)
        print("Waiting for another 30 mins to retry")
        time.sleep(30 * 60)
