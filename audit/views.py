from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Company, Products, SubDistributors, OpeningStockHistory, TodayOpeningStock, TodayNewStock, NewStockHistory, TodayClosingStock, ClosingStockHistory, AccessStatus, WholesaleRecord, RetailRecord, SubRecord, ShopDeliveryRecord, ActiveDeliveryStartRecord, ActiveDeliverySalesRecord, TodayDeliveryStartRecord, TodayDeliverySalesRecord, Invoice, Profile, TotalAudit, todayTauditId, TodayInvoiceNumber, messages, TodayAudit, Remmittance, Catalogue
from datetime import date
import random
import json



@login_required(login_url='login')
def index(request):

    prof = Profile.objects.filter(user=request.user, role="deliverydriver")
    verifyAccess = Profile.objects.filter(user=request.user, accessStat=True)

    if verifyAccess:

        if prof:
            return redirect('delivery')
        else:    
            return render(request, 'audit/index.html')
    
    else:
        return redirect('login')


def login(request):
    messages = ""
    
    # usrs = User.objects.all()
    # for x in usrs:
    #     print(x.username)
    #     print(x.password)
    #     print("-----")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            valUserRole = User.objects.get(username=username)
            if Profile.objects.filter(user=valUserRole, role="shopattendant", accessStat=True).exists():
                auth.login(request, user)
                return redirect('index')

            elif Profile.objects.filter(user=valUserRole, role="deliverydriver", accessStat=True).exists():
                auth.login(request, user)
                return redirect('delivery')
            
            elif Profile.objects.filter(user=valUserRole, role="admin", accessStat=True).exists():
                auth.login(request, user)
                return redirect('index')

            else:
                messages = "You have not been granted access"

                # return redirect('login')

        else:
            messages = "You cannot access this page"

            # return redirect('login')

    return render(request, 'audit/login.html', {"messages": messages})


def wholesales(request):
    products = Products.objects.all()
    # prof = Profile.objects.get(user=request.user, role="deliverydriver")
    # verifyAccess = Profile.objects.get(user=request.user, accessStat=True)

    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')
        else:    
            return render(request, 'audit/wholesales.html', {"products": products})
    
    else:
        return redirect('login')


def retail(request):
    companies = Company.objects.all()
    products = Products.objects.all()

    prof = Profile.objects.filter(user=request.user, role="deliverydriver")
    verifyAccess = Profile.objects.filter(user=request.user, accessStat=True)

    if verifyAccess:

        if prof:
            return redirect('delivery')
        else:    
            if request.method == "POST":
                i = 0
                for p in request.POST:
                    i += 1
                    if i >= 2:
                        product = Products.objects.get(name=p)
                        if RetailRecord.objects.filter(product=product).exists():
                            newRetailQuantity= RetailRecord.objects.get(product=product)
                            nrq = int(newRetailQuantity.productQuantity) + int(request.POST[p])
                            newRetailQuantity.delete()
                            record = RetailRecord.objects.create(product=product, productQuantity=str(nrq), productPrice=product.retailPrice)
                            record.save()
                        else:
                            record = RetailRecord.objects.create(product=product, productQuantity=request.POST[p], productPrice=product.retailPrice)
                            record.save()
                return redirect("index") 
            return render(request, 'audit/retail.html', {"products": products})

    
    else:
        return redirect('login')

    

def subsMain(request):

    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')
        else:    
            subDistributors = SubDistributors.objects.all()
            return render(request, 'audit/subs-main.html', {"subDistributors": subDistributors})
    
    else:
        return redirect('login')

    

def subs(request, subname):

    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')
        else: 

            companies = Company.objects.all()
            products = Products.objects.all()

            if request.method == "POST":
                if request.POST["subsmodeofpayment"] == "Cash":
                    pData = {}
                    sbName = request.POST["subname"]
                    subproductvalue = request.POST["subproductvalue"]
                    submodeofpayment = request.POST["subsmodeofpayment"]
                    amtcollectedfromsub = request.POST["amtcollectedfromsub"]
                    substobalance = request.POST["substobalance"]
                    subsbalance = request.POST["subsbalance"]

                    a = 0

                    for i in request.POST:
                        a += 1
                        if a > 7:
                            pData[i] = request.POST[i]
                    
                    if SubDistributors.objects.filter(name=sbName).exists():
                        ActualSubDist = SubDistributors.objects.get(name=sbName)
                        subCashRecord = SubRecord.objects.create(subName=ActualSubDist, productData=pData, productValue=subproductvalue, modeOfPayment=submodeofpayment, amtFromSubDistributor=amtcollectedfromsub, subDistributorDebt=substobalance, subDistributorCredit=subsbalance)
                        subCashRecord.save()
                        return redirect('index')
                    else:
                        pass

                elif request.POST["subsmodeofpayment"] == "Transfer":
                    pData = {}
                    sbName = request.POST["subname"]
                    subproductvalue = request.POST["subproductvalue"]
                    submodeofpayment = request.POST["subsmodeofpayment"]
                    

                    a = 0

                    for i in request.POST:
                        a += 1
                        if a > 4:
                            pData[i] = request.POST[i]
                    
                    if SubDistributors.objects.filter(name=sbName).exists():
                        ActualSubDist = SubDistributors.objects.get(name=sbName)
                        subTransferRecord = SubRecord.objects.create(subName=ActualSubDist, productData=pData, productValue=subproductvalue, modeOfPayment=submodeofpayment)
                        subTransferRecord.save()
                        return redirect('index')

                    else:
                        pass


                elif request.POST["subsmodeofpayment"] == "POS":
                    pData = {}
                    sbName = request.POST["subname"]
                    subproductvalue = request.POST["subproductvalue"]
                    submodeofpayment = request.POST["subsmodeofpayment"]
                    

                    a = 0

                    for i in request.POST:
                        a += 1
                        if a > 4:
                            pData[i] = request.POST[i]
                    
                    if SubDistributors.objects.filter(name=sbName).exists():
                        ActualSubDist = SubDistributors.objects.get(name=sbName)
                        subPosRecord = SubRecord.objects.create(subName=ActualSubDist, productData=pData, productValue=subproductvalue, modeOfPayment=submodeofpayment)
                        subPosRecord.save()
                        return redirect('index')
                    else:
                        pass

                else:
                    pass

            return render(request, 'audit/subs.html', {"subname": subname, "products": products, "companies": companies})

            # if SubDistributors.objects.filter(name=subname).exists():
            #     if request.method == "POST":
            #         i = 0
            #         for n in request.POST:
            #             i += 1
            #             if i >= 2:
            #                 product = Products.objects.get(name=n)
            #                 sub = SubDistributors.objects.get(name=subname)
            #                 record = SubRecord.objects.create(subName=sub, product=product, productQuantity=request.POST[n], productPrice=product.subPrice)
            #                 record.save()
            # else:
            #     return redirect("index")
    
    else:
        return redirect('login')

    

