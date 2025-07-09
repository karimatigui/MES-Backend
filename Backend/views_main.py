# # views.py
# from rest_framework.decorators import api_view # type: ignore
# from rest_framework.response import Response # type: ignore
# import requests  # type: ignore
# from Backend.utils.token_manager import get_mingle_token
# from django.http import JsonResponse
# from rest_framework import status
# from Backend.models import IonAPICredentials
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.hashers import make_password
# import json
# import string
# import random
# from .models import UserAccount
# import traceback
# from django.core.mail import send_mail




# @api_view(['GET'])
# def get_operations(request):
#     order_number = request.GET.get('order_number')
#     if not order_number:
#         return Response({"error": "Missing 'order_number' parameter"}, status=400)

#     url = (
#         f"https://mingle-ionapi.eu1.inforcloudsuite.com/"
#         f"LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/"
#         f"tiapi.sfcProductionOrder/Orders(Order='{order_number}')/OperationRefs"
#     )

#     try:
#         token = get_mingle_token()
#     except Exception as e:
#         return Response({"error": "Token fetch failed", "details": str(e)}, status=500)

#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Accept": "application/json",
#         "X-Infor-LnCompany": "5100",
#         "X-Infor-LnIdentity": "zumtech2"
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json().get("value", [])
#         return Response(data)
#     except requests.exceptions.HTTPError as http_err:
#         return Response({
#             "error": "HTTP error occurred",
#             "details": str(http_err),
#             "status_code": response.status_code,
#             "response_text": response.text,
#             "url": url
#         }, status=response.status_code)
#     except requests.exceptions.RequestException as e:
#         return Response({
#             "error": "Request failed",
#             "details": str(e)
#         }, status=500)
# # ----------------------------------------------------------------------------------------------
# @api_view(['GET'])
# def get_token(request):
#     try:
#         token = get_mingle_token()
#     except Exception as e:
#         return Response({"error": "Token fetch failed", "details": str(e)}, status=500)

#     return JsonResponse({'access_token': token})
# # ----------------------------------------------------------------------------------------------

# @api_view(['GET'])
# def get_dispatch_data(request):
#     # Step 1: Get token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     access_token = token_response.json().get('access_token')

#     # Step 2: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     # Step 3: Call Infor API (with pagination support)
#     url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/tiapi.sfcProductionOrder/Operations?%24filter=OperationStatus%20eq%20tiapi.sfcProductionOrder.OperationStatus%27Active%27%20or%20OperationStatus%20eq%20tiapi.sfcProductionOrder.OperationStatus%27Started%27%20or%20OperationStatus%20eq%20tiapi.sfcProductionOrder.OperationStatus%27ReadyToStart%27'
#     all_results = []

#     while url:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             return Response({'error': 'Failed to fetch dispatch data'}, status=status.HTTP_502_BAD_GATEWAY)

#         json_data = response.json()
#         all_results.extend(json_data.get('value', []))
#         url = json_data.get('@odata.nextLink')

#     return Response(all_results, status=status.HTTP_200_OK)

# # ------------------------------------------------------------------------------------
# @api_view(['GET'])
# def get_nc_data(request):
#     # Step 1: Get access token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     access_token = token_response.json().get('access_token')

#     # Step 2: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     # Step 3: Define base URL
#     url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/qmapi.ncmNonConformanceReport/NonConformanceReports'

#     # Step 4: Recursive fetch loop
#     all_results = []

#     while url:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             return Response({'error': 'Failed to fetch NC data from Infor', 'status': response.status_code}, status=status.HTTP_502_BAD_GATEWAY)

#         data = response.json()
#         all_results.extend(data.get('value', []))
#         url = data.get('@odata.nextLink')  # Move to next page if exists

#     # Step 5: Return combined results
#     return Response(all_results, status=status.HTTP_200_OK)

# # -------------------------------------------------------------------------------------------------------
# @api_view(['POST'])
# def post_nc(request):
#     payload = request.data

#     # Step 1: Get token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     access_token = token_response.json().get('access_token')

#     # Step 2: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     # Step 3: POST to Infor API
#     infor_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/qmapi.ncmNonConformanceReport/NonConformanceReports'

#     try:
#         response = requests.post(infor_url, json=payload, headers=headers)
#         response.raise_for_status()
#         return Response(response.json(), status=status.HTTP_201_CREATED)
#     except requests.exceptions.RequestException as e:
#         print("Error posting to Infor API:", e)
#         return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
# # ------------------------------------------------------------------------------------
# @api_view(['POST'])
# def complete_order(request):
#     # Step 1: Get token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     access_token = token_response.json().get('access_token')
#     Order = request.data.get('order_id')   

