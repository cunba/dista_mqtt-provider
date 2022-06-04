import logging
from models.messaging import Messaging

from payloads.disband_measure_information_payload import DisbandMeasureInformationPayload
from repositories import OxygenRepository
from python_client import Oxygen
from python_client import MeasureDTO

class DisbandActionDisbandMacOxygen:

    def __init__(self, config, topic):
        self.messenger = Messaging(config, topic, self.action)
        self.messenger.loop_start()
    
    def action(self, client, userdata, msg):
        jsonString = msg.payload.decode('utf-8')
        print(str(client))
        print(str(userdata))
        print(str(msg))
        logging.info('Received json: ' + jsonString)
        disbandMeasureInformationPayload = DisbandMeasureInformationPayload.from_json(jsonString)
        logging.info('Received message: ' + str(disbandMeasureInformationPayload))

    def save_data(self, disbandMac, payload):
        measureDTO = MeasureDTO(payload.get('data'), payload.get('date'), disbandMac)
        OxygenRepository.save(measureDTO)