def stockQuantity(request):



    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')
        else:    
            companies = Company.objects.all()
            products = Products.objects.all()

            tOpenStk = TodayOpeningStock.objects.all()
            sdrec = ShopDeliveryRecord.objects.all()
            tdStRec = TodayDeliveryStartRecord.objects.all()


            showOpeningStockBar = True

            if tOpenStk.first():
                showOpeningStockBar = False
            else:
                showOpeningStockBar = True

            

            if request.method == "POST":
                if 'opening-stock' in request.POST:
                    openVal = TodayOpeningStock.objects.all()
                    if openVal.first():
                        pass
                    else:
                        opdict = {}
                        mainVl = ""
                        op = 0
                        for y in request.POST:
                            op +=1
                            if op >= 3:
                                open = Products.objects.get(name=y)
                                opening = TodayOpeningStock.objects.create(product=open, quantity=request.POST[y])
                                opening.save()

                        #TodayOpeningStock table must be cleared after closing stock        


                        for x in openVal:
                            opdict[x.product.name] = x.quantity

                        u = 0
                        for y in openVal:
                            u += 1
                            mainVl = str(y.addedAt)
                            if u == 1:
                                break
                        
                        opdict["timeRegistered"] = mainVl

                        ops = OpeningStockHistory.objects.create(productsData=opdict)
                        ops.save()

                        showOpeningStockBar = False

                    todayaudit = TodayAudit.objects.all()
                    if todayaudit.first():
                        todayaudit.delete()
                    else:
                        pass

                    return redirect('index')

                            
                elif 'new-stock' in request.POST:
                    nwstHis = {}
                    nwVal = ""
                    nw = 0
                    for n in request.POST:
                        nw += 1
                        if nw >= 3:
                            new = Products.objects.get(name=n)
                            newSt = TodayNewStock.objects.create(product=new, quantity=request.POST[n])
                            newSt.save()

                    
                    nst = TodayNewStock.objects.all()
                    for x in nst:
                        nwstHis[x.product.name] = x.quantity

                    u = 0
                    for m in nst:
                        u += 1
                        nwVal = str(m.addedAt)
                        if u == 1:
                            break

                    nwstHis["timeRegistered"] = nwVal

                    nwSHistory = NewStockHistory.objects.create(productsData=nwstHis)
                    nwSHistory.save()



                    tnstHis = NewStockHistory.objects.filter(productsData={})
                    tnstHis.delete()

                    return redirect('index')

                                

                elif 'closing-stock' in request.POST:
                    clstHis = {}
                    clTxtVal = ""
                    clVal = TodayClosingStock.objects.all()
                    if clVal.first():
                        pass
                    else:
                        cl = 0
                        for c in request.POST:
                            cl += 1
                            if cl >= 3:
                                close = Products.objects.get(name=c)
                                closingSt = TodayClosingStock.objects.create(product=close, quantity=request.POST[c])
                                closingSt.save()


                        clst = TodayClosingStock.objects.all()
                        for x in clst:
                            clstHis[x.product.name] = x.quantity

                        u = 0
                        for m in clst:
                            u += 1
                            clTxtVal = str(m.addedAt)
                            if u == 1:
                                break

                        clstHis["timeRegistered"] = clTxtVal

                        clsHistory = ClosingStockHistory.objects.create(productsData=clstHis)
                        clsHistory.save()


                        clstHisEmpty = ClosingStockHistory.objects.filter(productsData={})
                        clstHisEmpty.delete()

                
                elif "closed" in request.POST:
                    shopSlsHandover = float(request.POST["shopsaleshandover"])
                    shopDlvryHandover = float(request.POST["shopdeliveryhandover"])

                    recordRemmittance = Remmittance.objects.create(shopSalesHandover=shopSlsHandover, shopDeliveryHandover=shopDlvryHandover)  
                    recordRemmittance.save()

                    auditDict = {}
                    sdelrec = ShopDeliveryRecord.objects.all()
                    for i in sdelrec:
                        amountExp = 0
                        vl = float(i.amountBroughtBack)
                        dlNum = float(i.deliveryNumber)
                        equivalentDeliveryRecord = TodayDeliveryStartRecord.objects.filter(amountBroughtBack=vl)
                        if equivalentDeliveryRecord:
                            prodD = i.productData
                            for a in prodD:
                                valProduct = Products.objects.get(name=a)
                                amountExp += (float(prodD[a]["productQuantity"]) - float(prodD[a]["productBroughtBack"])) * (float(valProduct.wholesalePrice))

                            auditDict[f"Amount expected for delivery {dlNum}"] = amountExp
                            if float(amountExp) != float(vl):
                                msg = messages.objects.create(message_type="Error", message_content=f"Recorded amount recieved by shop attendant and Audited amount for {dlNum} are not equal")
                                msg.save()
                            

                        else:
                            messg = messages.objects.create(message_type="Error", message_content=f"Delivery handover, amount recieved by shop attendant for delivery {dlNum} does not jkl match")
                            messg.save()

                            prodD = i.productData
                            for a in prodD:
                                valProduct = Products.objects.get(name=a)
                                amountExp += (float(prodD[a]["productQuantity"]) - float(prodD[a]["productBroughtBack"])) * (float(valProduct.wholesalePrice))

                            auditDict[f"Amount expected for delivery {dlNum}"] = amountExp
                            if float(amountExp) != float(vl):
                                mgssg = messages.objects.create(message_type="Error", message_content=f"Recorded amount recieved by shop attendant and Audited amount for {dlNum} are not equal")
                                mgssg.save()   
                    

                    randomValue = random.uniform(1, 100000)
                    openingStockDict = {}
                    newStockDict = {}
                    closingStockDict = {}
                    shopAttendantDeliveryStockDetailsDict = {}
                    expectedShopAttendantDeliveryStockDetails = {}
                    totalDeliveryHandover = 0
                    invoiceNumbers = {}
                    allSubSales = {}
                    allWholesales = {}
                    allRetailSales = {}
                    shopCustomersToTransfer = {}
                    totalShopHandover = 0
                    fullShopSalesAudit = {}
                    customersInDebt = {}
                    customerCredit = {}
                    msgs = {}
                    msgSet = {999}
                    opHs = OpeningStockHistory.objects.all()
                    nwHs = NewStockHistory.objects.all()
                    clHs = ClosingStockHistory.objects.all()
                    wholesaleRec = WholesaleRecord.objects.all()
                    retailRec = RetailRecord.objects.all()
                    subRec = SubRecord.objects.all()
                    shopDelRec = ShopDeliveryRecord.objects.all()
                    todayDelStartRec = TodayDeliveryStartRecord.objects.all()
                    todayDelSalesRec = TodayDeliverySalesRecord.objects.all()
                    invoiceNum = TodayInvoiceNumber.objects.all()
                    messgss = messages.objects.all()
                    transferWholesalers = WholesaleRecord.objects.filter(modeOfPayment="Transfer")
                    transferSubDistributors = SubRecord.objects.filter(modeOfPayment="Transfer")


                    for b in opHs:
                        openingStockDict[str(b.id)] = b.productsData
                    
                    for c in nwHs:
                        newStockDict[str(c.id)] = c.productsData

                    for d in clHs:
                        closingStockDict[str(d.id)] = d.productsData

                    for e in shopDelRec:
                        shopAttendantDeliveryStockDetailsDict[str(e.id)] = {"driverName": e.driverName, "productData": e.productData, "amountBroughtBack": e.amountBroughtBack, "deliveryStatus": e.deliveryStatus, "leftAt": str(e.leftAt)}

                    expectedShopAttendantDeliveryStockDetails = auditDict
                    
                    totalDeliveryHandover = float(shopDlvryHandover)

                    tnMb = TodayInvoiceNumber.objects.all()

                    for tn in tnMb:
                        invoiceNumbers[str(tn.id)] = tn.invoiceNumber

                    for f in invoiceNum:
                        invoiceNumbers[str(f.id)] = f.invoiceNumber

                    for g in subRec:
                        allSubSales[str(g.id)] = {"subName": g.subName.name, "productData": g.productData, "productValue": g.productValue, "modeOfPayment": g.modeOfPayment, "amtFromSubDistributor": g.amtFromSubDistributor, "subDistributorDebt": g.subDistributorDebt, "subDistributorCredit": g.subDistributorCredit, "soldAt": str(g.soldAt)}

                    for h in wholesaleRec:
                        allWholesales[str(h.customerId)] = {"customerName": h.customerName, "productsData": h.productsData, "productValue": h.productValue, "modeOfPayment": h.modeOfPayment, "amtFromCustomer": h.amtFromCustomer, "customerDebt": h.customerDebt, "customerCredit": h.customerCredit, "soldAt": str(h.soldAt)}

                    for l in retailRec:
                        retailRecProdValue = float(l.productQuantity) * float(l.productPrice)
                        allRetailSales[str(l.id)] = {"product": l.product.name, "productQuantity": l.productQuantity, "productPrice": l.productPrice, "productValue": retailRecProdValue, "soldAt": str(l.soldAt)}

                    for m in transferWholesalers:
                        shopCustomersToTransfer[str(m.customerId)] = {"customerName": m.customerName, "productValue": m.productValue, "modeOfPayment": m.modeOfPayment}

                    for n in transferSubDistributors:
                        shopCustomersToTransfer[str(n.id)] = {"customerName": n.subName.name, "productValue": n.productValue, "modeOfPayment": n.modeOfPayment}

                    totalShopHandover = float(shopSlsHandover)


                    totalSalesAmt = 0
                    rawSalesAmt = 0
                    audtMessg = {}
                    for o in wholesaleRec:
                        wholesaleCname = o.customerName
                        audt = 0
                        for p in o.productsData:
                            audtProd = Products.objects.get(name=p)
                            audt += float(o.productsData[p]) * float(audtProd.wholesalePrice)

                        rawSalesAmt += audt
                        audt -= float(o.customerDebt)
                        audt += float(o.customerCredit)
                        totalSalesAmt += audt

                        if o.modeOfPayment == "Cash":
                            if audt != float(o.amtFromCustomer):
                                audtMessg[f"Error in {wholesaleCname}'s transaction"] = f"Amount paid by {wholesaleCname} at {o.soldAt} is supposed to be {audt}"
                        else:
                            audtMessg["Info" ] = f"{wholesaleCname} is to make a transfer"


                    for q in retailRec:
                        rrItemValue = 0
                        rrItemValue += float(q.productQuantity) * float(q.productPrice)

                        rawSalesAmt += rrItemValue
                        totalSalesAmt += rrItemValue

                    for r in subRec:
                        subCname = r.subName.name
                        subSval = float(r.productValue)
                        rawSalesAmt += subSval
                        subSval -= float(r.subDistributorDebt)
                        subSval += float(r.subDistributorCredit)

                        if r.modeOfPayment == "Cash":
                            if subSval != float(r.amtFromSubDistributor):
                                audtMessg[f"Error in {subCname}'s transaction"] = f"Amount paid by {subCname} at {r.soldAt} is supposed to be {subSval}"
                        
                        else:
                            audtMessg["Info"] = f"{subCname} is to make a transfer"

                    for s in shopDelRec:
                        sdRecAmtBb = float(s.amountBroughtBack)

                        rawSalesAmt += sdRecAmtBb
                        totalSalesAmt += sdRecAmtBb

                    if shopSlsHandover != totalSalesAmt:
                        audtMessg["Shop sales handover and Expected sales handover do not match"] = f"Shop sales handover: #{shopSlsHandover}. Expected Handover: #{totalSalesAmt}"
                        mg = messages.objects.create(message_type="Error", message_content=f"Shop sales handover of #{shopSlsHandover} and Expected shop of #{totalSalesAmt} sales handover do not match")
                        mg.save()

                    fullShopSalesAudit["auditMessages"] = audtMessg
                    fullShopSalesAudit["expectedClosinghandover"] = totalSalesAmt
                    fullShopSalesAudit["rawSales"] = rawSalesAmt


                    for t in wholesaleRec:
                        whlsCname = t.customerName

                        if t.modeOfPayment == "Cash" and float(t.customerDebt) > 0.0:
                            customersInDebt[whlsCname] = f"{whlsCname} owes #{t.customerDebt} from products worth #{t.productValue}"

                        if t.modeOfPayment == "Cash" and float(t.customerCredit) >= 0.0:
                            customerCredit[whlsCname] = f"{whlsCname} has a balance of #{t.customerCredit}"

                        

                    msgsgs = messages.objects.all()

                    for w in msgsgs:
                        # msgs[str(w.id)] = {
                        #     "messagetype": w.message_type,
                        #     "messagecontent": w.message_content,
                        #     "messagedate": str(w.message_date)
                        # }
                        msgSet.add(w.message_content)

                    msgSet.discard(999)

                    uv = 0
                    for pq in list(msgSet):
                        uv += 1
                        msgs[str(uv)] = {
                            "message_content": pq
                        }


                    for u in subRec:
                        subcname = u.subName.name

                        if u.modeOfPayment == "Cash" and float(u.subDistributorDebt) > 0.0:
                            customersInDebt[subcname] = f"{subcname} owes #{u.subDistributorDebt} from products worth #{u.productValue}"

                        if u.modeOfPayment == "Cash" and float(u.subDistributorCredit) >= 0.0:
                            customerCredit[subcname] = f"{subcname} has a balance of #{u.subDistributorCredit}"



                    shopTaudit = TodayAudit.objects.all()

                    if shopTaudit.first():
                        shopTaudit.update(
                            totalAuditId=randomValue,
                            shopAttendant=str(request.user.username),
                            shopAttendantStatus="Shop Attendant has closed",
                            openingStock=openingStockDict,
                            newStock=newStockDict,
                            closingStock=closingStockDict,
                            shopAttendantDeliveryStockDetails=shopAttendantDeliveryStockDetailsDict,
                            expectedShopAttendantDeliveryStockDetails=expectedShopAttendantDeliveryStockDetails,
                            invoiceNumbers=invoiceNumbers,
                            allSubSales=allSubSales,
                            allWholesales=allWholesales,
                            allRetailSales=allRetailSales,
                            shopCustomersToTransfer=shopCustomersToTransfer,
                            shopHandover=totalShopHandover,
                            TotalDeliveryHandover=totalDeliveryHandover,
                            fullShopSalesAudit=fullShopSalesAudit,
                            customersInDebt=customersInDebt,
                            customersCredit=customerCredit,
                            messages=msgs
                        )
                    else:        

                        shopTodayAudit = TodayAudit.objects.create(
                            totalAuditId=randomValue,
                            shopAttendant=str(request.user.username),
                            shopAttendantStatus="Shop Attendant has closed",
                            openingStock=openingStockDict,
                            newStock=newStockDict,
                            closingStock=closingStockDict,
                            shopAttendantDeliveryStockDetails=shopAttendantDeliveryStockDetailsDict,
                            expectedShopAttendantDeliveryStockDetails=expectedShopAttendantDeliveryStockDetails,
                            invoiceNumbers=invoiceNumbers,
                            allSubSales=allSubSales,
                            allWholesales=allWholesales,
                            allRetailSales=allRetailSales,
                            shopCustomersToTransfer=shopCustomersToTransfer,
                            shopHandover=totalShopHandover,
                            TotalDeliveryHandover=totalDeliveryHandover,
                            fullShopSalesAudit=fullShopSalesAudit,
                            customersInDebt=customersInDebt,
                            customersCredit=customerCredit,
                            messages=msgs
                        )

                        shopTodayAudit.save()

                    # tlAudit = TodayAudit.objects.all()
                    # tlList = []
                    # for z in tlAudit:
                    #     if z.driverStatus == "Driver has closed":
                    #         if z.shopAttendantStatus == "Shop Attendant has closed":
                    #             tlList.append(z)
                    #             TotalAudit.objects.bulk_create(tlList)

                    tlAudit = TodayAudit.objects.all()
                    for z in tlAudit:
                        if z.driverStatus == "Driver has closed":
                            if z.shopAttendantStatus == "Shop Attendant has closed":
                                recordTotalAudit = TotalAudit.objects.create(
                                totalAuditId=z.totalAuditId,
                                driver=z.driver,
                                shopAttendant=z.shopAttendant,
                                driverStatus=z.driverStatus,
                                shopAttendantStatus=z.shopAttendantStatus,
                                openingStock=z.openingStock,
                                newStock=z.newStock,
                                closingStock=z.closingStock,
                                driverDeliveryStockDetails=z.driverDeliveryStockDetails,
                                shopAttendantDeliveryStockDetails=z.shopAttendantDeliveryStockDetails,
                                expectedDriverDeliveryStockDetails=z.expectedDriverDeliveryStockDetails,
                                expectedShopAttendantDeliveryStockDetails=z.expectedShopAttendantDeliveryStockDetails,
                                deliveryCustomersToTransfer=z.deliveryCustomersToTransfer,
                                invoiceNumbers=z.invoiceNumbers,
                                allSubSales=z.allSubSales,
                                allWholesales=z.allWholesales,
                                allRetailSales=z.allRetailSales,
                                shopCustomersToTransfer=z.shopCustomersToTransfer,
                                shopHandover=z.shopHandover,
                                TotalDeliveryHandover=z.TotalDeliveryHandover,
                                fullShopSalesAudit=z.fullShopSalesAudit,
                                fullDeliverySalesAudit=z.fullDeliverySalesAudit,
                                customersInDebt=z.customersInDebt,
                                customersCredit=z.customersCredit,
                                messages=z.messages,
                            )

                            recordTotalAudit.save()
                    
                    


                    getTdAudit = TodayAudit.objects.all()
                    gettAudit = getTdAudit.first()

                    if gettAudit.driverStatus == "Driver has closed" and gettAudit.shopAttendantStatus == "Shop Attendant has closed":
                        opensh = OpeningStockHistory.objects.all()                
                        topens = TodayOpeningStock.objects.all()  
                        tnews = TodayNewStock.objects.all()             
                        newsh = NewStockHistory.objects.all()             
                        tclosings = TodayClosingStock.objects.all()             
                        csh = ClosingStockHistory.objects.all()             
                        wr = WholesaleRecord.objects.all()             
                        rr = RetailRecord.objects.all()             
                        sr = SubRecord.objects.all()             
                        sdr = ShopDeliveryRecord.objects.all()             
                        adstr = ActiveDeliveryStartRecord.objects.all()             
                        adsar = ActiveDeliverySalesRecord.objects.all()             
                        tdstr = TodayDeliveryStartRecord.objects.all()             
                        tdsar = TodayDeliverySalesRecord.objects.all()             
                        tdaid = todayTauditId.objects.all()     
                        tinvn = TodayInvoiceNumber.objects.all()             
                        mgs = messages.objects.all()             
                        rmt = Remmittance.objects.all()             

                        opensh.delete()       
                        topens.delete()       
                        tnews.delete()       
                        newsh.delete()       
                        tclosings.delete()       
                        csh.delete()       
                        wr.delete()       
                        rr.delete()       
                        sr.delete()       
                        sdr.delete()       
                        adstr.delete()       
                        adsar.delete()       
                        tdstr.delete()       
                        tdsar.delete()       
                        tdaid.delete()       
                        tinvn.delete()       
                        mgs.delete()       
                        rmt.delete() 

                    else:
                        pass
                            

                        
                    profchange = Profile.objects.filter(user=request.user, role="shopattendant", accessStat=True)
                    if profchange:
                        profchange.update(accessStat=False)

                    auth.logout(request)
                    return redirect('login')



            context = {"products": products, "companies": companies, "showOpeningStockBar": showOpeningStockBar}
            
            
                        
            return render(request, 'audit/stock-quantity.html', context)

    
    else:
        return redirect('login')


    

