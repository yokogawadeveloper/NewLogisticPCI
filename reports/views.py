import datetime
import os
from io import BytesIO
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from xhtml2pdf import pisa
from tracking.serializers import *
from .serializers import *


# Create your views here.

class DispatchReportViewSet(viewsets.ModelViewSet):
    queryset = DispatchInstruction.objects.all()
    serializer_class = DispatchInstructionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='dispatch_report')
    def dispatch_report(self, request, *args, **kwargs):
        try:
            filter_data = request.data['data_filter']
            date_type = request.data['date_type']
            date_flag = request.data['date_flag']
            date_from = request.data['date_from']
            date_to = request.data['date_to']
            if date_flag:
                type_filter = date_type + '__range'
                truck_request = DispatchInstruction.objects.filter(**filter_data).filter(
                    **{type_filter: [date_from, date_to]})
            else:
                truck_request = DispatchInstruction.objects.filter(**filter_data)
            serializer = DispatchInstructionSerializer(truck_request, many=True)
            for data in serializer.data:
                data['no_of_boxes'] = BoxDetails.objects.filter(dil_id=data['dil_id'], main_box=True).count()
                data['packing_cost'] = BoxDetails.objects.filter(dil_id=data['dil_id']).aggregate(total=Sum('price'))[
                    'total']
                data['billing_value'] = \
                    DispatchBillDetails.objects.filter(dil_id=data['dil_id']).aggregate(
                        total=Sum('total_amount_with_tax'))[
                        'total']
                data['sap_invoice_amount'] = 0
                data['transportation_cost'] = 0
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='dispatch_instruction_pdf')
    def dispatch_instruction_pdf(self, request):
        dil = DispatchInstruction.objects.get(dil_id=request.data['dil_id'])
        response_data = {
            'dil_id': dil.dil_id,
            'dil_no': dil.dil_no,
            'dil_date': dil.dil_date,
            'so_no': dil.so_no,
            'po_no': dil.po_no,
            'master_list': []
        }
        for master_item in dil.master_list.all():
            master_item_data = {
                'item_id': master_item.item_id,
                'item_no': master_item.item_no,
                'material_description': master_item.material_description,  # corrected field name
                'material_no': master_item.material_no,
                'ms_code': master_item.ms_code,
                'quantity': master_item.quantity,
                'linkage_no': master_item.linkage_no,
                'inline_items': []
            }
        # Create PDF file
        html_template = get_template('dispatch_export.html')
        html = html_template.render({'response_data': response_data})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="dispatch_instruction.pdf"'
            # Save the file
            media_path = os.path.join(settings.MEDIA_ROOT, "dispatch_export")
            if not os.path.exists(media_path):
                os.makedirs(media_path)
            file_path = os.path.join(media_path, "dispatch_instruction_{0}.pdf".format(dil.dil_no))
            with open(file_path, "wb") as file:
                file.write(response.getvalue())
            return response
        return HttpResponse("Error rendering PDF", status=400)


