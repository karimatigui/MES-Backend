from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
import requests  # type: ignore
from Backend.utils.token_manager import get_mingle_token
from django.http import JsonResponse
from rest_framework import status
from Backend.models import IonAPICredentials
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password


@api_view(['GET'])
def get_dispatch_data(request):
    # Step 1: Get token
    username = request.query_params.get("username")

    token_response = requests.get('http://localhost:8000/api/get-token/')
    if token_response.status_code != 200:
        return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    access_token = token_response.json().get('access_token')

    # Step 2: Get company code dynamically
    company_response = requests.get('http://127.0.0.1:8000/api/get_ionapi_credential/')
    company_response.raise_for_status()
    company_code = company_response.json().get('company')

    if not company_code:
        return Response({'error': 'Company code missing in credentials'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Step 3: Prepare headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'X-Infor-LnCompany': company_code,
    }

    # Step 4: Fetch ACTIVE LIST to remove from dispatch
    active_response = requests.get(f'http://127.0.0.1:8000/api/get_operation_active_list/?username={username}')
    active_data = active_response.json() if active_response.status_code == 200 else []

    # Build a set of (Order, Operation)
    active_set = set(
        (item.get("Order"), item.get("Operation"))
        for item in active_data
    )

    # Step 5: Call dispatch API (with pagination)
    url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/tiapi.sfcProductionOrder/Operations?%24filter=OperationStatus%20eq%20tiapi.sfcProductionOrder.OperationStatus%27Active%27%20or%20OperationStatus%20eq%20tiapi.sfcProductionOrder.OperationStatus%27Started%27%20or%20OperationStatus%20eq%20tiapi.sfcProductionOrder.OperationStatus%27ReadyToStart%27'
    all_results = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch dispatch data'}, status=status.HTTP_502_BAD_GATEWAY)

        json_data = response.json()
        all_results.extend(json_data.get('value', []))
        url = json_data.get('@odata.nextLink')

    # Step 6: FILTER OUT ACTIVE OPERATIONS

    filtered_results = [
    item for item in all_results
    if (item.get("Order"), str(item.get("Operation"))) not in active_set
    ]


    # Step 7: Return final filtered dispatch list
    return Response(filtered_results, status=status.HTTP_200_OK)