#     # Step 2: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#         'If-Match': '*',  # Added based on the UI showing If-Match field
#         'Content-Language': 'en-US'  # Added based on the UI showing Content-Language field
#     }
    
#     # Step 3: Format URL correctly - ensure proper URL encoding
#     base_url = "https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/"
#     # Use proper URL encoding for the order parameter
#     order_part = f"tiapi.sfcProductionOrder/Orders(Order='{Order}')"
#     action_part = "tiapi.sfcProductionOrder.Complete"
#     infor_url = f"{base_url}{order_part}/{action_part}"
    
#     # Use empty payload since this appears to be an action call
#     # From the UI, it seems this might not need a body payload
#     try:
#         response = requests.post(infor_url, headers=headers)
#         if response.status_code in [200, 201, 202, 204]:
#             # Some APIs return empty responses for success
#             try:
#                 return Response(response.json(), status=status.HTTP_200_OK)
#             except ValueError:  # JSON decoding failed
#                 return Response({"status": "success", "message": "Order completed"}, 
#                                status=response.status_code)
#         else:
#             error_detail = f"Error {response.status_code}: {response.text}"
#             # print(f"API Error: {error_detail}")
#             return Response({'error': error_detail}, 
#                            status=status.HTTP_502_BAD_GATEWAY)
#     except requests.exceptions.RequestException as e:
#         print("Error posting to Infor API:", e)
#         return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
# # ---------------------------------------------------------------------------------------
# @api_view(['GET'])
# def get_inventory(request):
#      # Get the token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     access_token = token_response.json().get('access_token')

#     # Call Infor API (still same URL internally)
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     infor_url ='https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/whapi.inrStockPointInventory/Inventory'

#     infor_response = requests.get(infor_url, headers=headers)

#     if infor_response.status_code != 200:
#         return Response({'error': 'Failed to fetch NC'}, status=status.HTTP_502_BAD_GATEWAY)

#     return Response(infor_response.json(), status=status.HTTP_200_OK)
# # -------------------------------------------------------------------------------------
# @api_view(['POST'])
# def report_operation(request):
#     try:
#         order_id = request.data['order_id']
#         operation = request.data['operation']
#         qty_deliver = request.data['qty_deliver']
#         qty_reject = request.data['qty_reject']
#         login_code = request.data.get('login_code', 'zumtech2')
#     except KeyError as e:
#         return Response({'error': f'Missing field: {e.args[0]}'}, status=400)

#     # Get access token from internal API
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=500)

#     access_token = token_response.json().get('access_token')
#     if not access_token:
#         return Response({'error': 'Token not found in response'}, status=500)

#     # Build SOAP payload
#     soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
#                   xmlns="http://www.infor.com/businessinterface/IWMStdReportOperation">
#   <soapenv:Header>
#     <Activation>
#       <company>5100</company>
#     </Activation>
#   </soapenv:Header>
#   <soapenv:Body>
#     <ReportOperation>
#       <ReportOperationRequest>
#         <DataArea>
#           <IWMStdReportOperation>
#             <LoginCode>{login_code}</LoginCode>
#             <Operation>{operation}</Operation>
#             <ProductionOrder>{order_id}</ProductionOrder>
#             <Complete>yes</Complete>
#             <QtyDeliver>{qty_deliver}</QtyDeliver>
#             <QtyReject>{qty_reject}</QtyReject>
#             <BackFlush>no</BackFlush>
#             <PostSubassyToInv>no</PostSubassyToInv>
#             <DirectProcessQuarantine>yes</DirectProcessQuarantine>
#           </IWMStdReportOperation>
#         </DataArea>
#       </ReportOperationRequest>
#     </ReportOperation>
#   </soapenv:Body>
# </soapenv:Envelope>"""

#     # SOAP service endpoint
#     soap_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/c4ws/services/IWMStdReportOperation'

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'text/xml;charset=UTF-8',
#         'Accept': 'text/xml',
#         'SOAPAction': 'ReportOperation'
#     }

#     try:
#         response = requests.post(soap_url, data=soap_payload.encode('utf-8'), headers=headers)
#         return Response({
#             'status': response.status_code,
#             'response': response.text
#         }, status=response.status_code)
#     except requests.exceptions.RequestException as e:
#         return Response({'error': str(e)}, status=502)
# # -----------------------------------------------------------------
# @api_view(['GET'])

