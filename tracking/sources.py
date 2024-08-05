from rest_framework.response import Response
from .models import *
from .serializers import *
import datetime
import json
import xmltodict
import requests


def get_gati(data, res, request):
    docket_no = DeliveryChallan.objects.filter(trucklist_id_id=data['truck_id'], is_active=True).values('lrn_no')[0][
        'lrn_no']
    try:
        url = "https://justi.gati.com/webservices/GatiKWEDktJTrack.jsp?p1=" + docket_no + "&p2=" + res['token_param']
        response = requests.get(url)
        response = response.json()
        obj = response['Gatiresponse']['dktinfo'][0]['TRANSIT_DTLS']
        queryset = TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id'])
        record_count = queryset.count()
        TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=3)
        if "Delivered" in obj[0]['INTRANSIT_STATUS']:
            gati_date = obj[0]['INTRANSIT_DATE'] + ' ' + obj[0]['INTRANSIT_TIME']
            gati_date = datetime.datetime.strptime(gati_date, "%d-%b-%Y %H:%M")
            filter_data = LogisticsDaTruckList.objects.filter(truckListID_id=data['truck_id']).values_list('daID_id',
                                                                                                           flat=True)
            DispatchInstruction.objects.filter(da_id__in=filter_data).update(status="Delivered", da_status_number=9)
            truck_list = TruckList.objects.filter(truckListId=data['truck_id'])
            truck_list.update(tracking_status=4, status='Delivered', delivered_datetime=gati_date)

        if record_count != 0:
            DeliveryDetails.objects.filter(trucklist_id_id=data['truck_id']).delete();
            for x in obj:
                gati_date = x['INTRANSIT_DATE'] + ' ' + x['INTRANSIT_TIME']
                gati_date = datetime.datetime.strptime(gati_date, "%d-%b-%Y %H:%M")
                TruckDeliveryDetails.objects.create(
                    trucklist_id_id=data['truck_id'],
                    current_datetime=gati_date,
                    current_location=x['INTRANSIT_LOCATION'],
                    current_status=x['INTRANSIT_STATUS'],
                    current_latitude=None,
                    current_longitude=None,
                    is_active=True,
                    created_by_id=request.user.id)
        if record_count == 0:
            for x in obj:
                gati_date = x['INTRANSIT_DATE'] + ' ' + x['INTRANSIT_TIME']
                gati_date = datetime.datetime.strptime(gati_date, "%d-%b-%Y %H:%M")
                TruckDeliveryDetails.objects.create(
                    trucklist_id_id=data['truck_id'],
                    current_datetime=gati_date,
                    current_location=x['INTRANSIT_LOCATION'],
                    current_status=x['INTRANSIT_STATUS'],
                    current_latitude=None,
                    current_longitude=None,
                    is_active=True,
                    created_by_id=request.user.id)

        TruckList.objects.filter(truckListId=data['truck_id']).update(status=obj[0]['INTRANSIT_STATUS'])
    except Exception as e:
        return Response(e)


def get_arc(data, res, request):
    vehicle_no = TruckList.objects.filter(truckListId=data['truck_id'], is_active=True).values('vehicle_no')[0][
        'vehicle_no']
    try:
        url = "http://35.154.134.64/webservice?token=" + \
              res['token_param'] + "&user=" + res['user_param'] + "&pass=" + \
              res['pass_param'] + "&vehicle_no=" + \
              vehicle_no + "&format=json"
        response = requests.get(url)
        response = response.json()
        obj = response['root']['VehicleData'][0]
        TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=3)
        arc_date = obj['Datetime']
        date_string = arc_date.strftime("%d-%m-%Y %H:%M:%S")
        arc_date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        # table creations
        TruckDeliveryDetails.objects.create(
            trucklist_id_id=data['truck_id'],
            current_datetime=arc_date,
            current_location=obj['Location'],
            current_status=obj['Status'],
            current_latitude=obj['Latitude'],
            current_longitude=obj['Longitude'],
            is_active=True,
            created_by_id=request.user.id)

        TruckList.objects.filter(truckListId=data['truck_id']).update(status=obj['Status'])
        if "Delivered" in obj['Status']:
            filter_data = LogisticsDaTruckList.objects.filter(truckListID_id=data['truck_id']).values_list('daID_id',
                                                                                                           flat=True)
            DispatchInstruction.objects.filter(da_id__in=filter_data).update(status="Delivered", da_status_number=9)
            TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=4)
    except Exception as e:
        return Response(e)


