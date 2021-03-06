import logging
from models.messaging import Messaging

from payloads.disband_measure_information_payload import DisbandMeasureInformationPayload
from repositories import PressureRepository
from python_client.disband.openapi_client.model.pressure import Pressure
from python_client.disband.openapi_client.model.measure_dto import MeasureDTO

class DisbandActionDisbandMacPressure:

    def __init__(self, config, topic, configBack):
        self.messenger = Messaging(config, topic, self.action)
        self.messenger.loop_start()
        self.repository = PressureRepository(configBack)
    
    def action(self, client, userdata, msg):
        jsonString = msg.payload.decode('utf-8')
        logging.info('Received json: ' + jsonString)
        disbandMeasureInformationPayload = DisbandMeasureInformationPayload.from_json(jsonString)
        self.save_data(disbandMeasureInformationPayload)

    def save_data(self, payload: DisbandMeasureInformationPayload):
        measureDTO = MeasureDTO(payload.disbandMac, data = payload.data, date = payload.sentAt)
        self.repository.save(measureDTO)