# def get_operation_data(request):
#     order_number = request.GET.get("order_id")
#     operation = request.GET.get("operation")

#     if not order_number or not operation:
#         return Response({"error": "Missing 'order_number' parameter"}, status=400)

#     url = (
#         f"https://mingle-ionapi.eu1.inforcloudsuite.com/"
#         f"LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/"
#         f"tiapi.sfcProductionOrder/Operations(Order='{order_number}',Operation={operation})"
#     )

#     try:
#         token = get_mingle_token()
#     except Exception as e:
#         return Response({"error": "Token fetch failed", "details": str(e)}, status=500)

#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Accept": "application/json",
#         "X-Infor-LnCompany": "5100",
#         "X-Infor-LnIdentity": "zumtech2"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()

#         # Use entire response, don't assume "value"
#         data = response.json()
#         return Response(data)

#     except requests.exceptions.HTTPError as http_err:
#         return Response({
#             "error": "HTTP error occurred",
#             "details": str(http_err),
#             "status_code": response.status_code,
#             "response_text": response.text,
#             "url": url
#         }, status=response.status_code)
#     except requests.exceptions.RequestException as e:
#         return Response({
#             "error": "Request failed",
#             "details": str(e)
#         }, status=500)
    
# # ------------------------------------------------------------------------------------------------------
# @api_view(['POST'])
# def post_initiate_materials(request):
#     # Step 1: Get token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     access_token = token_response.json().get('access_token')
#     order_number = request.data.get('order_id')   
#     Position = request.data.get('position')   

#     # Step 2: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#         'If-Match': '*',  # Added based on the UI showing If-Match field
#         'Content-Language': 'en-US'  # Added based on the UI showing Content-Language field
#     }
#     # order_number = 'J60000010'
#     # Position = 10
#     # Step 3: Format URL correctly - ensure proper URL encoding
#     base_url = "https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/"
#     # Use proper URL encoding for the order parameter
#     order_part = f"tiapi.sfcProductionOrder/Materials(Order='{order_number}',Position={Position})"
#     action_part = "tiapi.sfcProductionOrder.InitiateInventoryIssue"
#     infor_url = f"{base_url}{order_part}/{action_part}"
    
  
#     # Use empty payload since this appears to be an action call
#     # From the UI, it seems this might not need a body payload
#     try:
#         response = requests.post(infor_url, headers=headers)
#         if response.status_code in [200, 201, 202, 204]:
#             # Some APIs return empty responses for success
#             try:
#                 return Response(response.json(), status=status.HTTP_200_OK)
#             except ValueError:  # JSON decoding failed
#                 return Response({"status": "success", "message": "Order completed"}, 
#                                status=response.status_code)
#         else:
#             error_detail = f"Error {response.status_code}: {response.text}"
#             # print(f"API Error: {error_detail}")
#             return Response({'error': error_detail}, 
#                            status=status.HTTP_502_BAD_GATEWAY)
#     except requests.exceptions.RequestException as e:
#         print("Error posting to Infor API:", e)
#         return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
# # -------------------------------------------------------------------------------------------------------------

# @api_view(['GET'])
# def get_materials(request):
#     order_number = request.GET.get("order_id")
#     operation = request.GET.get("operation")

#     if not order_number or not operation:
#         return Response({"error": "Missing 'order_number' parameter"}, status=400)

#     url = (
#         f"https://mingle-ionapi.eu1.inforcloudsuite.com/"
#         f"LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/"
#         f"/tiapi.sfcProductionOrder/Orders(Order='{order_number}')/MaterialRefs?%24filter=Operation%20eq%20{operation}&%24select=%2A"

#     )

#     try:
#         token = get_mingle_token()
#     except Exception as e:
#         return Response({"error": "Token fetch failed", "details": str(e)}, status=500)

#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Accept": "application/json",
#         "X-Infor-LnCompany": "5100",
#         "X-Infor-LnIdentity": "zumtech2"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()

#         # Use entire response, don't assume "value"
#         data = response.json()
#         return Response(data)

#     except requests.exceptions.HTTPError as http_err:
#         return Response({
#             "error": "HTTP error occurred",
#             "details": str(http_err),
#             "status_code": response.status_code,
#             "response_text": response.text,
#             "url": url
#         }, status=response.status_code)
#     except requests.exceptions.RequestException as e:
#         return Response({
#             "error": "Request failed",
#             "details": str(e)
#         }, status=500)
#     # ------------------------------------------------------
#     # get realted NC 
# @api_view(['GET'])
# def get_related_nc_data(request):
#     # Step 1: Get access token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response(
#             {'error': 'Failed to get token'},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