def saraswati_logistic(data, res, request):
    try:
        vehicle_no = TruckList.objects.filter(truckListId=data['truck_id'], is_active=True)
        vehicle_no = vehicle_no.values('vehicle_no')[0]['vehicle_no']
        # fetch data
        url = "https://track.cxipl.com/api/v2/phone-tracking/doc-latest-location?vehicleNumber=" + vehicle_no
        headers = {"Content-type": "application/json", "authkey": "UB1CNQLKU32LPCFQJ2NGL7YY1E51HYF6"}
        response = requests.get(url, headers=headers, verify=False)
        response = response.json()
        obj = response['data']
        TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=3)
        saraswati_date = obj['timeStamp'].split('T')[0] + ' ' + obj['timeStamp'].split('T')[1]
        saraswati_date = saraswati_date.split('.')[0]
        # if LogisticsTruckDeliveryDetails already exists but longitude and latitude is different  create new record
        queryset = TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id'], is_active=True)

        if queryset.count() != 0:
            queryset = TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id'], is_active=True)
            queryset = queryset.values('current_latitude', 'current_longitude')
            new = queryset[0]['current_latitude'] != obj['latitude'] and queryset[0]['current_longitude'] != obj[
                'longitude']
            if new:
                pass
            else:
                TruckDeliveryDetails.objects.create(
                    trucklist_id_id=data['truck_id'],
                    current_datetime=saraswati_date,
                    current_location=obj['locationInfo']['city'] + ', ' + obj['locationInfo']['state'],
                    current_status="Transit",
                    current_latitude=obj['latitude'],
                    current_longitude=obj['longitude'], is_active=True,
                    created_by_id=request.user.id)
                return Response({
                    "message": "Sarawati Data Created Successfully for new location",
                    "status": True
                })
        if queryset.count() == 0:
            TruckDeliveryDetails.objects.create(
                trucklist_id_id=data['truck_id'],
                current_datetime=saraswati_date,
                current_location=obj['locationInfo']['city'] + ', ' + obj['locationInfo']['state'],
                current_status="Transit", current_latitude=obj['latitude'],
                current_longitude=obj['longitude'], is_active=True,
                created_by_id=request.user.id)
            return Response({
                "message": "Sarawati Data Created Successfully",
                "status": True
            })
    except Exception as e:
        return Response(e)


def safe_express(data, res, request):
    try:
        doc_no = DeliveryChallan.objects.filter(truck_list=data['truck_id'], is_active=True)
        doc_no = doc_no.values('lrn_no')[0]['lrn_no']
        doc_no = '100002891346'
        doc_type = "WB"
        url = "https://webs.safexpress.com:8443/SafexWaybillTracking/webresources/tracking/all"
        payload = json.dumps({"docNo": doc_no, "docType": doc_type})
        headers = {'Content-Type': "application/json", 'Cache-Control': "no-cache", }
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        response = response.json()
        obj = response['shipment']['tracking']
        # return Response(obj)
        queryset = TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id'])
        record_count = queryset.count()
        TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=3)
        status = []  # assign
        date = None
        for i in obj:
            if i['status'] == 'DELIVERED':
                status.append(i['status'])
                date = i['date']
                break

        if "Delivered" in status or "DELIVERED" in status:
            date = datetime.datetime.strptime(date, "%d-%b-%Y %I:%M:%S %p")
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            delivered_datetime = date
            filter_data = LogisticsDaTruckList.objects.filter(truckListID_id=data['truck_id']).values_list('daID_id',
                                                                                                           flat=True)
            DispatchInstruction.objects.filter(da_id__in=filter_data).update(status="Delivered", da_status_number=9)
            truck_list = TruckList.objects.filter(truckListId=data['truck_id'])
            truck_list.update(tracking_status=4, status='Delivered', delivered_datetime=date)

        if record_count != 0:
            TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id']).delete();
            for x in obj:
                objs = []
                safe_date = datetime.datetime.strptime(x['date'], '%d-%b-%Y %I:%M:%S %p')
                objs.append(TruckDeliveryDetails(
                    trucklist_id_id=data['truck_id'],
                    current_datetime=safe_date,
                    current_location=x['description'].split()[-1],
                    current_status=x['status'], current_latitude=None,
                    current_longitude=None, is_active=True,
                    created_by_id=request.user.id)
                )
                TruckDeliveryDetails.objects.bulk_create(objs)

        if record_count == 0:
            for x in obj:
                objs = []
                safe_date = datetime.datetime.strptime(x['date'], '%d-%b-%Y %I:%M:%S %p')
                objs.append(LogisticsTruckDeliveryDetails(
                    trucklist_id_id=data['truck_id'],
                    current_datetime=safe_date,
                    current_location=x['description'].split()[-1],
                    current_status=x['status'], current_latitude=None,
                    current_longitude=None, is_active=True,
                    created_by_id=request.user.id)
                )

                TruckDeliveryDetails.objects.bulk_create(objs)
    except requests.exceptions.ConnectionError as e:
        return Response(data={"error": "OOPS !Connection Error"})

    except IndexError as e:
        return Response(data={"error": "OOPS ! Document Number is not valid"})

    except Exception as e:
        return Response(e)