class BoxDetailsReportViewSet(viewsets.ModelViewSet):
    queryset = BoxDetails.objects.all()
    serializer_class = BoxDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    @action(methods=['post'], detail=False, url_path='box_details_report')
    def box_details_report(self, request, *args, **kwargs):
        try:
            filter_data = request.data['data_filter']
            date_type = request.data['date_type']
            date_flag = request.data['date_flag']
            date_from = request.data['date_from']
            date_to = request.data['date_to']
            main_box = request.data['main_box']
            # Combine filters for DispatchInstruction
            dispatch_filters = {**filter_data}
            if date_flag and date_type != 'box_created_date':
                dispatch_filters[date_type + '__range'] = [date_from, date_to]
            dispatch = DispatchInstruction.objects.filter(**dispatch_filters)
            # Get the box details
            if date_flag and date_type == 'box_created_date':
                box_details = BoxDetails.objects.filter(dil_id__in=dispatch).filter(
                    created_at__range=[date_from, date_to], main_box=main_box)
            else:
                box_details = BoxDetails.objects.filter(dil_id__in=dispatch, main_box=main_box)
            # Serialize the data
            serializer = BoxDetailSerializer(box_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PackingListPDFViewSet(viewsets.ModelViewSet):
    queryset = BoxDetails.objects.all()
    serializer_class = PackingListPDFBoxDetailsSerializer

    @action(detail=False, methods=['post'], url_path="packing_list_pdf_based_box_code")
    def packing_list_pdf_based_box_code(self, request):
        data = request.data
        box_details = BoxDetails.objects.filter(box_code=data['box_code']).first()

        if not box_details:
            return Response({'error': 'Box not found'}, status=404)

        # Ensure all attributes are handled to avoid NoneType errors
        box_code = box_details.box_code if box_details.box_code is not None else 'N/A'
        height = box_details.height if box_details.height is not None else 0
        length = box_details.length if box_details.length is not None else 0
        breadth = box_details.breadth if box_details.breadth is not None else 0
        net_weight = box_details.net_weight if box_details.net_weight is not None else 0
        gross_weight = box_details.gross_weight if box_details.gross_weight is not None else 0
        box_serial_no = box_details.box_serial_no if box_details.box_serial_no is not None else ''

        response_data = [{
            'box_no_manual': box_code,
            'volume': f'{int(height)}\"x{int(length)}\"x{int(breadth)}\"',
            'net_weight': net_weight,
            'gross_weight': gross_weight,
            'box_serial_no': box_serial_no,
            'item_packing': []
        }]

        # Fetch Dispatch instruction data
        dispatch = DispatchInstruction.objects.get(dil_id=box_details.dil_id.dil_id)

        # Get list of item packing
        count_box_details = BoxDetails.objects.filter(parent_box=box_code).count()
        if count_box_details > 1:
            filter_data = BoxDetails.objects.filter(parent_box=box_code, main_box=False).values_list('box_code',
                                                                                                     flat=True)
        else:
            filter_data = BoxDetails.objects.filter(parent_box=box_code).values_list('box_code', flat=True)
        box_data = BoxDetails.objects.filter(box_code__in=filter_data)

        # Serializer for box details
        box_serializer = BoxDetailSerializer(box_data, many=True, context={'request': request})
        box_serializer_data = box_serializer.data

        # Serializer for item packing
        item_packing_data = ItemPacking.objects.filter(box_code__in=filter_data)
        item_packing_serializer = ItemPackingSerializer(item_packing_data, many=True, context={'request': request})
        item_serializer_data = item_packing_serializer.data

        # Fetch new box details if box_item_flag is true
        new_box_details = BoxDetails.objects.filter(box_code=data['box_code'], box_item_flag=True).values_list(
            'box_code', flat=True)
        new_item_packing_data = ItemPacking.objects.filter(box_code__in=new_box_details)
        new_item_packing_serializer = ItemPackingSerializer(new_item_packing_data, many=True,
                                                            context={'request': request})
        new_item_packing_serializer_data = new_item_packing_serializer.data

        # Combine item packing data with box details
        for box in box_serializer_data:
            item_list = []
            for item in item_serializer_data:
                if box['box_code'] == item['box_code']:
                    for inline_item in item['item_packing_inline']:
                        inline_item['box_no_manual'] = box['box_no_manual']
                    item_list.append(item)
                    new_item_packing_serializer_data.append(item)
            response_data[0]['item_packing'] = new_item_packing_serializer_data

        # Create a buffer to hold the PDF data
        # return Response(response_data)
        buffer = BytesIO()
        width, height = A4
        x_gap = 10  # Define the gap for x-axis

        def draw_header(canvas, page_number, total_pages):
            canvas.setFont("Helvetica-Bold", 12)
            logo_path = os.path.join(settings.MEDIA_ROOT, "images", "yokogawa_logo.jpg")
            canvas.drawImage(logo_path, inch, height - inch - 30, width=150, height=30)
            canvas.drawString(6 * inch, height - inch, "Packing List")
            canvas.setFont("Helvetica", 9)
            company_info = [
                "Yokogawa India Limited",
                "Plot No.96, Electronic City Complex, Hosur Road",
                "Bangalore-560100, India",
                "State Name & Code: Karnataka-29 India",
                "Phone: +91-80-2852-1100",
            ]
            text_object = canvas.beginText(inch, height - 2 * inch)
            for line in company_info:
                text_object.textLine(line)
            canvas.drawText(text_object)

            doc_info = [
                f"DO No: {dispatch.dil_no}",
                f"DO Date: {dispatch.dil_date}",
                f"SO No: {dispatch.so_no}",
                f"PO No: {dispatch.po_no.split()[0]}",
            ]
            text_object = canvas.beginText(6 * inch, height - 2 * inch)
            for line in doc_info:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, height - 2.8 * inch, width - inch, height - 2.8 * inch)

            page_no_info = f"Page {page_number} of {total_pages}"
            canvas.drawString(6 * inch, height - 2.7 * inch, page_no_info)

        def shipment_header(canvas, y_position):
            canvas.setFont("Helvetica", 7)
            ship_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(inch, y_position + 15, "SHIP TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(inch, y_position)
            for line in ship_to:
                text_object.textLine(line)
            canvas.drawText(text_object)

            bill_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawString(4 * inch, y_position + 15, "BILL TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(4 * inch, y_position)  # Adjusted x position to 3.5 * inch
            for line in bill_to:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, y_position - 0.8 * inch, width - inch, y_position - 0.8 * inch)

        def draw_footer(canvas, page_number, total_pages):
            canvas.setFont("Helvetica", 10)
            footer_text = f"Page {page_number} of {total_pages}"
            canvas.drawString(inch, inch / 2, footer_text)

        def draw_wrapped_string(canvas, x, y, text, max_width):
            if text is None:
                text = ''
            words = text.split()
            lines = []
            line = ""
            for word in words:
                if canvas.stringWidth(line + word) <= max_width:
                    line += word + " "
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())
            for line in lines:
                canvas.drawString(x, y, line)
                y -= 12
            return y

        def draw_content(canvas, y_position, page_number, total_pages):
            canvas.setFont("Helvetica", 8)
            canvas.setFont("Helvetica-Bold", 8)
            y_position -= 20
            dispatch_header = [
                'Model Description',
                'MS Code',
                'Linkage No',
                'Customer PO Sl No',
                'Customer Part No',
            ]
            y_position -= 10
            canvas.drawString(inch, y_position, "Packing Id")
            text_object = canvas.beginText(2 * inch + x_gap, y_position)
            for dil_header in dispatch_header:
                text_object.textLine(dil_header)
            canvas.drawText(text_object)
            canvas.drawString(5 * inch + x_gap, y_position, "Quantity/Quantity Unit")

            # Draw a line based on the header
            canvas.line(inch, y_position - 10 * 5, width - inch, y_position - 10 * 5)

            # data binding for content
            canvas.setFont("Helvetica", 8)
            y_position -= 20 * 2
            for datas in response_data:
                y_position -= 25  # Adjust for box spacing
                if y_position < inch:
                    canvas.showPage()
                    page_number += 1
                    draw_header(canvas, page_number, total_pages)
                    draw_footer(canvas, page_number, total_pages)
                    y_position = height - 3 * inch

                canvas.setFont("Helvetica-Bold", 9)
                draw_wrapped_string(canvas, inch, y_position, datas['box_no_manual'], 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 10, str(datas['volume']), 4 * inch)
                canvas.setFont("Helvetica", 7)
                draw_wrapped_string(canvas, inch, y_position - 20, "NT W/T:" + str(datas['net_weight']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 30, "GR W/T:" + str(datas['gross_weight']), 4 * inch)
                # draw_wrapped_string(canvas, inch, y_position - 40, "Box No:" + str(datas['box_serial_no']), 4 * inch)
                canvas.setFont("Helvetica", 8)
                for item_packing in datas['item_packing']:
                    if y_position < inch:
                        canvas.showPage()
                        page_number += 1
                        draw_header(canvas, page_number, total_pages)
                        draw_footer(canvas, page_number, total_pages)
                        y_position = height - 3 * inch
                    canvas.setFont("Helvetica", 8)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('material_description', ''),
                                                     4 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('linkage_no', ''), 4 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('ms_code', ''), 2 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, "Cust PO  SI No: " + (
                            item_packing['item_ref_id'].get('customer_po_sl_no', '') or ''), 2 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, "Cust Part No: " + (
                            item_packing['item_ref_id'].get('customer_po_item_code', '') or ''), 2 * inch)
                    canvas.drawString(5 * inch + x_gap + 10, y_position + 50,
                                      str(item_packing.get('item_qty', '')) + " ST")
                    canvas.setFont("Helvetica", 8)
                    y_position -= 20  # Adjust for item packing spacing
                    for inline_item_packing in item_packing.get('item_packing_inline', []):
                        if y_position < inch:
                            canvas.showPage()
                            page_number += 1
                            draw_header(canvas, page_number, total_pages)
                            draw_footer(canvas, page_number, total_pages)
                            y_position = height - 3 * inch

                        text_object = canvas.beginText(2 * inch + x_gap, y_position)

                        # Set font to Courier for serial_no and tag_no
                        canvas.setFont("Courier", 7)
                        text_object.textLine(f"S/N=  {inline_item_packing.get('serial_no', '')}")
                        text_object.textLine(f"TAG=  {inline_item_packing.get('tag_no', '')}")
                        text_object.textLine(f"Box=  {inline_item_packing.get('box_no_manual', '')}")
                        canvas.drawText(text_object)
                        canvas.setFont("Helvetica", 8)
                        y_position -= 30  # Adjust for inline item spacing

                    canvas.setDash(3, 3)
                    canvas.line(inch, y_position, width - inch, y_position)
                    canvas.setDash()
                    y_position -= 20  # Adjust for dash line spacing

            return y_position, page_number

        # First pass: Create a PDF and count the pages
        temp_buffer = BytesIO()
        c = canvas.Canvas(temp_buffer, pagesize=A4)

        def first_pass_pdf():
            page_number = 1
            y_position = height - 3 * inch
            draw_header(c, page_number, 0)  # Total pages is 0 for now
            y_position -= 0.4 * inch  # Adjust y_position for shipment_header
            shipment_header(c, y_position)
            y_position -= 0.8 * inch  # Adjust y_position after shipment_header
            y_position, page_number = draw_content(c, y_position, page_number, 0)
            draw_footer(c, page_number, 0)

            while y_position < inch:
                c.showPage()
                page_number += 1
                draw_header(c, page_number, 0)  # Total pages is 0 for now
                y_position = height - 3 * inch
                y_position, page_number = draw_content(c, y_position, page_number, 0)
                draw_footer(c, page_number, 0)

            c.save()
            return page_number

        total_pages = first_pass_pdf()

        # Second pass: Create the final PDF with correct page numbers
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        def second_pass_pdf():
            page_number = 1
            y_position = height - 3 * inch
            draw_header(c, page_number, total_pages)
            y_position -= 0.4 * inch  # Adjust y_position for shipment_header
            shipment_header(c, y_position)
            y_position -= 0.8 * inch  # Adjust y_position after shipment_header
            y_position, page_number = draw_content(c, y_position, page_number, total_pages)
            draw_footer(c, page_number, total_pages)

            while y_position < inch:
                c.showPage()
                page_number += 1
                draw_header(c, page_number, total_pages)
                y_position = height - 3 * inch
                y_position, page_number = draw_content(c, y_position, page_number, total_pages)
                draw_footer(c, page_number, total_pages)

            c.save()

        second_pass_pdf()

        # Send the PDF to the client
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="dispatch_instruction.pdf"'
        response.write(buffer.getvalue())
        media_path = os.path.join(settings.MEDIA_ROOT, "packing_export")
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        file_path = os.path.join(media_path, f"packing_list_{data['box_code']}.pdf")
        with open(file_path, "wb") as file:
            file.write(buffer.getvalue())
        return response

    @action(detail=False, methods=['post'], url_path="packing_list_pdf_based_dispatch")
    def packing_list_pdf_based_dispatch(self, request):
        data = request.data
        dispatch = DispatchInstruction.objects.get(dil_id=data['dil_id'])
        box_details = BoxDetails.objects.filter(dil_id=data['dil_id'], main_box=True)
        box_details_length = len(box_details)

        response_data = []  # Initialize response_data
        iteration = 0

        for boxs in box_details:
            iteration += 1
            box_code = boxs.box_code if boxs.box_code is not None else 'N/A'
            height = boxs.height if boxs.height is not None else 0
            length = boxs.length if boxs.length is not None else 0
            breadth = boxs.breadth if boxs.breadth is not None else 0
            net_weight = boxs.net_weight if boxs.net_weight is not None else 0
            gross_weight = boxs.gross_weight if boxs.gross_weight is not None else 0
            box_serial_no = boxs.box_serial_no if boxs.box_serial_no is not None else ''
            pagination = str(box_details_length) + "/" + str(iteration)

            box_data_entry = {
                'box_no_manual': box_code,
                'volume': f'{int(height)}\"x{int(length)}\"x{int(breadth)}\"',
                'net_weight': net_weight,
                'gross_weight': gross_weight,
                'box_no': box_serial_no,
                'pagination': pagination,
                'item_packing': []
            }

            # Get list of item packing
            count_box_details = BoxDetails.objects.filter(parent_box=box_code).count()
            if count_box_details > 1:
                filter_data = BoxDetails.objects.filter(parent_box=box_code, main_box=False).values_list('box_code',
                                                                                                         flat=True)
            else:
                filter_data = BoxDetails.objects.filter(parent_box=box_code).values_list('box_code', flat=True)

            # Serializer for box details
            box_data = BoxDetails.objects.filter(box_code__in=filter_data)
            box_serializer = BoxDetailSerializer(box_data, many=True, context={'request': request})
            box_serializer_data = box_serializer.data

            # Serializer for item packing
            item_packing_data = ItemPacking.objects.filter(box_code__in=filter_data)
            item_packing_serializer = ItemPackingSerializer(item_packing_data, many=True, context={'request': request})
            item_serializer_data = item_packing_serializer.data

            # Fetch new box details if box_item_flag is true
            new_box_details = BoxDetails.objects.filter(box_code=box_code, box_item_flag=True).values_list('box_code',
                                                                                                           flat=True)
            new_item_packing_data = ItemPacking.objects.filter(box_code__in=new_box_details)
            new_item_packing_serializer = ItemPackingSerializer(new_item_packing_data, many=True,
                                                                context={'request': request})
            new_item_packing_serializer_data = new_item_packing_serializer.data

            # Combine item packing data with box details
            for box in box_serializer_data:
                item_list = []
                for item in item_serializer_data:
                    if box['box_code'] == item['box_code']:
                        for inline_item in item['item_packing_inline']:
                            inline_item['box_no_manual'] = box['box_no_manual']
                        item_list.append(item)
                        new_item_packing_serializer_data.append(item)
                box_data_entry['item_packing'] = new_item_packing_serializer_data
            response_data.append(box_data_entry)  # Append to response_data

        response = response_data[::-1]
        # return Response(response_data)

        # PDF Creation main logic
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        x_gap = 10  # Define the gap for x-axis

        def draw_header(canvas, page_number, total_pages):
            canvas.setFont("Helvetica-Bold", 12)
            logo_path = os.path.join(settings.MEDIA_ROOT, "images", "yokogawa_logo.jpg")
            canvas.drawImage(logo_path, inch, height - inch - 30, width=150, height=30)
            canvas.drawString(6 * inch, height - inch, "Packing List")
            canvas.setFont("Helvetica", 9)
            company_info = [
                "Yokogawa India Limited",
                "Plot No.96, Electronic City Complex, Hosur Road",
                "Bangalore-560100, India",
                "State Name & Code: Karnataka-29 India",
                "Phone: +91-80-2852-1100",
            ]
            text_object = canvas.beginText(inch, height - 2 * inch)
            for line in company_info:
                text_object.textLine(line)
            canvas.drawText(text_object)

            doc_info = [
                f"DO No: {dispatch.dil_no}",
                f"DO Date: {dispatch.dil_date}",
                f"SO No: {dispatch.so_no}",
                f"PO No: {dispatch.po_no.split()[0]}",
            ]
            text_object = canvas.beginText(6 * inch, height - 2 * inch)
            for line in doc_info:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, height - 2.8 * inch, width - inch, height - 2.8 * inch)

            page_no_info = f"Page {page_number} of {total_pages}"
            canvas.drawString(6 * inch, height - 2.7 * inch, page_no_info)

        def shipment_header(canvas, y_position):
            canvas.setFont("Helvetica", 7)
            ship_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(inch, y_position + 15, "SHIP TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(inch, y_position)
            for line in ship_to:
                text_object.textLine(line)
            canvas.drawText(text_object)

            bill_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawString(4 * inch, y_position + 15, "BILL TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(4 * inch, y_position)  # Adjusted x position to 3.5 * inch
            for line in bill_to:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, y_position - 0.8 * inch, width - inch, y_position - 0.8 * inch)

        def draw_footer(canvas, page_number, total_pages):
            canvas.setFont("Helvetica", 10)
            footer_text = f"Page {page_number} of {total_pages}"
            canvas.drawString(inch, inch / 2, footer_text)

        def draw_wrapped_string(canvas, x, y, text, max_width):
            if text is None:
                text = ''
            words = text.split()
            lines = []
            line = ""
            for word in words:
                if canvas.stringWidth(line + word) <= max_width:
                    line += word + " "
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())
            for line in lines:
                canvas.drawString(x, y, line)
                y -= 12
            return y

        def draw_content(canvas, y_position, page_number, total_pages):
            processed_box_codes = set()  # Track processed box codes
            canvas.setFont("Helvetica", 8)
            canvas.setFont("Helvetica-Bold", 8)
            y_position -= 20
            dispatch_header = [
                'Model Description',
                'MS Code',
                'Linkage No',
                'Customer PO Sl No',
                'Customer Part No',
            ]
            y_position -= 10
            canvas.drawString(inch, y_position, "Packing Id")
            text_object = canvas.beginText(2 * inch + x_gap, y_position)
            for dil_header in dispatch_header:
                text_object.textLine(dil_header)
            canvas.drawText(text_object)
            canvas.drawString(5 * inch + x_gap, y_position, "Quantity/Quantity Unit")

            # Draw a line based on the header
            canvas.line(inch, y_position - 10 * 5, width - inch, y_position - 10 * 5)

            # data binding for content
            canvas.setFont("Helvetica", 8)
            y_position -= 20 * 2
            for datas in response:
                box_code = datas['box_no_manual']
                if box_code in processed_box_codes:
                    continue  # Skip this box_code if already processed
                processed_box_codes.add(box_code)  # Mark this box_code as processed
                y_position -= 25  # Adjust for box spacing
                if y_position < inch:
                    canvas.showPage()
                    page_number += 1
                    draw_header(canvas, page_number, total_pages)
                    draw_footer(canvas, page_number, total_pages)
                    y_position = height - 3 * inch

                canvas.setFont("Helvetica-Bold", 9)
                draw_wrapped_string(canvas, inch, y_position, datas['box_no_manual'], 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 10, str(datas['volume']), 4 * inch)
                canvas.setFont("Helvetica", 7)
                draw_wrapped_string(canvas, inch, y_position - 20, "NT W/T:" + str(datas['net_weight']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 30, "GR W/T:" + str(datas['gross_weight']), 4 * inch)
                # draw_wrapped_string(canvas, inch, y_position - 40, "Box No:" + str(datas['box_no']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 40, "Box No:" + str(datas['pagination']), 4 * inch)
                canvas.setFont("Helvetica", 8)
                item_packing_list = datas['item_packing'] if 'item_packing' in datas else []
                for item_packing in item_packing_list:
                    if y_position < inch:
                        canvas.showPage()
                        page_number += 1
                        draw_header(canvas, page_number, total_pages)
                        draw_footer(canvas, page_number, total_pages)
                        y_position = height - 3 * inch
                    canvas.setFont("Helvetica", 8)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, item_packing['item_name'],
                                                     4 * inch)
                    canvas.drawString(5 * inch + x_gap + 10, y_position + 10,
                                      str(item_packing.get('item_qty', '')) + " ST")
                    canvas.setFont("Helvetica", 8)
                    y_position -= 20  # Adjust for item packing spacing
                    for inline_item_packing in item_packing.get('item_packing_inline', []):
                        if y_position < inch:
                            canvas.showPage()
                            page_number += 1
                            draw_header(canvas, page_number, total_pages)
                            draw_footer(canvas, page_number, total_pages)
                            y_position = height - 3 * inch

                        text_object = canvas.beginText(2 * inch + x_gap, y_position)

                        # Set font to Courier for serial_no and tag_no
                        canvas.setFont("Courier", 7)
                        text_object.textLine(f"S/N=  {inline_item_packing.get('serial_no', '')}")
                        text_object.textLine(f"TAG=  {inline_item_packing.get('tag_no', '')}")
                        text_object.textLine(f"Box=  {inline_item_packing.get('box_no_manual', '')}")
                        canvas.drawText(text_object)
                        canvas.setFont("Helvetica", 8)
                        y_position -= 30  # Adjust for inline item spacing

                    canvas.setDash(3, 3)
                    canvas.line(inch, y_position, width - inch, y_position)
                    canvas.setDash()
                    y_position -= 20  # Adjust for dash line spacing

            return y_position, page_number

        # Initialize the PDF creation
        y_position = height - 2 * inch
        page_number = 1
        total_pages = 1
        # Draw the first page header, shipment header, footer, and content
        draw_header(p, page_number, total_pages)
        shipment_header(p, y_position - 30 * 3)
        draw_footer(p, page_number, total_pages)
        y_position, page_number = draw_content(p, y_position - 150, page_number,
                                               total_pages)  # Adjust y_position for shipment header height

        # Finalize the PDF creation
        p.showPage()
        p.save()

        # Save the PDF to the file system
        media_path = os.path.join(settings.MEDIA_ROOT, "packing_export")
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        file_path = os.path.join(media_path, f"dispatch_packing_summary_{dispatch.dil_id}.pdf")
        with open(file_path, "wb") as file:
            file.write(buffer.getvalue())

        # Send the PDF to the client
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="dispatch_packing_list_{dispatch.dil_id}.pdf"'
        buffer.seek(0)
        response.write(buffer.getvalue())

        return response

    @action(detail=False, methods=['post'], url_path="working_packing_list_pdf_based_box_code")
    def working_packing_list_pdf_based_box_code(self, request):
        data = request.data
        box_details = BoxDetails.objects.filter(box_code=data['box_code']).first()
        count_box_details = BoxDetails.objects.filter(parent_box=data['box_code']).count()
        box_details_length = BoxDetails.objects.filter(dil_id=box_details.dil_id.dil_id, main_box=True).count()

        if not box_details:
            return Response({'error': 'Box not found'}, status=404)

        dispatch = DispatchInstruction.objects.get(dil_id=box_details.dil_id.dil_id)

        # Ensure all attributes are handled to avoid NoneType errors
        box_code = box_details.box_code if box_details.box_code is not None else 'N/A'
        height = box_details.height if box_details.height is not None else 0
        length = box_details.length if box_details.length is not None else 0
        breadth = box_details.breadth if box_details.breadth is not None else 0
        net_weight = box_details.net_weight if box_details.net_weight is not None else 0
        gross_weight = box_details.gross_weight if box_details.gross_weight is not None else 0
        box_serial_no = box_details.box_serial_no if box_details.box_serial_no is not None else ''
        box_no = str(box_details.box_serial_no) + "/" + str(box_details_length)

        response_data = [{
            'box_no_manual': box_code,
            'volume': f'{int(height)}\"x{int(length)}\"x{int(breadth)}\"',
            'net_weight': net_weight,
            'gross_weight': gross_weight,
            'box_serial_no': box_serial_no,
            'box_no': box_no,
            'item_packing': []
        }]

        # Get Box Details
        if count_box_details > 1:
            filter_data = BoxDetails.objects.filter(parent_box=data['box_code'], main_box=False).values_list('box_code',
                                                                                                             flat=True)
        else:
            filter_data = BoxDetails.objects.filter(parent_box=data['box_code']).values_list('box_code', flat=True)

        box_data = BoxDetails.objects.filter(box_code__in=filter_data)

        # Serializer for box details
        box_serializer = BoxDetailSerializer(box_data, many=True, context={'request': request})
        box_serializer_data = box_serializer.data

        # Serializer for item packing
        item_packing_data = ItemPacking.objects.filter(box_code__in=filter_data)
        item_packing_serializer = ItemPackingSerializer(item_packing_data, many=True, context={'request': request})
        item_serializer_data = item_packing_serializer.data

        # Fetch new box details if box_item_flag is true
        new_box_details = BoxDetails.objects.filter(box_code=data['box_code'], box_item_flag=True).values_list(
            'box_code', flat=True)
        new_item_packing_data = ItemPacking.objects.filter(box_code__in=new_box_details)
        new_item_packing_serializer = ItemPackingSerializer(new_item_packing_data, many=True,
                                                            context={'request': request})
        new_item_packing_serializer_data = new_item_packing_serializer.data

        # Combine item packing data with box details
        for box in box_serializer_data:
            item_list = []
            for item in item_serializer_data:
                if box['box_code'] == item['box_code']:
                    if box['main_box'] == False:
                        for item_packing_inline in item['item_packing_inline']:
                            item_packing_inline['box_no_manual'] = box['box_no_manual']
                    item_list.append(item)
                    new_item_packing_serializer_data.append(item)
            response_data[0]['item_packing'] = new_item_packing_serializer_data

        # Create a buffer to hold the PDF data
        # return Response(response_data)
        buffer = BytesIO()
        width, height = A4
        x_gap = 10  # Define the gap for x-axis

        def draw_header(canvas, page_number, total_pages):
            canvas.setFont("Helvetica-Bold", 12)
            logo_path = os.path.join(settings.MEDIA_ROOT, "images", "yokogawa_logo.jpg")
            canvas.drawImage(logo_path, inch, height - inch - 30, width=150, height=30)
            canvas.drawString(6 * inch, height - inch, "Packing List")
            canvas.setFont("Helvetica", 9)
            company_info = [
                "Yokogawa India Limited",
                "Plot No.96, Electronic City Complex, Hosur Road",
                "Bangalore-560100, India",
                "State Name & Code: Karnataka-29 India",
                "Phone: +91-80-2852-1100",
            ]
            text_object = canvas.beginText(inch, height - 2 * inch)
            for line in company_info:
                text_object.textLine(line)
            canvas.drawText(text_object)

            doc_info = [
                f"DO No: {dispatch.dil_no}",
                f"DO Date: {dispatch.dil_date}",
                f"SO No: {dispatch.so_no}",
                f"PO No: {dispatch.po_no.split()[0]}",
            ]
            text_object = canvas.beginText(6 * inch, height - 2 * inch)
            for line in doc_info:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, height - 2.8 * inch, width - inch, height - 2.8 * inch)

            page_no_info = f"Page {page_number} of {total_pages}"
            canvas.drawString(6 * inch, height - 2.7 * inch, page_no_info)

        def shipment_header(canvas, y_position):
            canvas.setFont("Helvetica", 7)
            ship_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(inch, y_position + 15, "SHIP TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(inch, y_position)
            for line in ship_to:
                text_object.textLine(line)
            canvas.drawText(text_object)

            bill_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawString(4 * inch, y_position + 15, "BILL TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(4 * inch, y_position)  # Adjusted x position to 3.5 * inch
            for line in bill_to:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, y_position - 0.8 * inch, width - inch, y_position - 0.8 * inch)

        def draw_footer(canvas, page_number, total_pages):
            canvas.setFont("Helvetica", 10)
            footer_text = f"Page {page_number} of {total_pages}"
            canvas.drawString(inch, inch / 2, footer_text)

        def draw_wrapped_string(canvas, x, y, text, max_width):
            if text is None:
                text = ''
            words = text.split()
            lines = []
            line = ""
            for word in words:
                if canvas.stringWidth(line + word) <= max_width:
                    line += word + " "
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())
            for line in lines:
                canvas.drawString(x, y, line)
                y -= 12
            return y

        def draw_content(canvas, y_position, page_number, total_pages):
            canvas.setFont("Helvetica", 8)
            canvas.setFont("Helvetica-Bold", 8)
            y_position -= 20
            dispatch_header = [
                'Model Description',
                'MS Code',
                'Linkage No',
                'Customer PO Sl No',
                'Customer Part No',
            ]
            y_position -= 10
            canvas.drawString(inch, y_position, "Packing Id")
            text_object = canvas.beginText(2 * inch + x_gap, y_position)
            for dil_header in dispatch_header:
                text_object.textLine(dil_header)
            canvas.drawText(text_object)
            canvas.drawString(5 * inch + x_gap, y_position, "Quantity/Quantity Unit")

            # Draw a line based on the header
            canvas.line(inch, y_position - 10 * 5, width - inch, y_position - 10 * 5)

            # data binding for content
            canvas.setFont("Helvetica", 8)
            y_position -= 20 * 2
            for datas in response_data:
                y_position -= 25  # Adjust for box spacing
                if y_position < inch:
                    canvas.showPage()
                    page_number += 1
                    draw_header(canvas, page_number, total_pages)
                    draw_footer(canvas, page_number, total_pages)
                    y_position = height - 3 * inch

                canvas.setFont("Helvetica-Bold", 9)
                draw_wrapped_string(canvas, inch, y_position, datas['box_no_manual'], 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 10, str(datas['volume']), 4 * inch)
                canvas.setFont("Helvetica", 7)
                draw_wrapped_string(canvas, inch, y_position - 20, "NT W/T:" + str(datas['net_weight']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 30, "GR W/T:" + str(datas['gross_weight']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 40, "Box No:" + str(datas['box_no']), 4 * inch)
                canvas.setFont("Helvetica", 8)
                for item_packing in datas['item_packing']:
                    if y_position < inch:
                        canvas.showPage()
                        page_number += 1
                        draw_header(canvas, page_number, total_pages)
                        draw_footer(canvas, page_number, total_pages)
                        y_position = height - 3 * inch
                    canvas.setFont("Helvetica", 8)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('material_description', ''),
                                                     4 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('linkage_no', ''), 4 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('ms_code', ''), 2 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, "Cust PO  SI No: " + (
                                item_packing['item_ref_id'].get('customer_po_sl_no', '') or ''), 2 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, "Cust Part No: " + (
                                item_packing['item_ref_id'].get('customer_po_item_code', '') or ''), 2 * inch)
                    canvas.drawString(5 * inch + x_gap + 10, y_position + 50,
                                      str(item_packing.get('item_qty', '')) + " ST")
                    canvas.setFont("Helvetica", 8)
                    y_position -= 20  # Adjust for item packing spacing
                    count = 0
                    for inline_item_packing in item_packing.get('item_packing_inline', []):
                        if count == 3:  # Move to next line after 4 items
                            y_position -= 30
                            count = 0
                        if y_position < inch:
                            canvas.showPage()
                            page_number += 1
                            draw_header(canvas, page_number, total_pages)
                            draw_footer(canvas, page_number, total_pages)
                            y_position = height - 3 * inch

                        text_object = canvas.beginText(2 * inch + 5 + (count * 2 * inch), y_position)
                        canvas.setFont("Courier", 7)
                        text_object.textLine(f"S/N=  {inline_item_packing.get('serial_no', '')}")
                        text_object.textLine(f"TAG=  {inline_item_packing.get('tag_no', '')}")
                        text_object.textLine(f"Box=  {inline_item_packing.get('box_no_manual', '')}")
                        canvas.drawText(text_object)
                        canvas.setFont("Helvetica", 8)
                        count += 1  # Increment counter

                    canvas.setDash(3, 3)
                    y_position -= 30
                    canvas.line(inch, y_position, width - inch, y_position)
                    canvas.setDash()
                    y_position -= 20  # Adjust for dash line spacing

            return y_position, page_number

        # First pass: Create a PDF and count the pages

        temp_buffer = BytesIO()
        c = canvas.Canvas(temp_buffer, pagesize=A4)

        def first_pass_pdf():
            page_number = 1
            y_position = height - 3 * inch
            draw_header(c, page_number, 0)  # Total pages is 0 for now
            y_position -= 0.4 * inch  # Adjust y_position for shipment_header
            shipment_header(c, y_position)
            y_position -= 0.8 * inch  # Adjust y_position after shipment_header
            y_position, page_number = draw_content(c, y_position, page_number, 0)
            draw_footer(c, page_number, 0)

            while y_position < inch:
                c.showPage()
                page_number += 1
                draw_header(c, page_number, 0)  # Total pages is 0 for now
                y_position = height - 3 * inch
                y_position, page_number = draw_content(c, y_position, page_number, 0)
                draw_footer(c, page_number, 0)

            c.save()
            return page_number

        total_pages = first_pass_pdf()

        # Second pass: Create the final PDF with correct page numbers
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        def second_pass_pdf():
            page_number = 1
            y_position = height - 3 * inch
            draw_header(c, page_number, total_pages)
            y_position -= 0.4 * inch  # Adjust y_position for shipment_header
            shipment_header(c, y_position)
            y_position -= 0.8 * inch  # Adjust y_position after shipment_header
            y_position, page_number = draw_content(c, y_position, page_number, total_pages)
            draw_footer(c, page_number, total_pages)

            while y_position < inch:
                c.showPage()
                page_number += 1
                draw_header(c, page_number, total_pages)
                y_position = height - 3 * inch
                y_position, page_number = draw_content(c, y_position, page_number, total_pages)
                draw_footer(c, page_number, total_pages)

            c.save()

        second_pass_pdf()

        # Send the PDF to the client
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="dispatch_instruction.pdf"'
        response.write(buffer.getvalue())
        media_path = os.path.join(settings.MEDIA_ROOT, "packing_export")
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        file_path = os.path.join(media_path, f"packing_list_{data['box_code']}.pdf")
        with open(file_path, "wb") as file:
            file.write(buffer.getvalue())
        return response

    @action(detail=False, methods=['post'], url_path="working_packing_list_pdf_based_dispatch")
    def working_packing_list_pdf_based_dispatch(self, request):
        data = request.data
        dispatch = DispatchInstruction.objects.get(dil_id=data['dil_id'])
        box_details = BoxDetails.objects.filter(dil_id=data['dil_id'], main_box=True)
        box_details_length = len(box_details)

        response_data = []  # Initialize response_data
        iteration = 0

        for boxs in box_details:
            iteration += 1
            box_code = boxs.box_code if boxs.box_code is not None else 'N/A'
            height = boxs.height if boxs.height is not None else 0
            length = boxs.length if boxs.length is not None else 0
            breadth = boxs.breadth if boxs.breadth is not None else 0
            net_weight = boxs.net_weight if boxs.net_weight is not None else 0
            gross_weight = boxs.gross_weight if boxs.gross_weight is not None else 0
            box_serial_no = boxs.box_serial_no if boxs.box_serial_no is not None else ''
            pagination = str(iteration) + "/" + str(box_details_length)

            box_data_entry = {
                'box_no_manual': box_code,
                'volume': f'{int(height)}\"x{int(length)}\"x{int(breadth)}\"',
                'net_weight': net_weight,
                'gross_weight': gross_weight,
                'box_no': box_serial_no,
                'pagination': pagination,
                'item_packing': []
            }

            # Get list of item packing
            count_box_details = BoxDetails.objects.filter(parent_box=box_code).count()
            if count_box_details > 1:
                filter_data = BoxDetails.objects.filter(parent_box=box_code, main_box=False).values_list('box_code',
                                                                                                         flat=True)
            else:
                filter_data = BoxDetails.objects.filter(parent_box=box_code).values_list('box_code', flat=True)

            # Serializer for box details
            box_data = BoxDetails.objects.filter(box_code__in=filter_data)
            box_serializer = BoxDetailSerializer(box_data, many=True, context={'request': request})
            box_serializer_data = box_serializer.data

            # Serializer for item packing
            item_packing_data = ItemPacking.objects.filter(box_code__in=filter_data)
            item_packing_serializer = ItemPackingSerializer(item_packing_data, many=True, context={'request': request})
            item_serializer_data = item_packing_serializer.data

            # Fetch new box details if box_item_flag is true
            new_box_details = BoxDetails.objects.filter(box_code=box_code, box_item_flag=True).values_list('box_code',
                                                                                                           flat=True)
            new_item_packing_data = ItemPacking.objects.filter(box_code__in=new_box_details)
            new_item_packing_serializer = ItemPackingSerializer(new_item_packing_data, many=True,
                                                                context={'request': request})
            new_item_packing_serializer_data = new_item_packing_serializer.data

            # Combine item packing data with box details
            for box in box_serializer_data:
                item_list = []
                for item in item_serializer_data:
                    if box['box_code'] == item['box_code']:
                        if box['main_box'] == False:
                            for item_packing_inline in item['item_packing_inline']:
                                item_packing_inline['box_no_manual'] = box['box_no_manual']
                        item_list.append(item)
                        new_item_packing_serializer_data.append(item)
                box_data_entry['item_packing'] = new_item_packing_serializer_data
            response_data.append(box_data_entry)  # Append to response_data

        response = response_data
        # return Response(response_data)

        # PDF Creation main logic
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        x_gap = 10  # Define the gap for x-axis

        def draw_header(canvas, page_number, total_pages):
            canvas.setFont("Helvetica-Bold", 12)
            logo_path = os.path.join(settings.MEDIA_ROOT, "images", "yokogawa_logo.jpg")
            canvas.drawImage(logo_path, inch, height - inch - 30, width=150, height=30)
            canvas.drawString(6 * inch, height - inch, "Packing List")
            canvas.setFont("Helvetica", 9)
            company_info = [
                "Yokogawa India Limited",
                "Plot No.96, Electronic City Complex, Hosur Road",
                "Bangalore-560100, India",
                "State Name & Code: Karnataka-29 India",
                "Phone: +91-80-2852-1100",
            ]
            text_object = canvas.beginText(inch, height - 2 * inch)
            for line in company_info:
                text_object.textLine(line)
            canvas.drawText(text_object)

            doc_info = [
                f"DO No: {dispatch.dil_no}",
                f"DO Date: {dispatch.dil_date}",
                f"SO No: {dispatch.so_no}",
                f"PO No: {dispatch.po_no.split()[0]}",
            ]
            text_object = canvas.beginText(6 * inch, height - 2 * inch)
            for line in doc_info:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, height - 2.8 * inch, width - inch, height - 2.8 * inch)

            page_no_info = f"Page {page_number} of {total_pages}"
            canvas.drawString(6 * inch, height - 2.7 * inch, page_no_info)

        def shipment_header(canvas, y_position):
            canvas.setFont("Helvetica", 7)
            ship_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(inch, y_position + 15, "SHIP TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(inch, y_position)
            for line in ship_to:
                text_object.textLine(line)
            canvas.drawText(text_object)

            bill_to = [
                "THERMAX BABCOCK & WILCOX ENERGY",
                "PLOT NO. A2,&A3",
                "KHANDALA INDUSTRIAL AREA,PHSE 1",
                "MAHARASHTRA,27 Maharashtra",
                "IN 412802",
            ]
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawString(4 * inch, y_position + 15, "BILL TO")
            canvas.setFont("Helvetica", 7)
            text_object = canvas.beginText(4 * inch, y_position)  # Adjusted x position to 3.5 * inch
            for line in bill_to:
                text_object.textLine(line)
            canvas.drawText(text_object)
            canvas.line(inch, y_position - 0.8 * inch, width - inch, y_position - 0.8 * inch)

        def draw_footer(canvas, page_number, total_pages):
            canvas.setFont("Helvetica", 10)
            footer_text = f"Page {page_number} of {total_pages}"
            canvas.drawString(inch, inch / 2, footer_text)

        def draw_wrapped_string(canvas, x, y, text, max_width):
            if text is None:
                text = ''
            words = text.split()
            lines = []
            line = ""
            for word in words:
                if canvas.stringWidth(line + word) <= max_width:
                    line += word + " "
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())
            for line in lines:
                canvas.drawString(x, y, line)
                y -= 12
            return y

        def draw_content(canvas, y_position, page_number, total_pages):
            processed_box_codes = set()  # Track processed box codes
            canvas.setFont("Helvetica", 8)
            canvas.setFont("Helvetica-Bold", 8)
            y_position -= 20
            dispatch_header = [
                'Model Description',
                'MS Code',
                'Linkage No',
                'Customer PO Sl No',
                'Customer Part No',
            ]
            y_position -= 10
            canvas.drawString(inch, y_position, "Packing Id")
            text_object = canvas.beginText(2 * inch + x_gap, y_position)
            for dil_header in dispatch_header:
                text_object.textLine(dil_header)
            canvas.drawText(text_object)
            canvas.drawString(5 * inch + x_gap, y_position, "Quantity/Quantity Unit")

            # Draw a line based on the header
            canvas.line(inch, y_position - 10 * 5, width - inch, y_position - 10 * 5)

            # data binding for content
            canvas.setFont("Helvetica", 8)
            y_position -= 20 * 2
            for datas in response:
                box_code = datas['box_no_manual']
                if box_code in processed_box_codes:
                    continue  # Skip this box_code if already processed
                processed_box_codes.add(box_code)  # Mark this box_code as processed
                y_position -= 25  # Adjust for box spacing
                if y_position < inch:
                    canvas.showPage()
                    page_number += 1
                    draw_header(canvas, page_number, total_pages)
                    draw_footer(canvas, page_number, total_pages)
                    y_position = height - 3 * inch

                canvas.setFont("Helvetica-Bold", 9)
                draw_wrapped_string(canvas, inch, y_position, datas['box_no_manual'], 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 10, str(datas['volume']), 4 * inch)
                canvas.setFont("Helvetica", 7)
                draw_wrapped_string(canvas, inch, y_position - 20, "NT W/T:" + str(datas['net_weight']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 30, "GR W/T:" + str(datas['gross_weight']), 4 * inch)
                # draw_wrapped_string(canvas, inch, y_position - 40, "Box No:" + str(datas['box_no']), 4 * inch)
                draw_wrapped_string(canvas, inch, y_position - 40, "Box No:" + str(datas['pagination']), 4 * inch)
                canvas.setFont("Helvetica", 8)
                item_packing_list = datas['item_packing'] if 'item_packing' in datas else []
                for item_packing in item_packing_list:
                    if y_position < inch:
                        canvas.showPage()
                        page_number += 1
                        draw_header(canvas, page_number, total_pages)
                        draw_footer(canvas, page_number, total_pages)
                        y_position = height - 3 * inch
                    canvas.setFont("Helvetica", 8)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('material_description', ''),
                                                     4 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('linkage_no', ''), 4 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position,
                                                     item_packing['item_ref_id'].get('ms_code', ''), 2 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, "Cust PO  SI No: " + (
                            item_packing['item_ref_id'].get('customer_po_sl_no', '') or ''), 2 * inch)
                    y_position = draw_wrapped_string(canvas, 2 * inch + x_gap, y_position, "Cust Part No: " + (
                            item_packing['item_ref_id'].get('customer_po_item_code', '') or ''), 2 * inch)
                    canvas.drawString(5 * inch + x_gap + 10, y_position + 50,
                                      str(item_packing.get('item_qty', '')) + " ST")
                    canvas.setFont("Helvetica", 8)
                    y_position -= 20  # Adjust for item packing spacing
                    count = 0  # Counter for inline items
                    for inline_item_packing in item_packing.get('item_packing_inline', []):
                        if count == 3:  # Move to next line after 4 items
                            y_position -= 30
                            count = 0
                        if y_position < inch:
                            canvas.showPage()
                            page_number += 1
                            draw_header(canvas, page_number, total_pages)
                            draw_footer(canvas, page_number, total_pages)
                            y_position = height - 3 * inch

                        text_object = canvas.beginText(2 * inch + 5 + (count * 2 * inch), y_position)
                        canvas.setFont("Courier", 7)
                        text_object.textLine(f"S/N=  {inline_item_packing.get('serial_no', '')}")
                        text_object.textLine(f"TAG=  {inline_item_packing.get('tag_no', '')}")
                        text_object.textLine(f"Box=  {inline_item_packing.get('box_no_manual', '')}")
                        canvas.drawText(text_object)
                        canvas.setFont("Helvetica", 8)
                        count += 1  # Increment counter

                    canvas.setDash(3, 3)
                    y_position -= 30
                    canvas.line(inch, y_position, width - inch, y_position)
                    canvas.setDash()
                    y_position -= 20  # Adjust for dash line spacing
            return y_position, page_number

        # Initialize the PDF creation and end of draw_content
        y_position = height - 2 * inch
        page_number = 1
        total_pages = 1
        # Draw the first page header, shipment header, footer, and content
        draw_header(p, page_number, total_pages)
        shipment_header(p, y_position - 30 * 3)
        draw_footer(p, page_number, total_pages)
        y_position, page_number = draw_content(p, y_position - 150, page_number,
                                               total_pages)  # Adjust y_position for shipment header height

        # Finalize the PDF creation
        p.showPage()
        p.save()

        # Save the PDF to the file system
        media_path = os.path.join(settings.MEDIA_ROOT, "packing_export")
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        file_path = os.path.join(media_path, f"dispatch_packing_summary_{dispatch.dil_id}.pdf")
        with open(file_path, "wb") as file:
            file.write(buffer.getvalue())

        # Send the PDF to the client
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="dispatch_packing_list_{dispatch.dil_id}.pdf"'
        buffer.seek(0)
        response.write(buffer.getvalue())

        return response