def confirmation(request):


    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')
        else:    
            if request.method == "POST":

                if request.POST["modeOfPayment"] == "Cash":
                    productsData = {}
                    customername = request.POST["customerName"]
                    productval = request.POST["productValue"]
                    cashPaymentMode = request.POST["modeOfPayment"]
                    amtFromCustomer =  request.POST["amtFromCustomer"]
                    customerdebt = request.POST["customerDebt"]
                    customercredit = request.POST["customerCredit"]

                    i = 0

                    for x in request.POST:
                        i += 1
                        if i > 7:
                            productsData[x] = request.POST[x]

                    cashWholesalesRecord = WholesaleRecord.objects.create(customerName=customername, productsData=productsData, productValue=productval, modeOfPayment=cashPaymentMode, amtFromCustomer=amtFromCustomer, customerDebt=customerdebt, customerCredit=customercredit)
                    cashWholesalesRecord.save()
                    return redirect("index")

                elif request.POST["modeOfPayment"] == "Transfer":
                    productsData = {}
                    customername = request.POST["customerName"]
                    productval = request.POST["productValue"]
                    transferPaymentMode = request.POST["modeOfPayment"]

                    i = 0

                    for x in request.POST:
                        i += 1
                        if i > 5:
                            productsData[x] = request.POST[x]

                    transferWholesalesRecord = WholesaleRecord.objects.create(customerName=customername, productsData=productsData, productValue=productval, modeOfPayment=transferPaymentMode)
                    transferWholesalesRecord.save()
                    return redirect("index")
                elif request.POST["modeOfPayment"] == "POS":
                    productsData = {}
                    customername = request.POST["customerName"]
                    productval = request.POST["productValue"]
                    posPaymentMode = request.POST["modeOfPayment"]

                    i = 0

                    for x in request.POST:
                        i += 1
                        if i > 5:
                            productsData[x] = request.POST[x]

                    posWholesalesRecord = WholesaleRecord.objects.create(customerName=customername, productsData=productsData, productValue=productval, modeOfPayment=posPaymentMode)
                    posWholesalesRecord.save()
                    return redirect("index")
                else:
                    pass
                # prodData = {}
                # i = 0
                # cName = request.POST["customerName"]
                # for n in request.POST:
                #     i += 1
                #     if i >= 3:
                #         product = Products.objects.get(name=n)
                #         record = WholesaleRecord.objects.create(customerName=cName, productsData=product, productQuantity=request.POST[n])
                #         record.save()    

            return render(request, 'audit/confirmation.html')

    
    else:
        return redirect('login')


    