def safe_expresss(data, res, request):
    try:
        doc_no = DeliveryChallan.objects.filter(trucklist_id_id=data['truck_id'], is_active=True)
        doc_no = doc_no.values('lrn_no')[0]['lrn_no']
        doc_type = "WB"
        url = "https://webs.safexpress.com:8443/SafexWaybillTracking/webresources/tracking/all"
        payload = json.dumps({"docNo": doc_no, "docType": doc_type})
        headers = {'Content-Type': "application/json", 'Cache-Control': "no-cache", }
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        response = response.json()
        obj = response['shipment']['tracking']
        # Data manipulation
        queryset = TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id'])
        record_count = queryset.count()
        TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=3)
        status = []
        date = None
        for i in obj:
            if i['status'] == 'DELIVERED':
                status.append(i['status'])
                date = i['date']
                break

        if "Delivered" in status or "DELIVERED" in status:
            # date = datetime.strptime(i['date'], '%d-%b-%Y %I:%M:%S %p')
            if date is not None:
                date = date.datetime.strptime(date, "%d-%b-%Y %I:%M:%S %p")
                date = date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                date = ''
            filter_data = LogisticsDaTruckList.objects.filter(truckListID_id=data['truck_id']).values_list('daID_id',
                                                                                                           flat=True)
            DispatchInstruction.objects.filter(da_id__in=filter_data).update(status="Delivered", da_status_number=9)
            truck_list = TruckList.objects.filter(truckListId=data['truck_id'])
            truck_list.update(tracking_status=4, status="Delivered", delivered_datetime=date)

        if record_count != 0:
            for count, x in enumerate(obj, start=1):
                if count > record_count:
                    objs = []
                    safe_date = datetime.datetime.strptime(x['date'], '%d-%b-%Y %I:%M:%S %p')
                    objs.append(TruckDeliveryDetails(
                        trucklist_id_id=data['truck_id'],
                        current_datetime=safe_date,
                        current_location=x['description'], current_status=x['status'],
                        current_latitude=None, current_longitude=None, is_active=True,
                        created_by_id=request.user.id)
                    )
                    TruckDeliveryDetails.objects.bulk_create(objs)

        if record_count == 0:
            for x in obj:
                objs = []
                safe_date = datetime.datetime.strptime(x['date'], '%d-%b-%Y %I:%M:%S %p')
                objs.append(TruckDeliveryDetails(
                    trucklist_id_id=data['truck_id'],
                    current_datetime=safe_date,
                    current_location=x['description'], current_status=x['status'],
                    current_latitude=None, current_longitude=None, is_active=True,
                    created_by_id=request.user.id))
                LogisticsTruckDeliveryDetails.objects.bulk_create(objs)

    except requests.exceptions.ConnectionError as e:
        return Response(data={"error": "OOPS !Connection Error"})

    except IndexError as e:
        return Response(data={"error": "OOPS ! Document Number is not valid"})
    except Exception as e:
        return Response(e)


