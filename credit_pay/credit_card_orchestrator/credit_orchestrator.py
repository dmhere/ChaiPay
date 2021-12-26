# from restapi.db_service.mongodb.mongo_service import MongoDBClient
import json
from rest_framework.response import Response
from credit_pay.db_service.mongodb.mongo_service import MongoDBClient
from credit_pay.stripe_orchestrator.stripe_orchestrator import StripeOrchestrator
import datetime

OK_STATUS = 200
CREATED = 201
NOT_FOUND = 404
UNAUTHORISED = 401
FORBIDDEN = 403


def audit_decorator(func):
    mongo_cl = MongoDBClient()

    def audit(ref, params):
        date = datetime.datetime.now()
        params["date_time"] = date
        mongo_cl.save(CreditService.credit_data, params, date_time=date)
        del params["date_time"]
        del params["type"]
        return func(ref, params)

    return audit


class CreditService:
    import os
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'config.json')
    with open(file_path, 'r') as f:
        __collection_details = json.load(f)['collections']
        pass
    credit_data = "credit_data"

    def __init__(self):
        self.s_orch = StripeOrchestrator()

    @audit_decorator
    def create_charge(self, params):
        try:

            charge_resp = self.s_orch.create_charge(params)
            return Response(charge_resp, CREATED)
        except Exception as e:
            raise Exception("Charge creation failed " + str(e))

    @audit_decorator
    def capture_charge(self, params):
        try:
            capture_resp = self.s_orch.capture_charge(params)
            return Response(capture_resp, CREATED)

        except Exception as e:
            raise Exception("Charge capture failed " + str(e))

    @audit_decorator
    def create_refund(self,params):
        try:
            refund_resp = self.s_orch.capture_charge(params)
            return Response(refund_resp, CREATED)
        except Exception as e:
            raise Exception("Refund failed " + str(e))

    @audit_decorator
    def get_charges(self, params):
        try:
            charges_resp = self.s_orch.get_charges(params)
            return Response(charges_resp, CREATED)
        except Exception as e:
            raise Exception("Charge fetch failed - " + str(e))




if __name__ == "__main__":
  pass


