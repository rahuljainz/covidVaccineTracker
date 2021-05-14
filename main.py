import time

from lambda_handler import lambda_handler

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
        "vaccine": "COVISHIELD",
        "age": 50,
        "days": 2,
        "IFTTT_WEBHOOK_EVENT_NAME": "vacineTracker",
        "IFTTT_WEBHOOK_KEY": "*******"
    }
    while True:
        lambda_handler(event, None)
        print("Waiting for another 30 mins to retry")
        time.sleep(30 * 60)
