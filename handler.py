import json
import subprocess
from datetime import datetime, timedelta

import requests

from constants import STATES_MAP


def fetch_vaccine_slot(district_id, date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
        district_id, date)
    command = ["curl", "-A", "\"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0\"", "-s", url]
    response = subprocess.check_output(command)
    response = json.loads(response.decode("utf-8"))
    open_slots = []
    for center in response["centers"]:
        for session in center["sessions"]:
            if session["available_capacity"] > 0:
                session["center_name"] = center["name"]
                session["district_name"] = center["district_name"]
                open_slots.append(session)
    return open_slots


def fetch_slots_for_districts(districts, date):
    slots = []
    for district_name, district_id in districts.items():
        print("Searching for district: {} for date: {}".format(district_name, date))
        slots.extend(fetch_vaccine_slot(district_id, date))

    covaxin_slots = [x for x in slots if x["vaccine"] == "COVAXIN"]
    covishield_slots = [x for x in slots if x["vaccine"] != "COVAXIN"]
    print("Covaxin slots found: {}".format(len(covaxin_slots)))
    print("Covishield slots found: {}".format(len(covishield_slots)))

    return slots


def fetch_slots_districts_days(districts, days, vaccine, age):
    now = datetime.now()
    allSlots = []
    for i in range(days):
        date = now.strftime("%d-%m-%Y")
        try:
            open_slots = fetch_slots_for_districts(districts, date)
            preferred_slots = [x for x in open_slots if filter_slot(x, vaccine, age)]
            print("{} Preferred slots found for date: {}".format(len(preferred_slots), date))
            allSlots.extend(preferred_slots)
        except Exception as e:
            print(e)
            print("Failing to run......")
        now = now + timedelta(days=1)
    return allSlots


def filter_slot(slot, vaccine: str, min_age):
    if slot["available_capacity"] <= 0:
        return False
    if min_age is not None and slot["min_age_limit"] != min_age:
        return False
    if vaccine is not None and slot["vaccine"].upper() != vaccine.upper():
        return False
    return True


def publish_slots(preferred_solts, event_name, webhook_key):
    if len(preferred_solts) > 0:
        print("Final Slots found for publishing: {}".format(preferred_solts))
        url = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(event_name, webhook_key)
        first_slot = preferred_solts[0]
        district_name = "{} {}".format(first_slot["district_name"], first_slot["center_name"])
        print("Vaccine found in district: {}".format(district_name))
        try:
            requests.post(url,
                          data={"value1": first_slot["vaccine"], "value2": district_name, "value3": first_slot["date"]})
        except Exception as e:
            print("Unable to publish slots", e)
    else:
        print("No preferred slot found")


def lambda_handler(event, context):
    districts = {}
    for location in event["locations"]:
        state = location["state"]
        if "district" not in location.keys():
            print("Looking for all districts in {}".format(state))
            districts = {**districts, **STATES_MAP[state]["districts_map"]}
        else:
            district = location["district"]
            if district not in STATES_MAP[state]["districts_map"].keys():
                print("District not found. Available districts: {}".format(STATES_MAP[state]["districts_map"].keys()))
                exit(1)
            print("Looking for district: {} in {}".format(district, state))
            districts[district] = STATES_MAP[state]["districts_map"][district]

    vaccine_name = event.get("vaccine", None)
    if vaccine_name is not None and vaccine_name != "COVAXIN" and vaccine_name != "COVISHIELD":
        print("Incorrect vaccine name: {}. It should be either COVAXIN or COVISHIELD".format(vaccine_name))
        exit(1)

    age = event.get("age", None)
    if age < 45:
        age = 18
    else:
        age = 45

    days = event.get("days", 3)
    print("Looking for slots for vaccine: {}, age group: {}, for next {} weeks".format(vaccine_name, age, days))
    slots = fetch_slots_districts_days(districts, days, vaccine_name, age)

    if "IFTTT_WEBHOOK_EVENT_NAME" in event.keys() and "IFTTT_WEBHOOK_KEY" in event.keys():
        publish_slots(slots, event["IFTTT_WEBHOOK_EVENT_NAME"], event["IFTTT_WEBHOOK_KEY"])
    return {
        'statusCode': 200,
        'slots': slots
    }