#     access_token = token_response.json().get('access_token')

#     # Step 2: Validate input parameters
#     order_number = request.GET.get("order_id")
#     operation = request.GET.get("operation")
#     # order_number = 'J10000045'
#     # operation = 10

#     if not order_number or not operation:
#         return Response(
#             {"error": "Missing 'order_id' or 'operation' parameter"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # Step 3: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     # Step 4: Construct initial URL
#     url = (
#         "https://mingle-ionapi.eu1.inforcloudsuite.com/"
#         "LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/"
#         f"qmapi.ncmNonConformanceReport/NonConformanceReports"
#         f"?$filter=OriginOrder eq '{order_number}' and Operation eq {operation}"
#         f"&$select=NonConformanceReport,NonConformingMaterialReportStatus"
#         f"&$orderby=NonConformanceReport"
#     )

#     # Step 5: Recursive pagination loop to fetch all results
#     all_results = []

#     while url:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             return Response(
#                 {'error': 'Failed to fetch NC data from Infor', 'status': response.status_code},
#                 status=status.HTTP_502_BAD_GATEWAY
#             )

#         data = response.json()
#         all_results.extend(data.get('value', []))
#         url = data.get('@odata.nextLink')  # Handle pagination

#     # Step 6: Return all fetched NC data
#     return Response(all_results, status=status.HTTP_200_OK)
# # ---------------------------------------------------------------------------------------
# # get realted NC 
# @api_view(['GET'])
# def get_items(request):
#     # Step 1: Get access token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response(
#             {'error': 'Failed to get token'},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

#     access_token = token_response.json().get('access_token')
#     # Step 3: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     # Step 4: Construct initial URL
#     url = "https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/LN/lnapi/odata/tcapi.ibdItem/Items"
    
#     all_results = []

#     while url:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             return Response(
#                 {'error': 'Failed to fetch NC data from Infor', 'status': response.status_code},
#                 status=status.HTTP_502_BAD_GATEWAY
#             )

#         data = response.json()
#         all_results.extend(data.get('value', []))
#         url = data.get('@odata.nextLink')  # Handle pagination

#     # Step 6: Return all fetched NC data
#     return Response(all_results, status=status.HTTP_200_OK)
# # ------------------------------------------------------------------------------------------------

# @api_view(['POST'])
# def post_nc_attachment(request):
#     payload = request.data

#     # Step 1: Get token
#     token_response = requests.get('http://localhost:8000/api/get-token/')
#     if token_response.status_code != 200:
#         return Response({'error': 'Failed to get token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     access_token = token_response.json().get('access_token')

#     # Step 2: Prepare headers
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'X-Infor-LnCompany': '5100',
#         'X-Infor-LnIdentity': 'zumtech2',
#     }

#     # Step 3: POST to Infor API
#     infor_url ="https://mingle-ionapi.eu1.inforcloudsuite.com/LDE4VNS7C63W3JGC_DEM/IDM/api/items"
#     try:
#         response = requests.post(infor_url, json=payload, headers=headers)
#         response.raise_for_status()
#         return Response(response.json(), status=status.HTTP_201_CREATED)
#     except requests.exceptions.RequestException as e:
#         print("Error posting to Infor API:", e)
#         return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
# # ------------------------------------------------------------------------------------


# @csrf_exempt  # Only for testing! In production, use CSRF protection
# def create_ionapi_credentials(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             credentials = IonAPICredentials(
#                 ti = data.get('ti', ''),
#                 cn = data.get('cn', ''),
#                 dt = data.get('dt', ''),
#                 ci = data.get('ci', ''),
#                 cs = data.get('cs', ''),
#                 iu = data.get('iu', ''),
#                 pu = data.get('pu', ''),
#                 oa = data.get('oa', ''),
#                 ot = data.get('ot', ''),
#                 or_field = data.get('or', ''),
#                 sc = data.get('sc', []),
#                 ev = data.get('ev', ''),
#                 v = data.get('v', ''),
#                 company = data.get('Company', '')
#             )
#             credentials.save()