class CustomerConsigneeExport(viewsets.ModelViewSet):
    queryset = TruckLoadingDetails.objects.all()
    serializer_class = TruckLoadingDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    @action(methods=['post'], detail=False, url_path='annexure_delivery_challan')
    def annexure_delivery_challan(self, request, *args, **kwargs):
        try:
            loading_details = self.queryset.filter(truck_list_id=request.data['truck_list_id']).values_list('box_code')
            item_packing = ItemPacking.objects.filter(box_code__in=loading_details).values_list('item_ref_id')
            master_list = MasterItemList.objects.filter(item_id__in=item_packing)
            item_serializer = MasterItemListSerializer(master_list, many=True)
            # Delivery Challan
            delivery_challan = DeliveryChallan.objects.filter(truck_list=request.data['truck_list_id'])
            challan_serializer = DeliveryChallanSerializer(delivery_challan, many=True)
            context = {'item_data': item_serializer.data, 'delivery_challan': challan_serializer.data}
            # Create PDF file
            html_template = get_template('annexure_delivery_challan.html')
            html = html_template.render(context)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="annexure_delivery_challan.pdf"'
                media_path = os.path.join(settings.MEDIA_ROOT, "dispatch_export")
                if not os.path.exists(media_path):
                    os.makedirs(media_path)
                file_path = os.path.join(media_path,
                                         "annexure_delivery_challan{0}.pdf".format(request.data['truck_list_id']))
                with open(file_path, "wb") as file:
                    file.write(response.getvalue())
                return response
            return HttpResponse("Error rendering PDF", status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='customer_consignee_pdf')
    def customer_consignee_pdf(self, request, *args, **kwargs):
        try:
            # Fetch the dispatch instruction, master list and delivery challan
            dispatch = DispatchInstruction.objects.get(dil_id=request.data['dil_id'])
            dispatch_serializer = DispatchInstructionSerializer(dispatch)

            master_list = MasterItemList.objects.filter(dil_id=request.data['dil_id'])
            item_serializer = MasterItemListSerializer(master_list)

            delivery_challan = DeliveryChallan.objects.filter(truck_list__id=request.data['truck_list_id']).first()
            dc_invoice = DCInvoiceDetails.objects.filter(delivery_challan=delivery_challan)
            total_consignee_value = dc_invoice.aggregate(Sum('bill_amount'))['bill_amount__sum']
            dc_invoice_serializer = DCInvoiceDetailsSerializer(dc_invoice, many=True)
            # Other details
            ck_lists = TruckList.objects.get(id=request.data['truck_list_id'])
            transporter = TrackingTransportation.objects.get(id=ck_lists.transportation.id)

            context = {
                'dispatch_data': dispatch_serializer.data,
                'master_list': item_serializer.data,
                'dc_invoice_data': dc_invoice_serializer.data,

                'today': datetime.datetime.now().date(),
                'descOfGoods': delivery_challan.description_of_goods,
                'transporter_name': transporter.transportation_name,
                'destination': delivery_challan.destination,
                'mode_of_delivery': delivery_challan.mode_of_delivery,
                'freight_mode': delivery_challan.freight_mode,
                'consignee_remakes': delivery_challan.consignee_remakes,
                'total_consignee_value': total_consignee_value or 0.0,
                'insurance': dispatch.insurance_scope.insurance_scope_name if dispatch.insurance_scope else None
            }
            # Create PDF file
            # return Response(context)
            html_template = get_template('customer_consignee.html')
            html = html_template.render(context)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="customer_consignee.pdf"'
                # Save the file
                media_path = os.path.join(settings.MEDIA_ROOT, "dispatch_export")
                if not os.path.exists(media_path):
                    os.makedirs(media_path)
                file_path = os.path.join(media_path, "customer_consignee{0}.pdf".format(request.data['dil_id']))
                with open(file_path, "wb") as file:
                    file.write(response.getvalue())
                return response
            return HttpResponse("Error rendering PDF", status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DCInvoiceDetailsReportViewSet(viewsets.ModelViewSet):
    queryset = DCInvoiceDetails.objects.all()
    serializer_class = DCInvoiceDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=['post'], detail=False, url_path='dc_invoice_details_report')
    def dc_invoice_details_report(self, request, *args, **kwargs):
        try:
            data = request.data
            dispatch_flag = data.get('dispatch_flag', False)
            delivery_flag = data.get('delivery_flag', False)
            truck_flag = data.get('truck_flag', False)

            dispatch_filter = data.get('dispatch_filter', {})
            delivery_filter = data.get('delivery_filter', {})
            truck_filter = data.get('truck_filter', {})

            queryset = DCInvoiceDetails.objects.all()

            if dispatch_flag:
                dispatch_ids = DispatchInstruction.objects.filter(**dispatch_filter).values_list('dil_id', flat=True)
                if dispatch_ids:
                    queryset = DCInvoiceDetails.objects.filter(dil_id__in=dispatch_ids)

            if truck_flag:
                truck_ids = TruckList.objects.filter(**truck_filter).values_list('id', flat=True)
                if truck_ids:
                    queryset = DCInvoiceDetails.objects.filter(truck_list__in=truck_ids)

            if delivery_flag:
                delivery_ids = DeliveryChallan.objects.filter(**delivery_filter).values_list('id', flat=True)
                if delivery_ids:
                    queryset = DCInvoiceDetails.objects.filter(delivery_challan__in=delivery_ids)

            serializer = DCInvoiceDetailsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# create report part views here.
