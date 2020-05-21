import json
import logging
import requests
import azure.functions as func
import os 
    
def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    message = event.subject
    registry=message.split(":")[0]
    version= message.split(":")[1]
    slack_message=":star::star:Image version: {version} pushed to {registry} :star::star:".format(version=version, registry=registry)
    data = []
    data.append({"type": "section","text": {"type": "mrkdwn","text": slack_message }, "accessory": { "type": "image", "image_url": "http://i.giphy.com/4AC11GmQzFVKg.gif", "alt_text": "Deployed image"}})
    slack_data = json.dumps({'blocks': data})
    logging.info('Python EventGrid trigger processed an event: %s', result)
    
    url = os.environ["SLACK_IMAGE_PUSH"]
    if event.event_type == "Microsoft.ContainerRegistry.ImagePushed":
        logging.info(message)
        r = requests.post(url, data=slack_data)
        logging.info(r.status_code)



