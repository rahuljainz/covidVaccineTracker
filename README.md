# covidVaccineTracker
Easily usable python script to track covid vaccine and get notification on your mobile device

## How to setup notifications on mobile

1. Go to https://ifttt.com/ and sign up.
2. Note your IFTTT Webhook Service Key
    1. Navigate to https://ifttt.com/services/maker_webhooks/settings
    2. Under "Account Info" locate the "URL". It will look like: https://maker.ifttt.com/use/SOMESTRINGOFCHARACTERS
    3. Open that URL and copy your key. It should say "Your key is: SOMESTRINGOFCHARACTERS".
3. Create a webhook applet
    1. Click on "Create" button on top-right corner of https://ifttt.com/home
    2. Click on "Add" in front of "If this".
   3. Search for "Webhooks". Select "Receive a web request". Enter event name, say "vacineTracker" and note that event name.
      ![Screenshot](img/IFTTT%20trigger.jpg)
    4. Click on "Add" in front of "Then That".
    5. Search for "Notifications" and then select "Send a notification from the IFTTT app".
    6. In the message section, write this `The {{MakerWebhooks.event.Value1}} vaccine is available in  {{MakerWebhooks.event.Value2}} on {{MakerWebhooks.event.Value3}}`
      ![Screenshot](img/IFTTT%20action.jpg)    
   7. Submit and save the applet
      ![Screenshot](img/IFTTT%20applet.jpg)
   
4. Download the IFTTT app on your mobile device and login with same account.

## How to run the script

1. Open the file `main.py`
2. In the event, edit the details as per your need. Following is the details:
   
    `locations`: Represents the locations that needs to be searched for vaccine slot. As already configured in the script, you can either select complete state or a combination of state and district
   
    `vaccine`: Name of the vaccine to search for, i.e., COVAXIN or COVISHIELD. Leave empty, if you're searching for both.
   
    `age`: Enter the age of the person for which you're searching the vaccine
   
    `days`: No. of days to be looked for available slots
   
    `IFTTT_WEBHOOK_EVENT_NAME`: Event name that you created in applet in IFTTT
   
    `IFTTT_WEBHOOK_KEY`: IFTTT webhook key that you noted in step above.
3. Run the following command: `python main.py`

## How to run this file on AWS lambda

Create a lambda function from the file `constants.py` and `handler.py`. Configure the event object in `main.py` as input to your lambda function and schedule the function to run timely.