def tci_express(data, res, request):
    try:
        consignment_no = None
        consignment_no = "288607465"
        if DeliveryChallan.objects.filter(trucklist_id_id=data['truck_id'], is_active=True).exists():
            consignment_no = DeliveryChallan.objects.filter(trucklist_id_id=data['truck_id'], is_active=True)
            consignment_no = consignment_no.values('lrn_no')[0]['lrn_no']
        # third party API calling
        res = {'user_param': 'AAACY0840P', 'pass_param': 'YIL@1234'}
        url = "https://customerapi.tciexpress.in/ServiceEnquire.asmx"
        headers = {'Content-type': 'text/xml'}
        xml_request = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><getConsignmentResponseMessage xmlns="http://www.tciexpress.in/"><pConsignmentNumber>' + \
                      consignment_no + '</pConsignmentNumber><pUserProfile><UserID>' + \
                      res['user_param'] + '</UserID><Password>' + res['pass_param'] + \
                      '</Password></pUserProfile></getConsignmentResponseMessage></soap:Body></soap:Envelope>'
        response = requests.post(url, xml_request, headers=headers, verify=False)
        response = xmltodict.parse(response.text)
        res = response['soap:Envelope']['soap:Body']['getConsignmentResponseMessageResponse']
        print('res',res)
        TruckList.objects.filter(truckListId=data['truck_id']).update(tracking_status=3)
        result = []

        for key in res.keys(): result.append(key)
        if any("getConsignmentResponseMessageResult" in s for s in result):
            obj = response['soap:Envelope']['soap:Body']['getConsignmentResponseMessageResponse']['getConsignmentResponseMessageResult']['ResponseMessage']['Consignment']['Message']
            val = list(obj)
            queryset = TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id'])
            record_count = queryset.count()
            # check the data availability
            if "Delivered" in val[-1]['EventDescription']:
                delivery_datetime = datetime.datetime.strptime(val[-1]['EventDate'] + ' ' + val[-1]['EventTime'],
                                                               '%d/%m/%Y %H:%M')
                filter_data = LogisticsDaTruckList.objects.filter(truckListID_id=data['truck_id']).values_list(
                    'daID_id', flat=True)
                DispatchInstruction.objects.filter(da_id__in=filter_data).update(status="Delivered", da_status_number=9)
                truck_list = TruckList.objects.filter(truckListId=data['truck_id'])
                filter_data.update(tracking_status=4, status="Delivered", delivered_datetime=delivery_datetime)
            if record_count != 0:
                TruckDeliveryDetails.objects.filter(trucklist_id_id=data['truck_id']).delete();
                for x in val:
                    objs = []
                    tci_date = x['EventDate']
                    tci_time = x['EventTime']
                    combined = tci_date + ' ' + tci_time
                    tci_date = date.datetime.strptime(combined, '%d/%m/%Y %H:%M')
                    objs.append(TruckDeliveryDetails(
                        trucklist_id_id=data['truck_id'],
                        current_datetime=tci_date,
                        current_location=x['EventPlace'],
                        current_status=x['EventDescription'], current_latitude=None,
                        current_longitude=None, is_active=True,
                        created_by_id=request.user.id))
                    TruckDeliveryDetails.objects.bulk_create(objs)

            if record_count == 0:
                for x in val:
                    objs = []
                    tci_date = x['EventDate']
                    tci_time = x['EventTime']
                    combined = tci_date + ' ' + tci_time
                    tci_date = datetime.datetime.strptime(combined, '%d/%m/%Y %H:%M')
                    objs.append(TruckDeliveryDetails(
                        trucklist_id_id=data['truck_id'],
                        current_datetime=tci_date,
                        current_location=x['EventPlace'],
                        current_status=x['EventDescription'], current_latitude=None,
                        current_longitude=None, is_active=True,
                        created_by_id=request.user.id))
                    TruckDeliveryDetails.objects.bulk_create(objs)

    except IndexError as e:
        return Response(data={"error": "OOPS !Consignment Number not found"})
    except Exception as e:
        return Response(str(e))