def adminPanel(request):

    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')

        elif Profile.objects.filter(user=request.user, role="admin").exists():    
            companies = Company.objects.all()
            products = Products.objects.all()
            openingStock = OpeningStockHistory.objects.all()
            newStock = NewStockHistory.objects.all()
            todOpStock = TodayOpeningStock.objects.all()
            todNewStock = TodayNewStock.objects.all()
            todClosingStock = TodayClosingStock.objects.all()
            closingStock = ClosingStockHistory.objects.all()
            subRecord = SubRecord.objects.all()
            shopdel = ShopDeliveryRecord.objects.all()
            retailRecord = RetailRecord.objects.all()
            wholesaleRecord = WholesaleRecord.objects.all()
            activeStartRecord = ActiveDeliveryStartRecord.objects.all()
            activeSalesRecord = ActiveDeliverySalesRecord.objects.all()
            todayAllStartRecord = TodayDeliveryStartRecord.objects.all()
            todayAllSalesRecord = TodayDeliverySalesRecord.objects.all()
            invoices = Invoice.objects.all()
            todInvNum = TodayInvoiceNumber.objects.all()
            todAudit = TodayAudit.objects.all()
            totAudit = TotalAudit.objects.all()
            catalogue = Catalogue.objects.all()
            




            def goLive(openingstock, newstock, subrecord, wholesalerecord, retailrecord, shopdeliveryrecord, activestartrecord, activesalesrecord, todayallstartrecord, todayallsalesrecord):
                opStockCalcValue = 0
                nwStockCalcValue = 0
                nwStockProfitValue = 0
                totalCustomerDebt = 0
                totalCustomerBalance = 0
                totalShopSalesValue = 0
                totalAmountOfMoneyInShop = 0
                deliveryExpectedAmountBasedOnSales = {}
                fullDeliveryAudit = {}
                productsAvailableVerify = {}
                pavLst = list(productsAvailableVerify)
                #The productsAvailable variable actually means products sold
                productsAvailable = {}
                #The productsAvailableActual variable actually means products remaining
                productsAvailableActual = {}
                #The allproductsAvailable variable actually means all products originally recieved
                allProductsAvailable = {}
                customersToTransfer = {}
                customersInDebt = {}
                customersCredit = {}
                fullDeliveryamountexpperDelivery = {}
                totCashexpfromDeliveries = {}
                allDelSales = {}
                shopDeliveryRecorded = {}
                

                for x in openingstock:
                    opStockCalcValue += float(x.product.costPrice) * float(x.quantity)
                    pavLst.append(x.product.name)


                actualOpeningStockValue = opStockCalcValue

                for y in newstock:
                    nwStockCalcValue += float(y.product.costPrice) * float(y.quantity)
                    nwStockProfitValue += (float(y.product.wholesalePrice) - float(y.product.costPrice)) * float(y.quantity)
                    pavLst.append(y.product.name)

                
                productsAvailableVerify = set(pavLst)


                actualNewStockCalcValue = nwStockCalcValue
                actualNewStockProfitValue = nwStockProfitValue

                for m in list(productsAvailableVerify):
                    productsAvailable[m] = 0

                for z in subrecord:
                    totalCustomerDebt += float(z.subDistributorDebt)
                    totalCustomerBalance += float(z.subDistributorCredit)
                    totalShopSalesValue += float(z.productValue)
                    totalAmountOfMoneyInShop += float(z.amtFromSubDistributor)

                    if z.modeOfPayment == "Cash":
                        if float(z.subDistributorDebt) != 0.0:
                            if z.subName in customersInDebt:
                                customersInDebt[z.subName.name] += z.subDistributorDebt
                            else:
                                customersInDebt[z.subName.name] = z.subDistributorDebt

                    if z.modeOfPayment == "Cash":
                        if float(z.subDistributorCredit) != 0.0:
                            if z.subName in customersCredit:
                                customersCredit[z.subName.name] += z.subDistributorCredit
                            else:
                                customersCredit[z.subName.name] = z.subDistributorCredit


                    for a in z.productData:
                        if a in productsAvailable:
                            productsAvailable[a] += float(z.productData[a])
                
                    if z.modeOfPayment != "Cash":
                        if z.subName in customersToTransfer:
                            customersToTransfer[z.subName] += float(z.productValue)
                        else:
                            customersToTransfer[z.subName] = float(z.productValue)

                    
                for b in wholesalerecord:
                    totalCustomerDebt += float(b.customerDebt)
                    totalCustomerBalance += float(b.customerCredit)
                    totalShopSalesValue += float(b.productValue)
                    totalAmountOfMoneyInShop += float(b.amtFromCustomer)

                    if b.modeOfPayment == "Cash":
                        if float(b.customerDebt) != 0.0:
                            if b.customerName in customersInDebt:
                                customersInDebt[b.customerName] += b.customerDebt
                            else:
                                customersInDebt[b.customerName] = b.customerDebt

                    if b.modeOfPayment == "Cash":
                        if float(b.customerCredit) != 0.0:
                            if b.customerName in customersCredit:
                                customersCredit[b.customerName] += b.customerCredit
                            else:
                                customersCredit[b.customerName] =  b.customerCredit


                    for c in b.productsData:
                        if c in productsAvailable:
                            productsAvailable[c] += float(b.productsData[c])

                    if b.modeOfPayment != "Cash":
                        if b.customerName in customersToTransfer:
                            customersToTransfer[b.customerName] += float(b.productValue)
                        else:
                            customersToTransfer[b.customerName] = float(b.productValue)


                for d in retailrecord:
                    totalShopSalesValue += (float(d.productQuantity) * float(d.productPrice))
                    totalAmountOfMoneyInShop += (float(d.productQuantity) * float(d.productPrice))
                    if d.product.name in productsAvailable:
                        productsAvailable[d.product.name] += float(d.productQuantity)


                for e in shopdeliveryrecord:
                    #Expected shop delivery amount(per delivery) based on sales should be done on the front-end
                    if e.deliveryStatus == "delivered":
                        totalAmountOfMoneyInShop += float(e.amountBroughtBack)
                        for f in e.productData:
                            if f in productsAvailable:
                                productsAvailable[f] += (float(e.productData[f]["productQuantity"]) - float(e.productData[f]["productBroughtBack"]))

                            


                        shopDeliveryRecAmtExpVal = 0

                        for g in e.productData:
                            shopDeliveryRecAmtExpVal += ((float(e.productData[g]["productQuantity"]) - float(e.productData[g]["productBroughtBack"])) * float(e.productData[g]["productPrice"]))


                        shopDeliveryRecorded[e.id] = {"driverName": e.driverName, "productData": e.productData, "amountBroughtBack": e.amountBroughtBack, "amountExpected": shopDeliveryRecAmtExpVal, "deliveryStatus": e.deliveryStatus}

                    else:
                        for k in e.productData:
                            if k in productsAvailable:
                                productsAvailable[k] += (float(e.productData[k]["productQuantity"]))



                for h in openingstock:
                    allProductsAvailable[h.product.name] = float(h.quantity)

                for i in newstock:
                    if i.product.name in allProductsAvailable:
                        allProductsAvailable[i.product.name] += float(i.quantity)
                    else:
                        allProductsAvailable[i.product.name] = float(i.quantity)

                for j in productsAvailable:
                    if j in allProductsAvailable:
                        productsAvailableActual[j] = float(allProductsAvailable[j]) - float(productsAvailable[j])

                shopDeliveryNotDelivered = shopdeliveryrecord.filter(deliveryStatus="still delivering")

                for tstr in todayallstartrecord:
                    delamntexp = 0
                    for tspData in tstr.productsData:
                        delexpProduct = Products.objects.get(name=tspData)
                        delamntexp += ((float(tstr.productsData[tspData]['productTakenQuantity']) - float(tstr.productsData[tspData]['productBroughtBackQuantity'])) * float(delexpProduct.wholesalePrice))

                    deliveryExpectedAmountBasedOnSales[f"Delivery amount expected for {tstr.deliveryNumber}"] = f"#{delamntexp}"

                fullDelAudtMessgs = {}
                deliverytransfers = {}
                deliverydebtors = {}
                deliverycreditors = {}
                for tstart in todayallstartrecord:
                    delPTaken = {}
                    for tstartData in tstart.productsData:
                        delPTaken[tstartData] = float(tstart.productsData[tstartData]['productTakenQuantity'])
                    
                    tsales = todayallsalesrecord.filter(salesId=float(tstart.salesId))

                    totalAmountExpDelivery = 0
                    delRawSalesAmt = 0
                    for tslss in tsales:
                        delexpamtBb = 0
                        for tsl in tslss.allCustomerData:
                            delexpamtBb += float(tslss.allCustomerData[tsl]['amtFromCustomer'])
                            delRawSalesAmt += float(tslss.allCustomerData[tsl]['productValue'])

                            if tslss.allCustomerData[tsl]['modeOfPayment'] != "Cash":
                                deliverytransfers[tsl] = f"is to transfer #{tslss.allCustomerData[tsl]['productValue']}"

                            if  float(tslss.allCustomerData[tsl]['customerDebt']) >= 0.0:
                                deliverydebtors[tsl] = f"has a debt of #{tslss.allCustomerData[tsl]['customerDebt']}"

                            if float(tslss.allCustomerData[tsl]['customerCredit'])  >= 0.0:
                                deliverycreditors[tsl] = f"has a balance of #{tslss.allCustomerData[tsl]['customerCredit']}"
                            
                            for ts in tslss.allCustomerData[tsl]['productsPurchased']:
                                if ts in delPTaken:
                                    delPTaken[ts] -= float(tslss.allCustomerData[tsl]['productsPurchased'][ts])
                                else:
                                    fullDelAudtMessgs["Delivery Error"] = f"{ts} was not recorded but was sold"
                    
                    totalAmountExpDelivery += delexpamtBb
                    fullDeliveryAudit[f"Expected products brought back from delivery {tstart.deliveryNumber} (from audit)"] = delPTaken
                    fullDeliveryamountexpperDelivery[f"Amount(money) expected from delivery {tstart.deliveryNumber}(from audit)"] = delexpamtBb

                totCashexpfromDeliveries["Total Cash amount expected from all Deliveries(from audit)"] = totalAmountExpDelivery
                allDelSales["All Delivery sales total [transfers, pos, cash](from audit)"] = delRawSalesAmt
                fullDeliveryAudit["All Customers to make a Transfer"] = deliverytransfers
                fullDeliveryAudit["All Debtors"] = deliverydebtors
                fullDeliveryAudit["All customers with balances"] = deliverycreditors
                fullDeliveryAudit["messages"] = fullDelAudtMessgs 

                
                goLiveVariables = {
                    "openingstock": openingstock,
                    "newstock": newstock,
                    "subrecord": subrecord,
                    "wholesalerecord": wholesalerecord,
                    "retailrecord": retailrecord,
                    "shopDeliveryNotDelivered": shopDeliveryNotDelivered,
                    "openingStockCalculatedValue": opStockCalcValue,
                    "newStockCalculatedValue": nwStockCalcValue,
                    "newStockProfitValue": nwStockProfitValue,
                    "totalCustomerDebtValue": totalCustomerDebt,
                    "totalCustomerBalanceValue": totalCustomerBalance,
                    "totalShopSalesValue": totalShopSalesValue,
                    "totalAmountOfMoneyInShop": totalAmountOfMoneyInShop,
                    "productsSold": productsAvailable,
                    "productsRemaining": productsAvailableActual,
                    "allProductsOriginallyAvailable": allProductsAvailable,
                    "customersToTransfer": customersToTransfer,
                    "customersInDebt": customersInDebt,
                    "customersCredit": customersCredit,
                    "shopDeliveryRecorded": shopDeliveryRecorded,
                    "shopDeliveryNotDelivered": shopDeliveryNotDelivered,
                    "activeStartRecord": activestartrecord,
                    "activeSalesRecord": activesalesrecord,
                    "todayAllStartRecord": todayallstartrecord,
                    "todayAllSalesRecord": todayallsalesrecord,
                    "deliveryExpectedAmountBasedOnSales": deliveryExpectedAmountBasedOnSales,
                    "fullDeliveryAudit": fullDeliveryAudit,
                    "fullDeliveryamountexpperDelivery": fullDeliveryamountexpperDelivery,
                    "totCashexpfromDeliveries": totCashexpfromDeliveries,
                    "allDelSales": allDelSales
                }

                return goLiveVariables        



            def calcTnewStockValue(tns):
                totalPriceOfItem = []
                for tnsp in tns:
                    tnP = Products.objects.get(name=tnsp.product.name)
                    nsTotValue = tnP.costPrice * tnsp.quantity
                    totalPriceOfItem.append(nsTotValue)

                newvle = 0
                for x in totalPriceOfItem:
                    newvle += x

                return newvle

            def showTableProducts(tosl, tnsl):
                tosProducts = []
                tnsProducts = []

                for tops in tosl:
                    tosProducts.append(tops.product)

                for tnsp in tnsl:
                    tnsProducts.append(tnsp.product)

                tpProducts = tosProducts + tnsProducts                



            def showTodayInvoices(todayInvoiceNumbers, invcs):
                invarr = []
                for x in todayInvoiceNumbers:
                    inv = invcs.get(invoiceNumber=x.invoiceNumber)
                    invarr.append(inv)

                
                return invarr

            if todInvNum.first():
                shTodayInv = showTodayInvoices(todInvNum, invoices)


            if request.method == "POST":
                if "addcatalogueproducts" in request.POST:
                    catNameOfProduct = request.POST['cataloguenameofproduct'] 
                    catRefNameOfProduct = request.POST['cataloguerefnameofproduct']
                    catImageOfProduct = request.FILES.get("catalogueimageofproduct")
                    catCompanyOfProduct = request.POST['cataloguecompanyofproduct']
                    catCostPriceOfProduct = request.POST['cataloguecostpriceofproduct']
                    catSubPriceOfProduct = request.POST['cataloguesubpriceofproduct']
                    catWholesalePriceOfProduct = request.POST['cataloguewholesalepriceofproduct']
                    catRetailPriceOfProduct = request.POST['catalogueretailpriceofproduct']

                    catCreate = Catalogue.objects.create(name=catNameOfProduct, referenceName=catRefNameOfProduct, company=catCompanyOfProduct, costPrice=catCostPriceOfProduct, subPrice=catSubPriceOfProduct, wholesalePrice=catWholesalePriceOfProduct, retailPrice=catRetailPriceOfProduct, image=catImageOfProduct,)
                    catCreate.save()

                elif "deletecatalogueproduct" in request.POST:
                    delCatNameOfProduct = request.POST['cataloguedeletenameofproduct']

                    catDelete = Catalogue.objects.filter(name=delCatNameOfProduct)
                    catDelete.delete()

                elif "admingrantaccess" in request.POST:
                    NoAccessProfiles = Profile.objects.filter(accessStat=False)
                    NoAccessProfiles.update(accessStat=True)  

                elif 'clearentiredatabase' in request.POST:
                    com = Company.objects.all()
                    pro = Products.objects.all()
                    sub = SubDistributors.objects.all()                
                    opensh = OpeningStockHistory.objects.all()                
                    topens = TodayOpeningStock.objects.all()  
                    tnews = TodayNewStock.objects.all()             
                    newsh = NewStockHistory.objects.all()             
                    tclosings = TodayClosingStock.objects.all()             
                    csh = ClosingStockHistory.objects.all()             
                    accst = AccessStatus.objects.all()             
                    wr = WholesaleRecord.objects.all()             
                    rr = RetailRecord.objects.all()             
                    sr = SubRecord.objects.all()             
                    sdr = ShopDeliveryRecord.objects.all()             
                    adstr = ActiveDeliveryStartRecord.objects.all()             
                    adsar = ActiveDeliverySalesRecord.objects.all()             
                    tdstr = TodayDeliveryStartRecord.objects.all()             
                    tdsar = TodayDeliverySalesRecord.objects.all()             
                    inv = Invoice.objects.all()             
                    tla = TotalAudit.objects.all()             
                    tdaid = todayTauditId.objects.all()     
                    tinvn = TodayInvoiceNumber.objects.all()             
                    mgs = messages.objects.all()             
                    tda = TodayAudit.objects.all()             
                    rmt = Remmittance.objects.all()             
                    cat = Catalogue.objects.all()      

                    com.delete()
                    pro.delete()       
                    sub.delete()       
                    opensh.delete()       
                    topens.delete()       
                    tnews.delete()       
                    newsh.delete()       
                    tclosings.delete()       
                    csh.delete()       
                    accst.delete()       
                    wr.delete()       
                    rr.delete()       
                    sr.delete()       
                    sdr.delete()       
                    adstr.delete()       
                    adsar.delete()       
                    tdstr.delete()       
                    tdsar.delete()       
                    inv.delete()       
                    tla.delete()       
                    tdaid.delete()       
                    tinvn.delete()       
                    mgs.delete()       
                    tda.delete()       
                    rmt.delete()       
                    cat.delete()    


                elif "manuallycloseshop" in request.POST:
                    opensh = OpeningStockHistory.objects.all()                
                    topens = TodayOpeningStock.objects.all()  
                    tnews = TodayNewStock.objects.all()             
                    newsh = NewStockHistory.objects.all()             
                    tclosings = TodayClosingStock.objects.all()             
                    csh = ClosingStockHistory.objects.all()             
                    wr = WholesaleRecord.objects.all()             
                    rr = RetailRecord.objects.all()             
                    sr = SubRecord.objects.all()             
                    sdr = ShopDeliveryRecord.objects.all()             
                    adstr = ActiveDeliveryStartRecord.objects.all()             
                    adsar = ActiveDeliverySalesRecord.objects.all()             
                    tdstr = TodayDeliveryStartRecord.objects.all()             
                    tdsar = TodayDeliverySalesRecord.objects.all()             
                    tdaid = todayTauditId.objects.all()     
                    tinvn = TodayInvoiceNumber.objects.all()             
                    mgs = messages.objects.all()             
                    rmt = Remmittance.objects.all()            
 

                    opensh.delete()       
                    topens.delete()       
                    tnews.delete()       
                    newsh.delete()       
                    tclosings.delete()       
                    csh.delete()       
                    wr.delete()       
                    rr.delete()       
                    sr.delete()       
                    sdr.delete()       
                    adstr.delete()       
                    adsar.delete()       
                    tdstr.delete()       
                    tdsar.delete()       
                    tdaid.delete()       
                    tinvn.delete()       
                    mgs.delete()       
                    rmt.delete() 


                    todAudit = TodayAudit.objects.all()
                    bulkCrteLst = []
                    for tda in todAudit:
                        bulkCrteLst.append(tda)
                        TotalAudit.objects.bulk_create(bulkCrteLst)


                      

                else:
                    return redirect("login")

            
            #goLiveCon stands for "goLiveContext"
            if wholesaleRecord.first():
                goLiveCon = goLive(todOpStock, todNewStock, subRecord, wholesaleRecord, retailRecord, shopdel, activeStartRecord, activeSalesRecord, todayAllStartRecord, todayAllSalesRecord)

                        



            context = {
            "products": products, 
            "companies": companies, 
            "openingStock": openingStock, 
            "newStock": newStock, 
            "closingStock": closingStock, 
            "shopdel": shopdel,
            # "goLiveCon": goLiveCon,
            "invoices": invoices,
            # "shTodayInv": shTodayInv,
            "todAudit": todAudit,
            "totAudit": totAudit,
            "catalogue": catalogue
            }

            if todInvNum.first():
                context["shTodayInv"] = shTodayInv



            if wholesaleRecord.first():
                context["goLiveCon"] = goLiveCon

                
            tNewStock = TodayNewStock.objects.all()

            if tNewStock.first():
                calculatedNewStockValue = calcTnewStockValue(tNewStock)
                context["tNewStock"] = tNewStock
                context["calculatedNewStockValue"] = calculatedNewStockValue
            else:
                pass


            if todOpStock.first() or todNewStock.first():
                tableHeaders = showTableProducts(todOpStock, todNewStock)
                context["tableHeaders"] = tableHeaders
                context["todOpStock"] = todOpStock
                context["todNewStock"] = todNewStock
            else:
                pass

            if todClosingStock.first():
                context["todClosingStock"] = todClosingStock
            else:
                pass

            if retailRecord.first():
                context["retailRecord"] = retailRecord
            else:
                pass

            if subRecord.first():
                context["subRecord"] = subRecord
            else:
                pass


            if todAudit.first():
                messgs = []
                i = 0
                for todAdt in todAudit:
                    for todmssgs in todAdt.messages:
                        if int(todmssgs) != 4:
                            messgs.append(todAdt.messages[todmssgs]['message_content'])
                            i += 1
                        else:
                            break
                context["messgs"] = messgs
            else:
                pass

        

            # if Profile.objects.filter(user=request.user, role="admin", accessStat=True).exists():
            return render(request, 'audit/admin-panel.html', context)
            
            # else:
            #     return redirect('login')
        else:
            return redirect('login')
    else:
        return redirect('login')


    


