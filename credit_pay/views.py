from rest_framework import serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from credit_pay.credit_card_orchestrator.credit_orchestrator import CreditService

bad_request = 400


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def create_charge(request):
    params = request.data
    params["type"] = "create_charge"
    try:
        if "amount" not in params:
            raise Exception("amount is missing in the request")
        if "currency" not in params:
            raise Exception("currency missing in the request")
        if "source" not in params:
            raise Exception("source missing in the request")
        if "description" not in params:
            raise Exception("description missing in the request")
        charge_status = CreditService().create_charge(params)

        return charge_status

    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": bad_request}).data
        return Response(response, status=bad_request)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def capture_charge(request, charge_id):
    try:
        params = request.data
        params["charge_id"] = charge_id.replace(":", "")
        params["type"] = "capture_charge"
        capture_status = CreditService().capture_charge(params)
        return capture_status

    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": bad_request}).data
        return Response(response, status=bad_request)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def create_refund(request, charge_id):
    try:
        params = request.data
        params["charge_id"] = charge_id.replace(":", "")
        params["type"] = "create_refund"
        refund_status = CreditService().create_refund(params)
        return refund_status

    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": bad_request}).data
        return Response(response, status=bad_request)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def get_charges(request):
    try:
        params = {"type": "get_charge"}
        params.update(request.GET)
        charge_data = CreditService().get_charges(params)
        return charge_data
    except Exception as e:
        response = ErrorSerializer({"message": str(e), "code": bad_request}).data
        return Response(response, status=bad_request)


class ErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    code = serializers.CharField()


