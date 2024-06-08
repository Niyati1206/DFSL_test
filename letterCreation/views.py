from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import Letter, Product, Subproduct, Quotation, AMCProvider, QuotationItem,MainItem,Manufacturer,Department,Lab,LetterProduct

from django.db.models import Count

def index(request):
    return render(request,'index.html')


def amc_providers_list(request):
    providers = AMCProvider.objects.all()
    return render(request, 'amc_providers_list.html', {'providers': providers})



def service_report_history(request):
    products = Product.objects.all()
    return render(request, 'service_report_history.html', {'products': products})

def get_sr_numbers(request):
    lab_id = request.GET.get('lab_id')
    main_item = request.GET.get('main_item')
    manufacturer = request.GET.get('manufacturer')

    if lab_id and main_item and manufacturer:
        sr_numbers = Product.objects.filter(
            lab_name__id=lab_id,
            main_item__name=main_item,
            main_item__manufacturer__name=manufacturer
        ).values_list('sr_no', flat=True).distinct()
        sr_numbers_list = list(sr_numbers)
        return JsonResponse({'sr_numbers': sr_numbers_list})
    return JsonResponse({'sr_numbers': []})


def load_form(request):
    # Fetch required context data for the form
    main_items = MainItem.objects.values('name', 'id').annotate(total=Count('name')).filter(total=1)
    labs = Lab.objects.all()
    manufacturer_names = list(Manufacturer.objects.values_list('name', flat=True))
    departments = Department.objects.all()
    
    # Fetch all letters with their related products and subproducts for the product information table
    letters = Letter.objects.prefetch_related('products__subproducts').all()

    context = {
        'main_items': main_items,
        'manufacturer_names': manufacturer_names,
        'departments': departments,
        'labs': labs,
        'letters': letters
    }

    return render(request, 'form1.html', context)


def get_manufacturers(request):
    main_item = request.GET.get('main_item')
    print(f"Received main_item: {main_item}")  # Debugging statement
    if main_item:
        manufacturers = Manufacturer.objects.filter(mainitem__name=main_item).values_list('name', flat=True).distinct()
    else:
        manufacturers = Manufacturer.objects.none()
    print(f"Manufacturers found: {list(manufacturers)}")  # Debugging statement
    return JsonResponse({'manufacturer_names': list(manufacturers)})



def get_manufacturer_names(request):
    main_item = request.GET.get('main_item')
    manufacturers = Manufacturer.objects.filter(mainitem__name=main_item).values_list('name', flat=True).distinct()
    return JsonResponse({'manufacturer_names': list(manufacturers)})

def get_product_serial_numbers(request):
    lab_id = request.GET.get('lab_id')
    manufacturer = request.GET.get('manufacturer')
    products = Product.objects.filter(lab_id=lab_id, manufacturer__name=manufacturer).values_list('serial_number', flat=True)
    return JsonResponse({'product_serial_numbers': list(products)})



def product_list(request):
    # Retrieve all LetterProduct objects
    letter_products = LetterProduct.objects.all()
    
    # Pass the data to the template
    context = {
        'letter_products': letter_products
    }
    
    # Render the template with the provided context
    return render(request, 'table.html', context)


def letter_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    letter_id = product.letter_id
    subproducts = product.subproducts.all()
    return render(request, 'letter1.html', {'product': product,'subproducts':subproducts, 'letter_id':letter_id})

def quotation_form(request):
    letters = Letter.objects.all()
    return render(request, 'letter_intermidiate.html', {'letters': letters})

