# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 06:34:44 2021

@author: Pavithra
"""

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import datetime
from datetime import date, timedelta
import time
import sklearn
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
  




st.markdown("<h1 style='text-align: center, color: purple'>The Agro Farm - Farmer's Guide</h1>", unsafe_allow_html=True)

#predicting future price




option = webdriver.ChromeOptions()
option.add_argument('headless')
driver=webdriver.Chrome("chromedriver.exe")






st.header('Market Price Prediction')

st.write("Wholesale prices of commodity in different Southern Zones")

with st.spinner("Fetching data.."):
    optioncmp = st.selectbox('Choose the Commodity of which you want to predict the price :',
    ('Rice','Wheat','Atta (Wheat)','Gram Dal','Tur/Arhar Dal','Urad Dal','Moong Dal','Masoor Dal','Groundnut Oil (Packed)','Musturd Oil (Packed)','Vanaspati (Packed)','Soya Oil (Packed)','Palm Oil (Packed)','Potato','Onion','Tomato','Sugar','Gur','Milk @','Tea Loose','Salt Pack (Iodised)'))
    

with st.spinner("Fetching data.."):
    optionzone = st.selectbox('Choose the Southern Zone/ Location:',
    ('CHENNAI','DINDUGAL','THIRUCHIRAPALLI','COIMBATORE','TIRUNELVELI','CUDDALORE','DHARMAPURI','VELLORE','RAMANATHAPURAM'))
    


if(optionzone=='CHENNAI'):
    zonenum = 170
elif(optionzone == 'PUDUCHERRY'):
    zonenum = 169
    
elif(optionzone=='DINDUGAL'):
    zonenum=171
    
elif(optionzone=='THIRUCHIRAPALLI'):
    zonenum = 172
    
elif(optionzone=='COIMBATORE'):
    zonenum = 173
    
elif(optionzone =='TIRUNELVELI'):
    zonenum = 174
    
elif(optionzone =='CUDDALORE'):
    zonenum = 175
    
    
elif(optionzone =='DHARMAPURI'):
    zonenum=176
    
elif(optionzone=='VELLORE'):
    zonenum = 177
    
else:
    zonenum = 178
    
    
if(st.button('Predict')):
    
    driver.get("https://fcainfoweb.nic.in/Reports/Report_Menu_Web.aspx")
    reporttype=driver.find_element(By.ID,"ctl00_MainContent_Ddl_Rpt_type")
    reporttyper = Select(reporttype)

    reporttyper.select_by_value("Wholesale")

    typeofrep=driver.find_element(By.ID,"ctl00_MainContent_Rbl_Rpt_type_1")
    typeofrep.click()


    daily=driver.find_element(By.ID,"ctl00_MainContent_Ddl_Rpt_Option1")
    dailyd = Select(daily)

    dailyd.select_by_value("Daily Variation")

    todaydate = date.today()
    todayd = todaydate.strftime("%d/%m/%y")

    frmdate = todaydate - timedelta(days=40)
    frmdatd = frmdate.strftime("%d/%m/%y")

    todayd = todaydate - timedelta(days=1)
    todaydd = todayd.strftime("%d/%m/%y")
    
    ####FOR PRINTING####
    
    
    tomorrow = todaydate + timedelta(days=1)
    tomorrowd = tomorrow.strftime("%d/%m/%y")
    
    
    tomorrow1 = todaydate + timedelta(days=2)
    tomorrowd1 = tomorrow1.strftime("%d/%m/%y")
    
    
    tomorrow2 = todaydate + timedelta(days=3)
    tomorrowd2 = tomorrow2.strftime("%d/%m/%y")
    
    
    tomorrow3 = todaydate + timedelta(days=4)
    tomorrowd3 = tomorrow3.strftime("%d/%m/%y")
    
    
    fromdate = driver.find_element(By.ID,"ctl00_MainContent_Txt_FrmDate")
    fromdate.send_keys(frmdatd)

    todate = driver.find_element(By.ID,"ctl00_MainContent_Txt_ToDate")
    todate.send_keys(todaydd)

    
    commodity = driver.find_element(By.ID,"ctl00_MainContent_Lst_Commodity")

    commodityd = Select(commodity)
    commodityd.select_by_value(optioncmp)
    
    with st.spinner("Evaluating, Please wait.."):
    
        getdata = driver.find_element(By.XPATH,".//*[@id='ctl00_MainContent_btn_getdata1']").click()

        time.sleep(5)
       

        pricelist = []
        for i in range(2,30):
    
            val = driver.find_element(By.XPATH,".//*[@id='gv0']/tbody/tr["+str(zonenum)+"]/td["+str(i)+"]")
            print(val.accessible_name)
            if(val.accessible_name=="NR" or val.accessible_name==" "):
                pricelist.append(0)
            else:
                pricelist.append(int(val.accessible_name))
    

        for i in range(len(pricelist)):
            if(pricelist[i]==0):
                pricelist[i]=sum(pricelist)/len(pricelist)
        
        
        
        print(pricelist)
        print("Current price of the stock is :",pricelist[len(pricelist)-1])

        datel = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        datelist = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]).reshape(-1,1)
        pricelistarr = np.array(pricelist)


        model = LinearRegression()
        model.fit(datelist,pricelistarr)


        r_sq = model.score(datelist,pricelistarr)
        print("coesfficient of determination :",r_sq)


        predictfuture = model.predict([[29],[30],[31],[32]])
        
        listprice = []
        listprice.append(predictfuture[0])
        listprice.append(predictfuture[1])
        listprice.append(predictfuture[2])
        listprice.append(predictfuture[3])
        numlist  = [1,2,3,4]
        
        st.write('Predicted price on '+str(tomorrowd)+' is approximately : ₹', predictfuture[0], '/ Quintal')
        
        st.write('Predicted price on '+str(tomorrowd1)+' is approximately : ₹', predictfuture[1], '/ Quintal')
        
        st.write('Predicted price on '+str(tomorrowd2)+' is approximately : ₹', predictfuture[2], '/ Quintal')
        
        st.write('Predicted price on '+str(tomorrowd3)+' is approximately : ₹', predictfuture[3], '/ Quintal')
     
        # define data values
        x = np.array([1,2,3,4]) # X-axis points
        y = np.array([predictfuture[0],predictfuture[1],predictfuture[2],predictfuture[3]])  # Y-axis points
  
        df = pd.DataFrame({
            'date': datel,
            'Price Trend': pricelist
            })

        df = df.rename(columns={'date':'index'}).set_index('index')
        st.line_chart(df)
        
        
        
st.header('Average per Month End Report')

st.write('Get Zonewise commodity average price')


optionzone = st.selectbox('Choose the Zone of which you want to know the average price:',
    ('NORTH ZONE','WEST ZONE','EAST ZONE','NORTH-EAST ZONE','SOUTH ZONE'))


date_avg=st.date_input('Select the Date :')

crcteddate_avg = date_avg.strftime("%d/%m/%y")


if(st.button('Get Average Month end report')):

    
    
    driver.get("https://fcainfoweb.nic.in/Reports/Report_Menu_Web.aspx")
    reporttype=driver.find_element(By.ID,"ctl00_MainContent_Ddl_Rpt_type")
    reporttyper = Select(reporttype)

    reporttyper.select_by_value("Wholesale")
    
    
    typeofrep=driver.find_element(By.ID,"ctl00_MainContent_Rbl_Rpt_type_2")
    typeofrep.click()
    
    
    zonewiseselect = driver.find_element(By.ID,"ctl00_MainContent_Ddl_Rpt_Option2")
    zonewiseselectd = Select(zonewiseselect)
    
    zonewiseselectd.select_by_value("Zonewise Average")
    
    
    
    
    
    whichzoneselect = driver.find_element(By.ID,"ctl00_MainContent_Lst_Zone")
    whichzoneselected = Select(whichzoneselect)
    
    
    whichzoneselected.select_by_value(optionzone)
    
    selectdate = driver.find_element(By.ID,"ctl00_MainContent_Txt_FrmDate")
    
    selectdate.send_keys(crcteddate_avg)
    
    
    with st.spinner("Evaluating..Please Wait"):
        get_avg = driver.find_element(By.XPATH,".//*[@id='ctl00_MainContent_btn_getdata1']").click()
        time.sleep(3)
        
        
        
        averageprice_commodity = []
        commodity = []
        
        for i in range(2,24):
            val1 = driver.find_element(By.XPATH,".//*[@id='Panel1']/table[3]/tbody/tr["+str(i)+"]/td[2]")
           
            val2 = driver.find_element(By.XPATH,".//*[@id='Panel1']/table[3]/tbody/tr["+str(i)+"]/td[1]")
            
            st.write((val2.accessible_name)+": "+ "₹" +val1.accessible_name +"/ Quintal")
            
            
  
    
  
    
        
st.header('Retail Price Prediction')

st.write('Southern Zones Retial Price forecast')
    





with st.spinner("Fetching data.."):
    optioncmp1 = st.selectbox('Choose the Commodity of which you want to predict the Retail price :',
    ('Rice','Wheat','Atta (Wheat)','Gram Dal','Tur/Arhar Dal','Urad Dal','Moong Dal','Masoor Dal','Groundnut Oil (Packed)','Musturd Oil (Packed)','Vanaspati (Packed)','Soya Oil (Packed)','Palm Oil (Packed)','Potato','Onion','Tomato','Sugar','Gur','Milk @','Tea Loose','Salt Pack (Iodised)'))
    

with st.spinner("Fetching data.."):
    optionzone1 = st.selectbox('Choose the Southern Zone:',
    ('CHENNAI','DINDUGAL','THIRUCHIRAPALLI','COIMBATORE','TIRUNELVELI','CUDDALORE','DHARMAPURI','VELLORE','RAMANATHAPURAM'))
    


if(optionzone1=='CHENNAI'):
    zonenum = 170
elif(optionzone1 == 'PUDUCHERRY'):
    zonenum = 169
    
elif(optionzone1=='DINDUGAL'):
    zonenum=171
    
elif(optionzone1=='THIRUCHIRAPALLI'):
    zonenum = 172
    
elif(optionzone1=='COIMBATORE'):
    zonenum = 173
    
elif(optionzone1 =='TIRUNELVELI'):
    zonenum = 174
    
elif(optionzone1 =='CUDDALORE'):
    zonenum = 175
    
    
elif(optionzone1 =='DHARMAPURI'):
    zonenum=176
    
elif(optionzone1=='VELLORE'):
    zonenum = 177
    
else:
    zonenum = 178
    
    
    
if(st.button('Predict Retail Price')):
    
    driver.get("https://fcainfoweb.nic.in/Reports/Report_Menu_Web.aspx")
    reporttype=driver.find_element(By.ID,"ctl00_MainContent_Ddl_Rpt_type")
    reporttyper = Select(reporttype)

    reporttyper.select_by_value("Retail")

    typeofrep=driver.find_element(By.ID,"ctl00_MainContent_Rbl_Rpt_type_1")
    typeofrep.click()


    daily=driver.find_element(By.ID,"ctl00_MainContent_Ddl_Rpt_Option1")
    dailyd = Select(daily)

    dailyd.select_by_value("Daily Variation")

    todaydate = date.today()
    todayd = todaydate.strftime("%d/%m/%y")

    frmdate = todaydate - timedelta(days=40)
    frmdatd = frmdate.strftime("%d/%m/%y")

    todayd = todaydate - timedelta(days=1)
    todaydd = todayd.strftime("%d/%m/%y")
    
    ####FOR PRINTING####
    
    
    tomorrow = todaydate + timedelta(days=1)
    tomorrowd = tomorrow.strftime("%d/%m/%y")
    
    
    tomorrow1 = todaydate + timedelta(days=2)
    tomorrowd1 = tomorrow1.strftime("%d/%m/%y")
    
    
    tomorrow2 = todaydate + timedelta(days=3)
    tomorrowd2 = tomorrow2.strftime("%d/%m/%y")
    
    
    tomorrow3 = todaydate + timedelta(days=4)
    tomorrowd3 = tomorrow3.strftime("%d/%m/%y")
    
    
    fromdate = driver.find_element(By.ID,"ctl00_MainContent_Txt_FrmDate")
    fromdate.send_keys(frmdatd)

    todate = driver.find_element(By.ID,"ctl00_MainContent_Txt_ToDate")
    todate.send_keys(todaydd)

    
    commodity = driver.find_element(By.ID,"ctl00_MainContent_Lst_Commodity")

    commodityd = Select(commodity)
    commodityd.select_by_value(optioncmp1)
    
    with st.spinner("Evaluating, Please wait.."):
    
        getdataa = driver.find_element(By.XPATH,".//*[@id='ctl00_MainContent_btn_getdata1']").click()

        time.sleep(5)
       

        pricelist = []
        for i in range(2,42):
    
            val = driver.find_element(By.XPATH,".//*[@id='gv0']/tbody/tr["+str(zonenum)+"]/td["+str(i)+"]")
            print(val.accessible_name)
            if(val.accessible_name=="NR" or val.accessible_name==" "):
                pricelist.append(0)
            else:
                pricelist.append(int(val.accessible_name))
    

        for i in range(len(pricelist)):
            if(pricelist[i]==0):
                pricelist[i]=sum(pricelist)/len(pricelist)
        
        
        
        print(pricelist)
        st.write("Current price of the stock is :",pricelist[len(pricelist)-1])

        datel = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
        datelist = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]).reshape(-1,1)
        pricelistarr = np.array(pricelist)


        modelreg = LinearRegression()
        modelreg.fit(datelist,pricelistarr)


        r_sq = modelreg.score(datelist,pricelistarr)
        print("coesfficient of determination :",r_sq)


        predictfuture = modelreg.predict([[29],[30],[31],[32]])
        
        listprice = []
        listprice.append(predictfuture[0])
        listprice.append(predictfuture[1])
        listprice.append(predictfuture[2])
        listprice.append(predictfuture[3])
        numlist  = [1,2,3,4]
        
        st.write('Predicted price on '+str(tomorrowd)+' is approximately : ₹', predictfuture[0], '/ Kg')
        
        st.write('Predicted price on '+str(tomorrowd1)+' is approximately : ₹', predictfuture[1], '/ Kg')
        
        st.write('Predicted price on '+str(tomorrowd2)+' is approximately : ₹', predictfuture[2], '/ Kg')
        
        st.write('Predicted price on '+str(tomorrowd3)+' is approximately : ₹', predictfuture[3], '/ Kg')
     
        # define data values
        x = np.array([1,2,3,4]) # X-axis points
        y = np.array([predictfuture[0],predictfuture[1],predictfuture[2],predictfuture[3]])  # Y-axis points
  
        df = pd.DataFrame({
            'date': datel,
            'Price Trend': pricelist
            })

        df = df.rename(columns={'date':'index'}).set_index('index')
        st.line_chart(df)
        
        
            
            
            
            
        
            
       
    
    
    
    
    
    
    

    
    
    









        
        
        
        
        
        
        




    
    
    
    

    








