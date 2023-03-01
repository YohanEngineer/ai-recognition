import paho.mqtt.client as mqtt
import logging
import base64
from io import BytesIO
from PIL import Image
import recognition


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def check_meeting_reservation(plate='AA-100-BB', tag='00-tag-00') :
    print('TO DO in other package')

def check_meeting(is_meeting_coming) :
    if is_meeting_coming :
        publish('OK', 'access-answer-topic')
    else :
        publish('KO','access-answer-topic')

def check_license_plate(decoded_image):
    license_plate, score = recognition.detect_number_plate('data/')
    print(license_plate)
    is_meeting_coming = check_meeting_reservation(plate=license_plate)
    check_meeting(is_meeting_coming)

def check_nfc_tag(tag):
    is_meeting_coming = check_meeting_reservation(tag=tag)
    check_meeting(is_meeting_coming)


def decoding_image(encoded_image):
    # Decode the base64 string into bytes
    decoded_bytes = base64.urlsafe_b64decode(encoded_image)
    # Open the bytes data as an image using PIL
    image = Image.open(BytesIO(decoded_bytes))
    # Display the image
    image.show()
    # Save the image to a file
    image.save("decoded_image.jpg")

    return image


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))
    client.subscribe("licence-plate-topic")
    client.subscribe("nfc-request-topic")



def on_message(client, userdata, msg):
    if msg.topic == 'licence-plate-topic' :
        logging.info('Image received from topic: ' + msg.topic)
        # encoded_image = str(msg.payload)
        # if encoded_image.startswith("b'data:image/jpeg;base64,"):
        #     logging.info(encoded_image.split("base64,")[1])
        #     decoded_image = decoding_image(encoded_image.split("base64,")[1])
        #     check_license_plate(decoded_image)
        # else:
        #     logging.info('Error with the image received.')
        check_license_plate('')

    if msg.topic == 'nfc-request-topic' :
        logging.info('NFC tag received from topic: ' + msg.topic)
        tag = str(msg.payload)
        check_nfc_tag(tag)


def publish(message, topic):
    logging.info("Publishing message : " + message + ' on topic : ' + topic)
    client.publish(topic, message)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.31.254.21", 72, 60)

client.loop_forever()