def quotation_page(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    amc_providers_exist = set(AMCProvider.objects.values_list('name', flat=True))
    return render(request, 'quotation_info.html', {'product': product, 'subproducts': subproducts, 'amc_providers_exist': amc_providers_exist})



def product_list4(request):
    letters = Letter.objects.all()
    return render(request, 'table2.html', {'letters': letters})

def letter_detail4(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    letter = product.letter
    amc_provider = subproduct.amc_provider
    related_subproducts = Subproduct.objects.filter(product=product, amc_provider=amc_provider)
    service_report_date = subproduct.service_report_date
    return render(request, 'letter4.html', {'product': product, 'amc_provider': amc_provider, 'related_subproducts': related_subproducts, 'service_report_date': service_report_date,'letter':letter})




def letter_detail6(request, subproduct_id):
    subproduct = Subproduct.objects.get(pk=subproduct_id)
    product = subproduct.product
    amc_provider = subproduct.amc_provider
    subproducts = Subproduct.objects.filter(product=product).select_related('amc_provider')
    quotations = Quotation.objects.filter(product=product, quotationitem__subproduct=subproduct)

    # Calculate global variables
    global_total_basic_price = Decimal('0')
    global_gst_value = Decimal('0')
    global_total_price_inclusive = Decimal('0')

    # Group subproducts by amc_provider name
    grouped_subproducts = {}
    for sub in subproducts:
        provider_name = sub.amc_provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(sub)

        # Calculate total basic price, GST value, and total price inclusive
        total_basic_price = sub.quotationitem_set.first().unit_price * sub.quantity
        gst_value = total_basic_price * Decimal('0.18')
        total_price_inclusive = total_basic_price + gst_value

        # Update global variables
        global_total_basic_price += total_basic_price
        global_gst_value += gst_value
        global_total_price_inclusive += total_price_inclusive

    # Load the text based on the quotation_expense_criteria value from Quotation model
    quotation_expense_criteria_text = ""
    for quotation in quotations:
        if quotation.quotation_expense_criteria == '20%':
            quotation_expense_criteria_text = "शासन निर्णय, वित्त विभाग, क्रमांकः विअप्र-२०१३/प्र.क.३०/२०१३/विनियम, दिनांक १७ एप्रिल , २०१५ अन्वये भाग पहिला उपविभाग. २ अनुक्रमांक. ५ नियम क्र.७ यंत्राच्या कार्यसज्जतेसाठी लागणारे सुटे भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणे करिता यंत्र सामग्रीच्या पुस्तकी किमतीच्या २०% मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या भागांची खरेदी करण्याबाबत अधिकार आहेत."
        elif quotation.quotation_expense_criteria == '25%':
            quotation_expense_criteria_text = "शासन निर्णय, वित्त विभाग, क्रमांकः विअप्र-२०१३/प्र.क.३०/२०१३/विनियम, दिनांक १७ एप्रिल , २०१५ अन्वये भाग पहिला उपविभाग. २ अनुक्रमांक. ५ नियम क्र.७ यंत्राच्या कार्यसज्जतेसाठी लागणारे सुटे भाग, उपसाधने व इतर वस्तू साधनसामग्री विकत घेण्यासाठी मंजूरी देणे करितासंयत्रे , यंत्रसामग्री आणि साधनसामग्री इत्यादीच्या दुरुस्ती करिता वार्षिक खर्च यंत्रसामग्रीच्या पुस्तकी किंमतीच्या 25% मर्यादेपर्यंत विभाग प्रमुख व प्रादेशिक कार्यालय प्रमुख यांना दरपत्रक मागून सुट्ट्या भागांची खरेदी करण्याबाबत अधिकार आहेत."

    return render(request, 'letter6.html', {
        'product': product,
        'grouped_subproducts': grouped_subproducts,
        'global_total_basic_price': global_total_basic_price,
        'quotations': quotations,
        'global_gst_value': global_gst_value,
        'global_total_price_inclusive': global_total_price_inclusive,
        'quotation_expense_criteria_text': quotation_expense_criteria_text,
    })

    
    
def product_list6(request):
    letters = Letter.objects.all()
    return render(request, 'table6.html', {'letters': letters})







def product_list7(request):
    letters = Letter.objects.all()
    return render(request, 'table7.html', {'letters': letters})


def letter_detail7(request, product_id):
    product = Product.objects.get(pk=product_id)
    subproducts = product.subproducts.all()
    letter = product.letter
    quotations = Quotation.objects.filter(product=product)

    grouped_subproducts = {}
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider.name
        if provider_name not in grouped_subproducts:
            grouped_subproducts[provider_name] = []
        grouped_subproducts[provider_name].append(subproduct)

    return render(request, 'letter.html', {'product': product, 'grouped_subproducts': grouped_subproducts, 'letter': letter, 'quotations': quotations})

@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            # Get form data
            letter_no = request.POST.get('letter_no')
            lab_name_id = request.POST.get('lab_name')
            letter_date = request.POST.get('date')

            if not lab_name_id.isdigit():
                raise ValueError(f"lab_name_id is not a digit: {lab_name_id}")

            # Validate and parse the date
            try:
                letter_date = datetime.datetime.strptime(letter_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f"Letter date {letter_date} is not in the correct format YYYY-MM-DD")

            # Create a Letter instance
            letter = Letter.objects.create(
                letter_no=letter_no,
                lab_name_id=lab_name_id,
                letter_date=letter_date
            )

            # Process products
            product_index = 0
            while True:
                sr_no = request.POST.get(f'products[{product_index}][sr_no]')
                service_report_date = request.POST.get(f'products[{product_index}][service_report_date]')

                if not sr_no:
                    break

                # Find the product by SR No
                try:
                    product = Product.objects.get(sr_no=sr_no)
                    amc_provider = product.amc_provider  # Assume AMC provider is a field in the Product model
                except Product.DoesNotExist:
                    raise ValueError(f"Product with SR No {sr_no} does not exist")

                # Validate and parse the service report date if provided
                if service_report_date:
                    try:
                        service_report_date = datetime.datetime.strptime(service_report_date, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValueError(f"Service report date {service_report_date} is not in the correct format YYYY-MM-DD")

                    # Update service report date
                    product.service_report_date = service_report_date
                    product.save()

                # Create a LetterProduct instance to link the Letter and Product
                LetterProduct.objects.create(
                    letter=letter,
                    product=product
                )

                # Process subproducts
                subproduct_index = 0
                while True:
                    part_name = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_name]')
                    if not part_name:
                        break

                    part_type = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_type]')
                    part_specification = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_specification]')
                    part_quantity = request.POST.get(f'products[{product_index}][subproducts][{subproduct_index}][part_quantity]')

                    if not part_quantity.isdigit():
                        raise ValueError(f"Part quantity is not a digit: {part_quantity}")

                    # Create a Subproduct instance
                    Subproduct.objects.create(
                        product=product,
                        part_name=part_name,
                        type_of_part=part_type,
                        specification=part_specification,
                        quantity=part_quantity,
                        amc_provider=amc_provider  # Use AMC provider from the Product model
                    )
                    subproduct_index += 1

                product_index += 1

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def submit_quotation_info(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        date = request.POST.get('date')
        ref_no = request.POST.get('ref_no')
        quotation_expense_criteria = request.POST.get('quotation_criteria')

        # Create the quotation
        product = Product.objects.get(pk=product_id)
        quotation = Quotation.objects.create(
            product=product,
            quotation_date=date,
            ref_no=ref_no,
            quotation_expense_criteria=quotation_expense_criteria
        )

        total_price = 0  # Initialize total_price

        # Process each subproduct
        subproduct_ids = [key.split('_')[-1] for key in request.POST.keys() if key.startswith('subproduct_id')]
        for subproduct_id in subproduct_ids:
            subproduct = Subproduct.objects.get(pk=subproduct_id)
            amc_provider = subproduct.amc_provider

            unit_price = Decimal(request.POST.get(f'unit_price_{subproduct_id}'))  # Convert to Decimal
            quantity = subproduct.quantity
            price_without_gst = unit_price * quantity
            gst_value = price_without_gst * Decimal('0.18')  # Calculate GST value
            price_with_gst = price_without_gst + gst_value

            total_price += price_with_gst  # Add price_with_gst to total_price

            # Create the quotation item
            quotation_item = QuotationItem.objects.create(
                quotation=quotation,
                subproduct=subproduct,
                unit_price=unit_price,
                price_without_gst=price_without_gst,
                price_with_gst=price_with_gst,
                gst_percentage=18,  # Hardcoded GST percentage for now
                gst_value=gst_value,
                expected_delivery=request.POST.get(f'expected_delivery_{subproduct_id}'),
                amc_provider=amc_provider
            )

            # Update the AMCProvider fields (if needed)
            # Note: This part may need adjustment based on your actual requirements

        quotation.total_price = total_price  # Update total_price
        quotation.save()

        return JsonResponse({'message': 'Quotation information submitted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)