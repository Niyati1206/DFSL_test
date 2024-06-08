from django.contrib import admin
from .models import Lab, Department, Manufacturer, Letter, MainItem, Product, Subproduct, Quotation, AMCProvider, QuotationItem, PrintTrack, ServiceReportTrack, LetterProduct

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_lab_name']
    
    def get_lab_name(self, obj):
        return obj.lab.name if obj.lab else ''
    get_lab_name.short_description = 'Lab Name'

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ac_no', 'bank_name', 'pan_no', 'gst_no', 'state', 'pincode', 'address', 'email_id', 'contact_no']

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['id', 'letter_no', 'lab_name', 'letter_date']

@admin.register(MainItem)
class MainItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_manufacturer']

    def get_manufacturer(self, obj):
        return obj.manufacturer.name if obj.manufacturer else ''
    get_manufacturer.short_description = 'Manufacturer'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_mainitem_name', 'sr_no', 'price', 'buying_date', 'get_department_name', 'get_lab_name', 'get_amc_provider_name', 'service_report_date', 'amc_period', 'expenditure_cost', 'manufacturer_warranty_period']

    def get_department_name(self, obj):
        return obj.department.name if obj.department else ''
    get_department_name.short_description = 'Department'

    def get_mainitem_name(self, obj):
        if obj.main_item:
            return f"{obj.main_item.name}-{obj.main_item.manufacturer}"
        return ''
    get_mainitem_name.short_description = 'Product Name' 

    def get_lab_name(self, obj):
        return obj.lab_name.name if obj.lab_name else ''
    get_lab_name.short_description = 'Lab Name'

    def get_amc_provider_name(self, obj):
        return obj.amc_provider.name if obj.amc_provider else ''
    get_amc_provider_name.short_description = 'AMC Provider'

@admin.register(Subproduct)
class SubproductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'type_of_part', 'part_name', 'specification', 'quantity', 'amc_provider']

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quotation_date', 'ref_no', 'quotation_expense_criteria', 'total_price']

@admin.register(AMCProvider)
class AMCProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ac_no', 'ifsc_code', 'ac_name', 'bank_name', 'pan_no', 'state', 'pincode', 'address']

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'quotation', 'subproduct', 'unit_price', 'price_without_gst', 'price_with_gst', 'gst_percentage', 'gst_value', 'expected_delivery', 'amc_provider']

@admin.register(PrintTrack)
class PrintTrackAdmin(admin.ModelAdmin):
    list_display = ['id', 'printed_date1', 'printed_date2', 'printed_date3', 'printed_date4', 'letter_no']

@admin.register(ServiceReportTrack)
class ServiceReportTrackAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'service_date']

@admin.register(LetterProduct)
class LetterProductAdmin(admin.ModelAdmin):
    list_display = ('letter', 'product')
    search_fields = ('letter__letter_no', 'product__sr_no')