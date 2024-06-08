# Generated by Django 3.2.12 on 2024-06-04 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AMCProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ac_no', models.CharField(max_length=255)),
                ('ifsc_code', models.CharField(max_length=255)),
                ('ac_name', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('pan_no', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('email_id', models.EmailField(max_length=254)),
                ('contact_no', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_no', models.CharField(max_length=255)),
                ('letter_date', models.DateField()),
                ('lab_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.lab')),
            ],
        ),
        migrations.CreateModel(
            name='MainItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ac_no', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('pan_no', models.CharField(max_length=255)),
                ('gst_no', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('email_id', models.EmailField(max_length=254)),
                ('contact_no', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PrintTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('printed_date1', models.DateField(blank=True, null=True)),
                ('printed_date2', models.DateField(blank=True, null=True)),
                ('printed_date3', models.DateField(blank=True, null=True)),
                ('printed_date4', models.DateField(blank=True, null=True)),
                ('letter_no', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr_no', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buying_date', models.DateField()),
                ('amc_period', models.CharField(max_length=255)),
                ('expenditure_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('manufacturer_warranty_period', models.CharField(max_length=255)),
                ('service_report_date', models.DateField(blank=True, null=True)),
                ('amc_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.amcprovider')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.department')),
                ('lab_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.lab')),
                ('main_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.mainitem')),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_date', models.DateField()),
                ('ref_no', models.CharField(max_length=255)),
                ('quotation_expense_criteria', models.CharField(choices=[('20%', '20%'), ('25%', '25%')], default='20%', max_length=3)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.product')),
            ],
        ),
        migrations.CreateModel(
            name='Subproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_part', models.CharField(max_length=255)),
                ('part_name', models.CharField(max_length=255)),
                ('specification', models.TextField()),
                ('quantity', models.IntegerField()),
                ('amc_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.amcprovider')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subproducts', to='letterCreation.product')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceReportTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_reports', to='letterCreation.product')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_without_gst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_with_gst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gst_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gst_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expected_delivery', models.CharField(max_length=255)),
                ('amc_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.amcprovider')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.quotation')),
                ('subproduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.subproduct')),
            ],
        ),
        migrations.AddField(
            model_name='mainitem',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.manufacturer'),
        ),
        migrations.CreateModel(
            name='LetterProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.letter')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.product')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='letterCreation.lab'),
        ),
    ]
