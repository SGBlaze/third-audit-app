from django.db import models
from datetime import datetime
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=100)
    referenceName = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    referenceName = models.CharField(max_length=20)
    image = models.ImageField(null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    costPrice = models.FloatField()
    subPrice = models.FloatField()
    wholesalePrice = models.FloatField()
    retailPrice = models.FloatField()


    def __str__(self):
        return self.name


class SubDistributors(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TodayOpeningStock(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(blank=True, null=True)
    addedAt = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return self.product.name


class OpeningStockHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    productsData = models.JSONField(default=dict)

    def __str__(self):
        return str(self.productsData)


class TodayNewStock(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    addedAt = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.product.name



class NewStockHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    productsData = models.JSONField(default=dict)

    def __str__(self):
        return str(self.productsData)



class TodayClosingStock(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    addedAt = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.product.name


class ClosingStockHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    
    productsData = models.JSONField(default=dict)

    def __str__(self):
        return str(self.productsData)



class WholesaleRecord(models.Model):
    customerId = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customerName = models.CharField(max_length=100)
    productsData = models.JSONField(default=dict)
    productValue = models.FloatField(default=0)
    modeOfPayment = models.CharField(default="Cash", max_length=100)
    amtFromCustomer = models.FloatField(default=0)
    customerDebt = models.FloatField(default=0)
    customerCredit = models.FloatField(default=0)
    soldAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customerName}: {self.productsData} via {self.modeOfPayment}'

class RetailRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    productQuantity = models.IntegerField()
    productPrice = models.IntegerField(blank=True, null=True)
    soldAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}: {self.productQuantity}'

class SubRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    subName = models.ForeignKey(SubDistributors, on_delete=models.CASCADE)
    productData = models.JSONField(default=dict)
    productValue = models.FloatField(default=0)
    modeOfPayment = models.CharField(default="Cash", max_length=100)
    amtFromSubDistributor = models.FloatField(default=0)
    subDistributorDebt = models.FloatField(default=0)
    subDistributorCredit = models.FloatField(default=0)
    soldAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subName}: {self.productData} via {self.modeOfPayment}"

class ShopDeliveryRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    driverName = models.CharField(max_length=100)
    deliveryNumber = models.FloatField(default=0)
    productData = models.JSONField(default=dict)
    amountBroughtBack = models.FloatField(default=0, blank=True)
    deliveryStatus = models.CharField(max_length=100, default="delivering")
    leftAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.driverName}: {self.leftAt}'



class ActiveDeliveryStartRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    salesId = models.FloatField(default=0)
    productTaken = models.ForeignKey(Products, on_delete=models.CASCADE)
    productTakenQuantity = models.IntegerField()
    productQuantityBroughtBack = models.IntegerField(default=0, blank=True)
    amountBroughtBack = models.FloatField(default=0, blank=True)
    leftAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.productTakenQuantity} {self.productTaken} taken, {self.productQuantityBroughtBack} {self.productTaken} brought back'


class ActiveDeliverySalesRecord(models.Model):
    salesId = models.FloatField(default=0)
    deliveryCustName = models.CharField(max_length=100)
    deliveryProductData = models.JSONField()
    productValue = models.FloatField()
    modeOfPayment = models.CharField(max_length=100)
    amtFromCustomer = models.FloatField(default=0)
    customerDebt = models.FloatField(default=0)
    customerCredit = models.FloatField(default=0)
    purchasedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.deliveryCustName} purchased {self.deliveryProductData} via {self.modeOfPayment}'


class TodayDeliveryStartRecord(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    deliveryNumber = models.IntegerField(default=0)
    salesId = models.FloatField(default=0)
    productsData = models.JSONField(default=dict)
    amountBroughtBack = models.FloatField(default=0, blank=True)
    finishedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.productsData)


class TodayDeliverySalesRecord(models.Model):
    deliveryNumber = models.IntegerField(default=0)
    salesId = models.FloatField(default=0)
    allCustomerData = models.JSONField()
    finishedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.finishedAt)

    

class Invoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    invoiceNumber = models.CharField(max_length=100)
    invoiceImage = models.ImageField(null=False, blank=False)
    addedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.company}: {self.invoiceNumber}'


class TodayInvoiceNumber(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    invoiceNumber = models.CharField(max_length=100)

    def __str__(self):
        return self.invoiceNumber


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    accessStat = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} is an {self.role} and has {self.accessStat} access'