#             return JsonResponse({
#                 'message': 'IonAPI credentials saved successfully!',
#                 'data': {
#                     'id': credentials.id,
#                     'cn': credentials.cn,
#                     'ti': credentials.ti
#                 }
#             }, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
# # -------------------------------------------------------
# def get_ionapi_credential(request):
#     if request.method == 'GET':
#         record = IonAPICredentials.objects.order_by('-created_at').first()
#         if record:
#             data = {
#                 'id': record.id,
#                 'ti': record.ti,
#                 'cn': record.cn,
#                 'dt': record.dt,
#                 'ci': record.ci,
#                 'cs': record.cs,
#                 'iu': record.iu,
#                 'pu': record.pu,
#                 'oa': record.oa,
#                 'ot': record.ot,
#                 'or': record.or_field,
#                 'sc': record.sc,
#                 'ev': record.ev,
#                 'v': record.v,
#                 'company': record.company,
#                 'created_at': record.created_at,
#             }
#             return JsonResponse(data)
#         else:
#             return JsonResponse({'error': 'No records found'}, status=404)
        
# # -----------------------------------------------------------------


# def generate_random_password(length=10):
#     chars = string.ascii_letters + string.digits + "!@#$%&*"
#     return ''.join(random.choices(chars, k=length))
# # ---------------------------------------------------------------------


# @csrf_exempt
# def create_user(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             email = data['email']

#             # ✅ Check if user already exists
#             if UserAccount.objects.filter(email=email).exists():
#                 return JsonResponse(
#                     {'error': f"A user with email '{email}' already exists."},
#                     status=409  # Conflict
#                 )
#             if UserAccount.objects.filter(username=data['username']).exists():
#                 return JsonResponse(
#                     {'error': 'Username already exists.'},
#                     status=409
#                 )

#             # Proceed to create user
#             plain_password = generate_random_password()
#             hashed_password = make_password(plain_password)

#             user = UserAccount.objects.create(
#                 username=data['username'],
#                 email=email,
#                 role=data['role'],
#                 language=data['language'],
#                 phone_number=data['phone_number'],
#                 password=hashed_password,
#             )

#             # ✅ Send email
#             subject = '✅ Your ZUM IT Account Login'
#             login_url = 'https://your-app.com/login'  # Customize this
#             message = f"""
# Hello {user.username},

# Welcome! Your account has been created successfully.

# 🔐 Your login credentials:
# - Username: {user.username}
# - Password: {plain_password}

# 🔗 Login here: {login_url}

# Please change your password after logging in.

# Best regards,  
# ZUM IT Team
# """
#             try:
#                 send_mail(
#                     subject,
#                     message,
#                     'karim01atigui@gmail.com',
#                     [email],
#                     fail_silently=False,
#                 )
#             except Exception as mail_error:
#                 print("❌ Failed to send email:", mail_error)
#                 return JsonResponse({'error': 'Email failed to send.'}, status=500)

#             return JsonResponse({
#                 'message': '✅ User created and email sent.',
#                 'username': user.username
#             }, status=201)

#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({'error': f'Server error: {str(e)}'}, status=400)

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)



# # ----------------------------------------------------------------

# def get_users(request):
#     if request.method == 'GET':
#         users = UserAccount.objects.all().values(
#             'id', 'username', 'email', 'role', 'language', 'phone_number', 'created_at','password'
#         )
#         return JsonResponse(list(users), safe=False)
#     return JsonResponse({'error': 'Only GET method allowed'}, status=405)
# # ------------------------------------------
# @csrf_exempt
# def delete_user(request, user_id):
#     if request.method == 'DELETE':
#         try:
#             user = UserAccount.objects.get(id=user_id)
#             user.delete()
#             return JsonResponse({'message': '✅ User deleted successfully.'}, status=200)
#         except UserAccount.DoesNotExist:
#             return JsonResponse({'error': 'User not found.'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

#     return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)

# # ---------------------------------
# @csrf_exempt
# def update_user(request, user_id):
#     if request.method == 'PUT':
#         try:
#             data = json.loads(request.body)
#             user = UserAccount.objects.get(id=user_id)

#             # Update fields
#             user.username = data.get('username', user.username)
#             user.email = data.get('email', user.email)
#             user.role = data.get('role', user.role)
#             user.language = data.get('language', user.language)
#             user.phone_number = data.get('phone_number', user.phone_number)

#             user.save()
#             return JsonResponse({'message': '✅ User updated successfully.'}, status=200)

#         except UserAccount.DoesNotExist:
#             return JsonResponse({'error': 'User not found.'}, status=404)
#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

#     return JsonResponse({'error': 'Only PUT method allowed'}, status=405)
