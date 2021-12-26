import stripe
from credit_pay.db_service.mongodb.mongo_service import MongoDBClient
from credit_pay.utilities.encryptor import Encryptor
from rest_framework import serializers


class StripeOrchestrator:
    def __init__(self):
        mongo_cl = MongoDBClient()
        sk_d = mongo_cl.get("stripe_data", {'type': "stripe_key"})
        self.sk = None if not sk_d else sk_d[0]["value"]
        stripe.api_key = Encryptor.decrypt(self.sk)

    def create_charge(self, params):
        charge_resp = stripe.Charge.create(capture=False, **params)
        return charge_resp

    def capture_charge(self, params):
        charge_id = params["charge_id"]
        del params["charge_id"]
        capture_resp = stripe.Charge.capture(charge_id, **params)
        return capture_resp

    def create_refund(self, params):
        try:
            charge_id = params["charge_id"]
            del params["charge_id"]
            refund_resp = stripe.Refund.create(charge_id, **params)
            return refund_resp
        except Exception as e:
            raise Exception("Refund failed " + str(e))

    def get_charges(self, params):
        charges_data = stripe.Charge.list(**params)
        return charges_data


# try:
#   # Use Stripe's library to make requests...
#   pass
# except stripe.error.CardError as e:
#   # Since it's a decline, stripe.error.CardError will be caught
#
#   print('Status is: %s' % e.http_status)
#   print('Code is: %s' % e.code)
#   # param is '' in this case
#   print('Param is: %s' % e.param)
#   print('Message is: %s' % e.user_message)
# except stripe.error.RateLimitError as e:
#   # Too many requests made to the API too quickly
#   pass
# except stripe.error.InvalidRequestError as e:
#   # Invalid parameters were supplied to Stripe's API
#   pass
# except stripe.error.AuthenticationError as e:
#   # Authentication with Stripe's API failed
#   # (maybe you changed API keys recently)
#   pass
# except stripe.error.APIConnectionError as e:
#   # Network communication with Stripe failed
#   pass
# except stripe.error.StripeError as e:
#   # Display a very generic error to the user, and maybe send
#   # yourself an email
#   pass
# except Exception as e:
#   # Something else happened, completely unrelated to Stripe
#   pass

class ErrorSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()

if __name__ == "__main__":
    pass
    # capture_resp = stripe.Charge.capture("ch_1JHPE9SBWV6CbihwSQUSzR3X")
    # print
    # charge_resp = stripe.Charge.create(
    #     amount=2000,
    #     currency="inr",
    #     source="tok_visa",
    #     description="My First Test Charge (created for API docs)",
    #     capture=False,
    # )
    # print("a")