class ItemPackingReportViewSet(viewsets.ModelViewSet):
    queryset = ItemPacking.objects.all()
    serializer_class = ItemPackingSerializer

    @action(methods=['post'], detail=False, url_path='item_packing_report_serial_no_wise')
    def item_packing_report_serial_no_wise(self, request, *args, **kwargs):
        try:
            data = request.data
            dil_flag = data.get('dil_flag', False)
            box_flag = data.get('box_flag', False)
            inline_flag = data.get('inline_flag', False)

            dil_filter = data.get('dil_filter', {})
            box_filter = data.get('box_filter', {})
            inline_filter = data.get('inline_filter', {})

            dispatch_ids = []
            box_codes = []
            inline_query = ItemPackingInline.objects.none()
            dispatch_serializer = None  # Initialize to None

            if dil_flag:
                dispatch_ids = DispatchInstruction.objects.filter(**dil_filter).values_list('dil_id', flat=True)
            only_dispatch_box_query = BoxDetails.objects.filter(dil_id__in=dispatch_ids)

            if box_flag:
                box_query = BoxDetails.objects.filter(**box_filter)
                if dispatch_ids:
                    box_query = box_query.filter(dil_id__in=dispatch_ids)
                box_codes = box_query.values_list('box_code', flat=True)
            else:
                box_codes = only_dispatch_box_query.values_list('box_code', flat=True)

            if inline_flag:
                inline_query = ItemPackingInline.objects.filter(**inline_filter)

            if box_codes:
                item_packing = ItemPacking.objects.filter(box_code__in=box_codes)
                item_packing_ids = item_packing.values_list('item_packing_id', flat=True)
                if inline_flag:
                    inline_query = inline_query.filter(item_pack_id__in=item_packing_ids)
                else:
                    inline_query = ItemPackingInline.objects.filter(item_pack_id__in=item_packing_ids)

            # Final response for packing inline
            serializer = ItemPackingInlineReportSerializer(inline_query, many=True)
            result = []
            # Binding the box details and dispatch data
            for response in serializer.data:
                if response['box_details']:
                    first_box_detail = response['box_details'][0]
                    dispatch = DispatchInstruction.objects.get(dil_id=first_box_detail['dil_id'])
                    dispatch_serializer = DispatchInstructionSerializer(dispatch)
                response['dispatch'] = dispatch_serializer.data
                result.append(response)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDocumentsDetailsViewSet(viewsets.ModelViewSet):
    queryset = BoxDetails.objects.all()
    serializer_class = BoxDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=['POST'], detail=False, url_path='customer_details_doc')
    def customer_details_doc(self, request, pk=None):
        try:
            box_code = request.data['box_code']
            box_details = BoxDetails.objects.get(box_code=box_code)
            dil_id = box_details.dil_id.dil_id
            box_size = box_details.box_size.box_size_id
            dispatch = DispatchInstruction.objects.get(dil_id=dil_id)
            box = BoxSize.objects.get(box_size_id=box_size)
            response_data = {
                'dil_id': dispatch.dil_id,
                'ship_to_party_name': dispatch.ship_to_party_name,
                'ship_to_address': dispatch.ship_to_address,
                'ship_to_city': dispatch.ship_to_city,
                'ship_to_postal_code': dispatch.ship_to_postal_code,
                'ship_to_country': dispatch.ship_to_country,
                'dil_no': dispatch.dil_no,
                'dil_date': dispatch.dil_date,
                'so_no': dispatch.so_no,
                'po_no': dispatch.po_no,
                'po_date': dispatch.po_date,
                'customer_name': dispatch.customer_name,
                'customer_number': dispatch.customer_number,
                'package_id': box_details.box_code,
                'barcode': box_details.box_code,
                'net_weight': box_details.net_weight,
                'gr_weight': box_details.qa_wetness,
                'box_size': box.box_size
            }
            html_template = get_template('customer_details.html')
            html = html_template.render({'response_data': response_data})
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="dispatch_instruction.pdf"'
                # Save the file
                media_path = os.path.join(settings.MEDIA_ROOT, "documents")
                if not os.path.exists(media_path):
                    os.makedirs(media_path)
                file_path = os.path.join(media_path, "customer_details_{0}.pdf".format(dispatch.dil_no))
                with open(file_path, "wb") as file:
                    file.write(response.getvalue())
                return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
