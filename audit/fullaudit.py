from .models import Company, Products, SubDistributors, OpeningStockHistory, TodayOpeningStock, TodayNewStock, NewStockHistory, TodayClosingStock, ClosingStockHistory, AccessStatus, WholesaleRecord, RetailRecord, SubRecord, ShopDeliveryRecord, ActiveDeliveryStartRecord, ActiveDeliverySalesRecord, TodayDeliveryStartRecord, TodayDeliverySalesRecord, Invoice, Profile, TotalAudit, todayTauditId, TodayInvoiceNumber, messages, TodayAudit


def auditShopAttendantDelivery(sdelrec, tdStartRec):
    auditDict = {}
    
    for i in sdelrec:
        amountExp = 0
        vl = float(i.amountBroughtBack)
        dlNum = float(i.deliveryNumber)
        equivalentDeliveryRecord = tdStartRec.get(amountBroughtBack=vl)
        if equivalentDeliveryRecord:
            prodD = i.productData
            for a in prodD:
                valProduct = Products.objects.get(name=a)
                amountExp += (float(prodD[a]["productTaken"]) - float(prodD[a]["productBroughtBack"])) * (float(valProduct.wholesalePrice))

            auditDict[f"Amount expected for delivery {dlNum}"] = amountExp
            if float(amountExp) != float(vl):
                msg = messages.objects.create(message_type="Error", message_content="Recorded amount recieved by shop attendant and Audited amount are not equal")
            

        else:
            messg = messages.objects.create(message_type="Error", message_content="Delivery handover, amount recieved by shop attendant do not match")

            prodD = i.productData
            for a in prodD:
                valProduct = Products.objects.get(name=a)
                amountExp += (float(prodD[a]["productTaken"]) - float(prodD[a]["productBroughtBack"])) * (float(valProduct.wholesalePrice))

            auditDict[f"Amount expected for delivery {dlNum}"] = amountExp
            if float(amountExp) != float(vl):
                msg = messages.objects.create(message_type="Error", message_content="Recorded amount recieved by shop attendant and Audited amount are not equal")

                

def hello():
    print("Hi")