def settings(request):
    

    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')

        elif Profile.objects.filter(user=request.user, role="admin").exists():    
            companies = Company.objects.all()
            if 'createnewemployee' in request.POST:
                newEmployeeName = request.POST['newemployeename']
                newEmployeePassword = request.POST['newemployeepassword']

                newUser = User.objects.create_user(username=newEmployeeName, password=newEmployeePassword)
                newUser.save()

                athUser = User.objects.get(username=newEmployeeName)
                newProfile = Profile.objects.create(user=athUser, role="shopattendant", accessStat=True)
                newProfile.save()
                return redirect('settings')

            elif 'deleteoldemployee' in request.POST:
                delEmployeeName = request.POST['delemployeename']

                delUser = User.objects.get(username=delEmployeeName)
                delProfile = Profile.objects.get(user=delUser)
                delProfile.delete()
                delUser.delete()
                return redirect('settings')


            elif 'createnewproduct' in request.POST:
                nameOfProduct = request.POST['nameofproduct']
                refNameOfProduct = request.POST['refnameofproduct']
                imageOfProduct = request.FILES.get("imageofproduct")
                costPriceOfProduct = request.POST['costpriceofproduct']
                subPriceOfProduct = request.POST['subpriceofproduct']
                wholesalePriceOfProduct = request.POST['wholesalepriceofproduct']
                retailPriceOfProduct = request.POST['retailpriceofproduct']

                if 'fromexistingcompany' in request.POST:
                    getCompany = Company.objects.get(name=request.POST['fromexistingcompany'])
                    newProduct = Products.objects.create(name=nameOfProduct, referenceName=refNameOfProduct, image=imageOfProduct, company=getCompany, costPrice=costPriceOfProduct, subPrice=subPriceOfProduct, wholesalePrice=wholesalePriceOfProduct, retailPrice=retailPriceOfProduct)
                    newProduct.save()
                    return redirect('settings')

                elif 'newcompanyname' in request.POST:
                    crtecompany = Company.objects.create(name=request.POST['newcompanyname'], referenceName=request.POST['refnameofnewcompany'])
                    crtecompany.save()
                    makeNewProduct = Products.objects.create(name=nameOfProduct, referenceName=refNameOfProduct, image=imageOfProduct, company=crtecompany, costPrice=costPriceOfProduct, subPrice=subPriceOfProduct, wholesalePrice=wholesalePriceOfProduct, retailPrice=retailPriceOfProduct)
                    makeNewProduct.save()

                    return redirect('settings')

                else:
                    pass

            elif 'removeoldproduct' in request.POST:
                    remPt = request.POST['nameofproduct']
                    getProductToRemove = Products.objects.get(name=remPt)
                    getProductToRemove.delete()     
                    return redirect('settings')


            
            elif 'changepriceofproduct' in request.POST:
                cpNameOfProduct = request.POST['nameofproduct']
                cpNewCostPriceOfProduct = request.POST['newcostpriceofproduct']
                cpNewSubPriceOfProduct = request.POST['newsubpriceofproduct']
                cpNewWholesalePriceOfProduct = request.POST['newwholesalepriceofproduct']
                cpNewRetailPriceOfProduct = request.POST['newretailpriceofproduct']

                cpGetProduct = Products.objects.filter(name=cpNameOfProduct)
                cpGetProduct.update(costPrice=cpNewCostPriceOfProduct, subPrice=cpNewSubPriceOfProduct, wholesalePrice=cpNewWholesalePriceOfProduct, retailPrice=cpNewRetailPriceOfProduct)
                return redirect('settings')


            elif 'changeyourpassword' in request.POST:
                nameOfAdmin = request.POST['nameofadmin']
                passwordOfAdmin = request.POST['passwordofadmin']
                nameOfNewAdmin = request.POST['nameofnewadmin']
                passwordOfNewAdmin = request.POST['passwordofnewadmin']

                if Users.objects.filter(username=nameOfAdmin, password=passwordOfAdmin).exists():
                    oldUser = User.objects.get(username=nameOfAdmin, password=passwordOfAdmin)
                    oldProfile = Profile.objects.get(user=oldUser, role="admin")
                    oldUser.delete()
                    oldProfile.delete()

                    newUser = User.objects.create(username=nameOfNewAdmin, password=passwordOfNewAdmin)
                    newUser.save()
                    newProfile = Profile.objects.create(user=newUser, role="admin", accessStat=True)
                    newProfile.save()
                    return redirect('settings')


                else:
                    messages.info(request, "The credentials of the admin were incorrect!!")
                    return redirect('settings')



            elif 'createnewdriver' in request.POST:
                newDriverName = request.POST['newdrivername']
                newDriverPassword = request.POST['newdriverpassword']

                addNewUser = User.objects.create_user(username=newDriverName, password=newDriverPassword)
                addNewUser.save()
                addNewProfile = Profile.objects.create(user=addNewUser, role="deliverydriver", accessStat=True)
                addNewProfile.save()
                return redirect('settings')



            elif 'deleteolddriver' in request.POST:
                delDriverName = request.POST['deldrivername']

                getUser = User.objects.get(username=delDriverName)
                getDriverProf = Profile.objects.get(user=getUser, role="deliverydriver")
                getUser.delete()
                getDriverProf.delete()
                return redirect('settings')



            elif 'createnewsub' in request.POST:
                newSubName = request.POST['createnewsubname']

                createSub = SubDistributors.objects.create(name=newSubName)
                createSub.save()
                return redirect('settings')


            elif 'deleteoldsub' in request.POST:
                oldSubName = request.POST['deleteoldsubname']

                oldSubDelete = SubDistributors.objects.filter(name=oldSubName)
                oldSubDelete.delete()
                return redirect('settings')



            elif 'shuteveryoneout' in request.POST:
                trueAccessProfiles = Profile.objects.filter(role="shopattendant", accessStat=True)
                ddTrueAccessProfiles = Profile.objects.filter(role="deliverydriver", accessStat=True)

                trueAccessProfiles.update(accessStat=False)
                ddTrueAccessProfiles.update(accessStat=False)
                return redirect('settings')



                
            else:
                # return redirect("login")
                return render(request, 'audit/settings.html', {'companies': companies})

        else:
            return redirect('login')
    else:
        return redirect('login')


    

