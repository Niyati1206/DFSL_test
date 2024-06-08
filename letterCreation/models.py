from django.db import models

class Lab(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Department(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    ac_no = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    pan_no = models.CharField(max_length=255)
    gst_no = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    address = models.TextField()
    email_id = models.EmailField()
    contact_no = models.CharField(max_length=255)

    def __str__(self):
        return self.name
  
class Letter(models.Model):
    letter_no = models.CharField(max_length=255)
    lab_name = models.ForeignKey(Lab, on_delete=models.CASCADE)
    letter_date = models.DateField()

    def __str__(self):
        return self.letter_no

class MainItem(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}-{self.manufacturer.name}"

class Product(models.Model):
    main_item = models.ForeignKey(MainItem, on_delete=models.CASCADE)
    sr_no = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buying_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    lab_name = models.ForeignKey(Lab, on_delete=models.CASCADE)
    amc_provider = models.ForeignKey('AMCProvider', on_delete=models.CASCADE)
    amc_period = models.CharField(max_length=255)
    expenditure_cost = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer_warranty_period = models.CharField(max_length=255)
    service_report_date = models.DateField(null=True, blank=True)  # New field for current service report date

    def __str__(self):
        return self.sr_no
    
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance has already been saved
            original_product = Product.objects.get(pk=self.pk)  # Get the original instance from the database
            if original_product.service_report_date != self.service_report_date:
                ServiceReportTrack.objects.create(product=self, service_date=original_product.service_report_date)
        super().save(*args, **kwargs)

class ServiceReportTrack(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='service_reports')
    service_date = models.DateField()

    def __str__(self):
        return f"Service report for {self.product} on {self.service_date}"

class Subproduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='subproducts')
    type_of_part = models.CharField(max_length=255)
    part_name = models.CharField(max_length=255)
    specification = models.TextField()
    quantity = models.IntegerField()
    # period_of_amc_contract = models.CharField(max_length=255)
    amc_provider = models.ForeignKey('AMCProvider', on_delete=models.CASCADE)

    def __str__(self):
        return self.part_name

class Quotation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quotation_date = models.DateField()
    ref_no = models.CharField(max_length=255)
    QUOTATION_EXPENSE_CHOICES = [
        ('20%', '20%'),
        ('25%', '25%'),
    ]
    quotation_expense_criteria = models.CharField(max_length=3, choices=QUOTATION_EXPENSE_CHOICES, default='20%')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.ref_no

class AMCProvider(models.Model):
    name = models.CharField(max_length=255)
    ac_no = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=255)
    ac_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    pan_no = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    address = models.TextField()
    email_id = models.EmailField()
    contact_no = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    subproduct = models.ForeignKey(Subproduct, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    gst_value = models.DecimalField(max_digits=10, decimal_places=2)
    expected_delivery = models.CharField(max_length=255)
    amc_provider = models.ForeignKey(AMCProvider, on_delete=models.CASCADE)

    def __str__(self):
        return self.subproduct.part_name

class PrintTrack(models.Model):
    printed_date1 = models.DateField(null=True, blank=True)
    printed_date2 = models.DateField(null=True, blank=True)
    printed_date3 = models.DateField(null=True, blank=True)
    printed_date4 = models.DateField(null=True, blank=True)
    letter_no = models.CharField(max_length=255)  # Reference to letter_no from Letter model

    def __str__(self):
        return self.letter_no
    
class LetterProduct(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.letter.letter_no} - {self.product.sr_no}"