class AccessStatus(models.Model):
    status = models.BooleanField()

    def __str__(self):
        return self.status

class TotalAudit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    totalAuditId = models.FloatField(default=0.0)
    driver = models.CharField(max_length=100, default="Driver Name not set")
    shopAttendant = models.CharField(max_length=100, default="Shop Attendant name not Set")
    driverStatus = models.CharField(default="Driver has not closed", max_length=100)
    shopAttendantStatus = models.CharField(default="Shop attendant has not closed", max_length=100)
    openingStock = models.JSONField(default=dict)
    newStock = models.JSONField(default=dict)
    closingStock = models.JSONField(default=dict)
    driverDeliveryStockDetails = models.JSONField(default=dict)
    shopAttendantDeliveryStockDetails = models.JSONField(default=dict)
    expectedDriverDeliveryStockDetails = models.JSONField(default=dict)
    expectedShopAttendantDeliveryStockDetails = models.JSONField(default=dict)
    deliveryCustomersToTransfer = models.JSONField(default=dict)
    invoiceNumbers = models.JSONField(default=dict)
    allSubSales = models.JSONField(default=dict)
    allWholesales = models.JSONField(default=dict)
    allRetailSales = models.JSONField(default=dict)
    shopCustomersToTransfer = models.JSONField(default=dict)
    shopHandover = models.FloatField(default=0)
    TotalDeliveryHandover = models.FloatField(default=0)
    fullShopSalesAudit = models.JSONField(default=dict)
    fullDeliverySalesAudit = models.JSONField(default=dict)
    customersInDebt = models.JSONField(default=dict)
    customersCredit = models.JSONField(default=dict)
    messages = models.JSONField(default=dict)
    auditDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"audited details for {self.auditDate}"


class TodayAudit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    totalAuditId = models.FloatField(default=0.0)
    driver = models.CharField(max_length=100, default="Driver Name not set")
    shopAttendant = models.CharField(max_length=100, default="Shop Attendant name not Set")
    driverStatus = models.CharField(default="Driver has not closed", max_length=100)
    shopAttendantStatus = models.CharField(default="Shop attendant has not closed", max_length=100)
    openingStock = models.JSONField(default=dict)
    newStock = models.JSONField(default=dict)
    closingStock = models.JSONField(default=dict)
    driverDeliveryStockDetails = models.JSONField(default=dict)
    shopAttendantDeliveryStockDetails = models.JSONField(default=dict)
    expectedDriverDeliveryStockDetails = models.JSONField(default=dict)
    expectedShopAttendantDeliveryStockDetails = models.JSONField(default=dict)
    deliveryCustomersToTransfer = models.JSONField(default=dict)
    invoiceNumbers = models.JSONField(default=dict)
    allSubSales = models.JSONField(default=dict)
    allWholesales = models.JSONField(default=dict)
    allRetailSales = models.JSONField(default=dict)
    shopCustomersToTransfer = models.JSONField(default=dict)
    shopHandover = models.FloatField(default=0)
    TotalDeliveryHandover = models.FloatField(default=0)
    fullShopSalesAudit = models.JSONField(default=dict)
    fullDeliverySalesAudit = models.JSONField(default=dict)
    customersInDebt = models.JSONField(default=dict)
    customersCredit = models.JSONField(default=dict)
    messages = models.JSONField(default=dict)
    auditDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"audited details for {self.auditDate}"


class Catalogue(models.Model):
    name = models.CharField(max_length=100)
    referenceName = models.CharField(max_length=20)
    image = models.ImageField(null=False, blank=False)
    company = models.CharField(max_length=100, null=True)
    costPrice = models.FloatField()
    subPrice = models.FloatField()
    wholesalePrice = models.FloatField()
    retailPrice = models.FloatField()

    def __str__(self):
        return f"{self.name} is from {self.company}"



class messages(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    message_type = models.CharField(max_length=100)
    message_content = models.CharField(max_length=1000)
    message_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_content


class todayTauditId(models.Model):
    auditId = models.FloatField()

    def __str__(self):
        return f"Today's total audit Id is: {self.auditId}"

class Remmittance(models.Model):
    shopSalesHandover = models.FloatField(default=0)
    shopDeliveryHandover = models.FloatField(default=0)
    remmittedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shop Sales Handover {self.shopSalesHandover}, Delivery Handover(from shop attendant): {self.shopDeliveryHandover}"