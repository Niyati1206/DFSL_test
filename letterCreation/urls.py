from django.urls import path
from . import views
urlpatterns = [
    
    
    path('form/',views.load_form), 
   
    path('get_manufacturer_names/', views.get_manufacturer_names, name='get_manufacturer_names'),
    path('get_manufacturers/', views.get_manufacturers, name='get_manufacturers'),
    path('get_sr_numbers/', views.get_sr_numbers, name='get_sr_numbers'),
    path('amc-providers/', views.amc_providers_list, name='amc_providers_list'),
    path('service-report-history/', views.service_report_history, name='service_report_history'),
    # path('letterGenerate/get_manufacturer_names/', views.get_manufacturer_names, name='get_manufacturer_names'),
    # path('letterGenerate/get_product_serial_numbers/', views.get_product_serial_numbers, name='get_product_serial_numbers'),
    

   
   path('submit_form/', views.submit_form, name='submit_form'),

#letter 3
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.letter_detail, name='letter_detail'),
 

#Quotations
    path('quotations/', views.quotation_form, name='product_list3'),
    path('submit_quotation_info/', views.submit_quotation_info, name='submit_quotation_info'),
    path('quotations/<int:product_id>/', views.quotation_page, name='quotation_page'),

    ###################
#letter 4
    path('products4/', views.product_list4, name='product_list2'),
    path('products4/<int:subproduct_id>/', views.letter_detail4, name='letter_detail4'),

#letter 6
    path('products6/', views.product_list6, name='product_list6'),
    path('letter6/<int:subproduct_id>/', views.letter_detail6, name='letter_detail6'),


#letter 7
    path('products7/', views.product_list7, name='product_list7'),
    path('products7/<int:product_id>/', views.letter_detail7, name='letter_detail7'),



]