def deliveryShop(request):

    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
            return redirect('delivery')

        else:    
            companies = Company.objects.all()
            products = Products.objects.all()


            if request.method == "POST":
                if 'deliveryrecordouting' in request.POST:
                    pTaken = {}
                    nameOfDriver = request.POST["drivername"]
                    validate = ShopDeliveryRecord.objects.filter(deliveryStatus="delivering")
                    if validate.first():
                        pass
                    else:
                        i = 0
                        for x in request.POST:
                            i += 1
                            if i >= 4:
                                product = Products.objects.get(name=x)
                                pTaken[x] = {"product": x, "productQuantity": request.POST[x], "productPrice": product.wholesalePrice}
                        deliveryShopRecord = ShopDeliveryRecord.objects.create(driverName=nameOfDriver, productData=pTaken)
                        deliveryShopRecord.save()

                        return redirect('deliveryshop')
                        


                elif 'goodsbroughtback' in request.POST:

                    goodsBb = ShopDeliveryRecord.objects.filter(amountBroughtBack=0.0)

                    for x in goodsBb:
                        product = x.productData
                        for b in request.POST:
                            if b in product:
                                pBb = {"productBroughtBack": request.POST[b]}
                                product[b].update(pBb)
                                goodsBb.update(productData=product)

                    return redirect('deliveryshop')
                        

                elif 'amountbroughtback' in request.POST:
                    k = 0
                    for z in request.POST:
                        k += 1
                        if k >= 2:
                            amtBb = ShopDeliveryRecord.objects.filter(amountBroughtBack=0.0)
                            latestRec = ShopDeliveryRecord.objects.all()
                            lrv = latestRec.latest("deliveryNumber")


                            for item in amtBb:
                                if lrv:
                                    item.deliveryNumber = float(lrv.deliveryNumber) + 1
                                else:
                                    item.deliveryNumber = 1
                                item.deliveryStatus = "delivered"
                                item.amountBroughtBack = request.POST[z]
                                item.save()

                    return redirect('index')

                            # currentShopRecord = ShopDeliveryRecord.objects.all()
                            # slist = []
                            # for n in currentShopRecord:
                            #     slist.append(n)   
                            # ShopDeliveryRecordHistory.objects.bulk_create(slist)
                            # currentShopRecord.delete()
                else:
                    return redirect('index')

            return render(request, 'audit/delivery-shop.html', {"products": products, "companies": companies})

    
    else:
        return redirect('login')


    

