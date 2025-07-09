# views.py
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
import requests  # type: ignore
from Backend.utils.token_manager import get_mingle_token
from django.http import JsonResponse
from rest_framework import status
from Backend.models import IonAPICredentials
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password


@api_view(['POST'])
def report_operation(request):
    try:
        order_id = request.data['order_id']
        operation = request.data['operation']
        qty_deliver = request.data['qty_deliver']
        qty_reject = request.data['qty_reject']
        login_code = request.data.get('login_code', 'zumtech2')
    except KeyError as e:
        return Response({'error': f'Missing field: {e.args[0]}'}, status=400)

    # Get access token from internal API
    token_response = requests.get('http://localhost:8000/api/get-token/')
    if token_response.status_code != 200:
        return Response({'error': 'Failed to get token'}, status=500)

    access_token = token_response.json().get('access_token')
    if not access_token:
        return Response({'error': 'Token not found in response'}, status=500)
   # Step 2: Get company code dynamically
    company_response = requests.get('http://127.0.0.1:8000/api/get_ionapi_credential/')
    company_response.raise_for_status()
    company_code = company_response.json().get('company')

    if not company_code:
        return Response({'error': 'Company code missing in credentials'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Build SOAP payload
    soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns="http://www.infor.com/businessinterface/IWMStdReportOperation">
  <soapenv:Header>
    <Activation>
      <company>{company_code}</company>
    </Activation>
  </soapenv:Header>
  <soapenv:Body>
    <ReportOperation>
      <ReportOperationRequest>
        <DataArea>
          <IWMStdReportOperation>
            <LoginCode>{login_code}</LoginCode>
            <Operation>{operation}</Operation>
            <ProductionOrder>{order_id}</ProductionOrder>
            <Complete>yes</Complete>
            <QtyDeliver>{qty_deliver}</QtyDeliver>
            <QtyReject>{qty_reject}</QtyReject>
            <BackFlush>no</BackFlush>
            <PostSubassyToInv>no</PostSubassyToInv>
            <DirectProcessQuarantine>yes</DirectProcessQuarantine>
          </IWMStdReportOperation>
        </DataArea>
      </ReportOperationRequest>
    </ReportOperation>
  </soapenv:Body>
</soapenv:Envelope>"""

    # SOAP service endpoint
    soap_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/c4ws/services/IWMStdReportOperation'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/xml;charset=UTF-8',
        'Accept': 'text/xml',
        'SOAPAction': 'ReportOperation'
    }

    try:
        response = requests.post(soap_url, data=soap_payload.encode('utf-8'), headers=headers)
        return Response({
            'status': response.status_code,
            'response': response.text
        }, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=502)