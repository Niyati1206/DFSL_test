from django.urls import path
from . import views

urlpatterns = [

    
    path('',views.index),

#main items
    path('items/', views.mitem, name="mitem"),
    path('items', views.item_list, name='item_list'),
    path('edit/', views.edit_item, name='edit_item'),

# delete
      path('delete/', views.delete_item, name='delete_item'),


    path('tracking/',views.tracking),

    path('form/',views.load_form), 
   
    
    path('get_sr_numbers/', views.get_sr_numbers, name='get_sr_numbers'),

   

#manufacturer
    path('manufacturer/', views.manufacturer_view, name='manufacturer'), 
    path('edit/<int:manufacturer_id>/', views.edit_manufacturer, name='edit_manufacturer'),
     path('get_manufacturers/', views.get_manufacturers, name='get_manufacturers'),
    path('manufacturer/', views.manufacturer_list, name='manufacturer_list'),
    
    path('get_manufacturer_names/', views.get_manufacturer_names, name='get_manufacturer_names'),
   
    path('edit/<int:id>/', views.edit_manufacturer, name='edit_manufacturer'),

    

# delete manufacturer
    path('delete/<int:manufacturer_id>/', views.delete_manufacturer, name='delete_manufacturer'),

#product_list
    path('product_list/', views.product_list_view, name='product_list'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/json/', views.product_detail_json, name='product_detail_json'),



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