def delivery(request):


    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        if Profile.objects.filter(user=request.user, role="shopattendant").exists():
            return redirect('login')
        else:    
            companies = Company.objects.all()
            products = Products.objects.all()
            tds = TodayDeliveryStartRecord.objects.all()
            tdsls = TodayDeliverySalesRecord.objects.all()

            for x in tds:
                if x.productsData == {}:
                    x.delete()
            for y in tdsls:
                if y.allCustomerData == {}:
                    y.delete()


            if "deliverygoodsrecieved" in request.POST:
                activeRecord = ActiveDeliveryStartRecord.objects.all()
                randVal = random.uniform(1, 100000)

                if activeRecord.first():
                    pass
                else: 
                    i = 0
                    for m in request.POST:
                        i += 1
                        if i >= 3:
                            product = Products.objects.get(name=m)
                            productTaken = ActiveDeliveryStartRecord.objects.create(salesId=randVal, productTaken=product, productTakenQuantity=request.POST[m])
                            productTaken.save()

                todayaudit = TodayAudit.objects.all()
                if todayaudit.first():
                    tdfirst = todayaudit.first()
                    if tdfirst.driverStatus == "Driver has closed":
                        todayaudit.delete()
                    else:
                        pass

                else:
                    pass

                return redirect('delivery')

            if "deliverycustomername" in request.POST:
                prodDetails = {}
                slsId = ActiveDeliveryStartRecord.objects.first()

                i = 0
                for d in request.POST:
                    i += 1
                    if i >= 2:
                        if Products.objects.filter(name=d).exists():
                            prodDetails[d] = request.POST[d]


                if request.POST['modeofpayment'] == 'Cash':  
                    crte = ActiveDeliverySalesRecord.objects.create(salesId=slsId.salesId, deliveryCustName=request.POST['deliverycustomername'], deliveryProductData=prodDetails, productValue=request.POST['productvalue'], modeOfPayment=request.POST['modeofpayment'], amtFromCustomer=request.POST['amtfromcustomer'], customerDebt=request.POST['customerdebt'], customerCredit=request.POST['customercredit'])
                    crte.save()

                elif request.POST['modeofpayment'] == 'Transfer':
                    crte = ActiveDeliverySalesRecord.objects.create(salesId=slsId.salesId, deliveryCustName=request.POST['deliverycustomername'], deliveryProductData=prodDetails, productValue=request.POST['productvalue'], modeOfPayment=request.POST['modeofpayment'])
                    crte.save()

                return redirect('delivery')
                        

            if "deliverygoodsreturned" in request.POST:
                i = 0
                for n in request.POST:
                    i += 1
                    if i >= 3:
                        product = Products.objects.get(name=n)
                        producVali = ActiveDeliveryStartRecord.objects.filter(productTaken=product)
                        producVali.update(productQuantityBroughtBack=request.POST[n])

                return redirect('delivery')

            if "deliveryamountbroughtback" in request.POST:
                salesIdLst = []
                productDt = {}
                customerMainDt = {}
                customerDt = {}
                tdstart = TodayDeliveryStartRecord.objects.all()
                if tdstart.first():
                    n = tdstart.latest('deliveryNumber')
                    l = n.deliveryNumber
                    l += 1
                else:
                    l = 1


                i = 0
                for x in request.POST:
                    i += 1
                    if i >= 2:
                        val = ActiveDeliveryStartRecord.objects.all()
                        val.update(amountBroughtBack=request.POST[x])
                        valSales = ActiveDeliverySalesRecord.objects.all()
                        vlList = []
                        vlsList = []
                        for x in val:
                            salesIdLst.append(x.salesId)
                            productDt[x.productTaken.name] = {"productTakenQuantity": x.productTakenQuantity, "productBroughtBackQuantity": x.productQuantityBroughtBack}

                        
                        
                        salesIdSet = set(salesIdLst)
                        dd = ""
                        pp = list(salesIdSet)
                        for x in pp:
                            dd += str(x)
                        salesIdFlt = float(dd)
                        
                        tdstartrecord = TodayDeliveryStartRecord.objects.create(deliveryNumber=l, salesId=salesIdFlt, productsData=productDt, amountBroughtBack=request.POST["deliveryamountbroughtback"]) 
                        tdstartrecord.save() 

                

                        for y in valSales:
                            customerDt["productsPurchased"] = y.deliveryProductData
                            customerMainDt[y.deliveryCustName] = {"productsPurchased": y.deliveryProductData, "productValue": y.productValue, "modeOfPayment": y.modeOfPayment, "amtFromCustomer": y.amtFromCustomer, "customerDebt": y.customerDebt, "customerCredit": y.customerCredit}
                        
                        tdSalesRecord = TodayDeliverySalesRecord.objects.create(deliveryNumber=l, salesId=salesIdFlt, allCustomerData=customerMainDt)
                        tdSalesRecord.save()

                        val.delete()
                        valSales.delete()

                return redirect('delivery')

                        

            if "closedelivery" in request.POST:
                allDeliverySales = {}
                audtMessages = {}
                deliveryCustomersToTransfer = {}
                tdStRecord = TodayDeliveryStartRecord.objects.all()
                tdSalesRecord = TodayDeliverySalesRecord.objects.all()
                
                for a in tdStRecord:
                    delNub = int(a.deliveryNumber)
                    offDelNumber = f"delivery {delNub}"
                    productsData = a.productsData
                    amountBback = float(a.amountBroughtBack)
                    finishedSellingAt = str(a.finishedAt)

                    tdsalesRec = TodayDeliverySalesRecord.objects.filter(deliveryNumber=delNub)


                    if tdsalesRec:

                        for b in tdsalesRec:
                            allCdata = b.allCustomerData

                        allDeliverySales[offDelNumber] = {"productsData": productsData, "amountBroughtBack": amountBback, "allCustomersData": allCdata, "finishedSellingTime": finishedSellingAt}

                    else:
                        mgggs = messages.objects.create(message_type="Error", message_content=f"{offDelNumber}'s sales data was not recorded")
                        mgggs.save()


                expMessages = {}

                for l in tdStRecord:
                    totProductsTaken = {}
                    # for m in l.productsData:
                    #     print(l.productsData[m]["productTakenQuantity"])
                    for j in l.productsData:
                       
                        # totProductsTaken[j] = float(l.productsData[j]['productTakenQuantity'])
                        totProductsTaken[j] = float(l.productsData[j]['productTakenQuantity'])

                    
                    tdSalSrecord = TodayDeliverySalesRecord.objects.filter(salesId=l.salesId)
                    for k in tdSalSrecord:
                        for m in k.allCustomerData:
                            for n in k.allCustomerData[m]["productsPurchased"]:
                                if n in totProductsTaken:
                                    totProductsTaken[n] -= float(k.allCustomerData[m]["productsPurchased"][n])
                    
                    
                    expMessages[f"Expected Products returned for delivery {l.deliveryNumber}"] = totProductsTaken



                #based on product taken and products brought back
                totalDeliveryAmountExpected = 0
                #based on cash sales
                realDeliveryAmountExpected = 0
                #based on all sales
                fullDeliveryAmountExpected = 0
                for d in tdStRecord:
                    dAmtExp = 0
                    for e in d.productsData:
                        vlProduct = Products.objects.get(name=e)
                        dAmtExp += ((float(d.productsData[e]["productTakenQuantity"]) - float(d.productsData[e]["productBroughtBackQuantity"])) * float(vlProduct.wholesalePrice))

                    totalDeliveryAmountExpected += dAmtExp
                    audtMessages[f"Amount Returned from delivery {d.deliveryNumber}"] = float(d.amountBroughtBack)

                    if float(d.amountBroughtBack) != float(dAmtExp):
                        audtMessages[f"Error in delivery {d.deliveryNumber}"] = f"Amount brought back: #{d.amountBroughtBack} and amount expected: #{dAmtExp} do not match"
                        mgsgs = messages.objects.create(message_type="Error", message_content=f"Delivery amount brought back: #{d.amountBroughtBack} and amount expected: #{dAmtExp} do not match") 
                        mgsgs.save()

                    else:
                        audtMessages[f"Info on delivery {d.deliveryNumber}"] = f"Successfully passed audit"


                for p in tdSalesRecord:
                    for q in p.allCustomerData:
                        fullDeliveryAmountExpected += float(p.allCustomerData[q]["productValue"])
                        
                        if p.allCustomerData[q]["modeOfPayment"] == "Cash":
                            realDeliveryAmountExpected += float(p.allCustomerData[q]["productValue"])




                for g in tdSalesRecord:
                    for h in g.allCustomerData:
                        if str(g.allCustomerData[h]["modeOfPayment"]) == "Transfer":
                            deliveryCustomersToTransfer[h] = f"#{g.allCustomerData[h]['productValue']} from #{g.allCustomerData[h]['productValue']}"



                driver = str(request.user.username)
                driverStat = "Driver has closed"
                driverDeliveryStockDetails = allDeliverySales
                expectedDriverDeliveryStockDetails = expMessages
                deliveryCToTransfer = deliveryCustomersToTransfer
                fullDeliverySalesAudit = {
                    "auditMessages": audtMessages,
                    "totalAmountExpectedBasedOnRecord": totalDeliveryAmountExpected,
                    "actualAmountExpectedBasedOnCashSales": realDeliveryAmountExpected,
                    "actualAmountExpectedFromAllSales": fullDeliveryAmountExpected 
                }

                shopTodAudit = TodayAudit.objects.all()

                if shopTodAudit.first():
                    shopTodAudit.update(
                        driver=driver,
                        driverStatus=driverStat,
                        driverDeliveryStockDetails=driverDeliveryStockDetails,
                        expectedDriverDeliveryStockDetails=expectedDriverDeliveryStockDetails,
                        deliveryCustomersToTransfer=deliveryCToTransfer,
                        fullDeliverySalesAudit=fullDeliverySalesAudit
                    )
                else:
                    todayAuditCreate = TodayAudit.objects.create(
                        driver=driver,
                        driverStatus=driverStat,
                        driverDeliveryStockDetails=driverDeliveryStockDetails,
                        expectedDriverDeliveryStockDetails=expectedDriverDeliveryStockDetails,
                        deliveryCustomersToTransfer=deliveryCToTransfer,
                        fullDeliverySalesAudit=fullDeliverySalesAudit
                    )

                    todayAuditCreate.save()

                # bulkCrteLst = []
                # print("-------")
                # for s in shopTodAudit:
                #     print(s)
                #     if s.driverStatus == "Driver has closed":
                #         print("Dyes")
                #         if s.shopAttendantStatus == "Shop Attendant has closed":
                #             print("Syes")
                #             bulkCrteLst.append(s)
                #             TodayAudit.objects.bulk_create(bulkCrteLst)

                # print(bulkCrteLst)

                for s in shopTodAudit:
                    if s.driverStatus == "Driver has closed":
                        if s.shopAttendantStatus == "Shop Attendant has closed":
                            recordTotalAudit = TotalAudit.objects.create(
                                totalAuditId=s.totalAuditId,
                                driver=s.driver,
                                shopAttendant=s.shopAttendant,
                                driverStatus=s.driverStatus,
                                shopAttendantStatus=s.shopAttendantStatus,
                                openingStock=s.openingStock,
                                newStock=s.newStock,
                                closingStock=s.closingStock,
                                driverDeliveryStockDetails=s.driverDeliveryStockDetails,
                                shopAttendantDeliveryStockDetails=s.shopAttendantDeliveryStockDetails,
                                expectedDriverDeliveryStockDetails=s.expectedDriverDeliveryStockDetails,
                                expectedShopAttendantDeliveryStockDetails=s.expectedShopAttendantDeliveryStockDetails,
                                deliveryCustomersToTransfer=s.deliveryCustomersToTransfer,
                                invoiceNumbers=s.invoiceNumbers,
                                allSubSales=s.allSubSales,
                                allWholesales=s.allWholesales,
                                allRetailSales=s.allRetailSales,
                                shopCustomersToTransfer=s.shopCustomersToTransfer,
                                shopHandover=s.shopHandover,
                                TotalDeliveryHandover=s.TotalDeliveryHandover,
                                fullShopSalesAudit=s.fullShopSalesAudit,
                                fullDeliverySalesAudit=s.fullDeliverySalesAudit,
                                customersInDebt=s.customersInDebt,
                                customersCredit=s.customersCredit,
                                messages=s.messages,
                            )

                            recordTotalAudit.save()


                getTdAudit = TodayAudit.objects.all()
                gettAudit = getTdAudit.first()

                if gettAudit.driverStatus == "Driver has closed" and gettAudit.shopAttendantStatus == "Shop Attendant has closed":
                    opensh = OpeningStockHistory.objects.all()                
                    topens = TodayOpeningStock.objects.all()  
                    tnews = TodayNewStock.objects.all()             
                    newsh = NewStockHistory.objects.all()             
                    tclosings = TodayClosingStock.objects.all()             
                    csh = ClosingStockHistory.objects.all()             
                    wr = WholesaleRecord.objects.all()             
                    rr = RetailRecord.objects.all()             
                    sr = SubRecord.objects.all()             
                    sdr = ShopDeliveryRecord.objects.all()             
                    adstr = ActiveDeliveryStartRecord.objects.all()             
                    adsar = ActiveDeliverySalesRecord.objects.all()             
                    tdstr = TodayDeliveryStartRecord.objects.all()             
                    tdsar = TodayDeliverySalesRecord.objects.all()             
                    tdaid = todayTauditId.objects.all()     
                    tinvn = TodayInvoiceNumber.objects.all()             
                    mgs = messages.objects.all()             
                    rmt = Remmittance.objects.all()             

                    opensh.delete()       
                    topens.delete()       
                    tnews.delete()       
                    newsh.delete()       
                    tclosings.delete()       
                    csh.delete()       
                    wr.delete()       
                    rr.delete()       
                    sr.delete()       
                    sdr.delete()       
                    adstr.delete()       
                    adsar.delete()       
                    tdstr.delete()       
                    tdsar.delete()       
                    tdaid.delete()       
                    tinvn.delete()       
                    mgs.delete()       
                    rmt.delete() 

                else:
                    pass

                profchange = Profile.objects.filter(user=request.user, role="deliverydriver", accessStat=True)
                if profchange:
                    profchange.update(accessStat=False)

                auth.logout(request)
                return redirect('login')                  

            return render(request, 'audit/delivery.html', {"products": products, "companies": companies})

    else:
        return redirect('login')


    

def invoice(request):


    if str(request.user) == "AnonymousUser":
        return redirect('login')

    elif Profile.objects.filter(user=request.user, accessStat=True).exists():    

        companies = Company.objects.all()
        if request.method == "POST":
            invoiceData = request.POST
            invoiceImg = request.FILES.get("invoiceimage")

            tIn = TodayInvoiceNumber.objects.create(invoiceNumber=invoiceData['invoicenumber'])
            tIn.save()
        
            companyValidate = Company.objects.get(name=invoiceData['company'])
            registerInvoice = Invoice.objects.create(company=companyValidate, invoiceNumber=invoiceData['invoicenumber'], invoiceImage=invoiceImg)
            registerInvoice.save()

            return redirect('index')

        return render(request, 'audit/invoice.html', {"companies": companies})
    
    else:
        return redirect('login')



def showerror(request):
    return render(request, 'audit/error.html')
    


def register(request):


    # if str(request.user) == "AnonymousUser":
    #     return redirect('login')

    if Profile.objects.filter(user=request.user, role="deliverydriver").exists():
        return redirect('login')

    elif Profile.objects.filter(user=request.user, role="shopattendant").exists():    
        return redirect('login')
    
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                messages.info(request, "This name already exists")
                return redirect('register')
            elif User.objects.filter(password=password).exists():
                messages.info(request, "This password is in use")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                validateUser = User.objects.get(username=username)
                newProfile = Profile.objects.create(user=validateUser, role="admin", accessStat=True)
                newProfile.save()
                return redirect('login')

        return render(request, 'audit/register.html')


