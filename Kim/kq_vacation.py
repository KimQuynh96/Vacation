from os import terminal_size, times
from time import sleep
from openpyxl import styles
import xlrd,openpyxl,os,selenium,datetime,json,re,xlsxwriter,time
from pathlib import Path
from datetime import datetime as dt
from os import path
from pathlib import Path
from warnings import filterwarnings
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.poolmanager import proxy_from_url
from selenium.webdriver.common.keys import Keys
from datetime import date
from kq_function_vacation import driver, data,infor,information_vacation,click_on_request_button,popup_time_card,msg_xlsx,is_Displayed1,msg,xpath3,scroll,scrolling_to_target,is_Displayed,total_data,xpath,xpath2
from dateutil.relativedelta import relativedelta
from kq_param_hr import submenu_my_vacation, time_card
from xlsxwriter import Workbook

param_excel_tc=json.loads(time_card())
param_excel=json.loads(submenu_my_vacation())
re_vc=param_excel["re_ad"]
detailex=param_excel["re_detail"]



def split_date_from_continuous_date(continuous_date,date_used):
   
    if continuous_date.rfind("~") > 0 :
        start_date=continuous_date[None: int(continuous_date.rfind("~"))]
        start_date = datetime.datetime.strptime(start_date , '%Y-%m-%d').date()
        end_date=continuous_date[int(continuous_date.rfind("~"))+1: None]
        end_date = datetime.datetime.strptime(end_date , '%Y-%m-%d').date()
        next_date_1=start_date
        while next_date_1 != end_date :
            date_used.append(str(next_date_1))
            if start_date == end_date :
                break
            next_date_1=next_date(next_date_1)
        date_used.append(str(end_date))
    else :
        date_used.append(continuous_date)

def choose_end_date(request_date,date_used):
    start_date=request_date
    if int(data["month"][str(request_date.month)]) == request_date.day:
        request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
    if request_date.weekday() == 5 :
        request_date= request_date + relativedelta(day=request_date.day +2)
        if int(data["month"][str(request_date.month)]) == request_date.day:
            request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
        
    if  request_date.weekday() == 6 :
        request_date= request_date + relativedelta(day=request_date.day +1)
        if int(data["month"][str(request_date.month)]) == request_date.day:
            request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
    
    if  start_date == request_date :
        request_date= request_date + relativedelta(day=request_date.day +1)
        if request_date.weekday() == 5 :
            request_date= request_date + relativedelta(day=request_date.day +2)
            if int(data["month"][str(request_date.month)]) == request_date.day:
                request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
            
        if  request_date.weekday() == 6 :
            request_date= request_date + relativedelta(day=request_date.day +1)
            if int(data["month"][str(request_date.month)]) == request_date.day:
                request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)

    end_date=request_date

    if str(end_date) not in date_used:
        return end_date
    else :
        return False

def choose_start_date(date_used,request_date):
    # < Find unused date , not saturday , not sunday , not holiday to use for request vacation > #
    if request_date.weekday() == 5 :
        request_date= request_date + relativedelta(day=request_date.day +2)
    if  request_date.weekday() == 6 :
        request_date= request_date + relativedelta(day=request_date.day +1)
    if str(request_date) in date_used  :
        request_date= request_date + relativedelta(day=request_date.day +1)
        if request_date.weekday() == 5 :
            request_date= request_date + relativedelta(day=request_date.day +2)
        if  request_date.weekday() == 6 :
            request_date= request_date + relativedelta(day=request_date.day +1)
        
        while str(request_date) in date_used  :
            if int(data["month"][str(request_date.month)]) == request_date.day:
                request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
            request_date= request_date + relativedelta(day=request_date.day +1)
            if request_date.weekday() == 5 :
                request_date= request_date + relativedelta(day=request_date.day +2)
                if int(data["month"][str(request_date.month)]) == request_date.day:
                    request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
                
            if  request_date.weekday() == 6 :
                request_date= request_date + relativedelta(day=request_date.day +1)
                if int(data["month"][str(request_date.month)]) == request_date.day:
                    request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
    return request_date

def next_date(request_date):
    if int(data["month"][str(request_date.month)]) == request_date.day:
        request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
    request_date= request_date + relativedelta(day=request_date.day +1)
    if request_date.weekday() == 5 :
        request_date= request_date + relativedelta(day=request_date.day +2)
        if int(data["month"][str(request_date.month)]) == request_date.day:
            request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
        
    if  request_date.weekday() == 6 :
        request_date= request_date + relativedelta(day=request_date.day +1)
        if int(data["month"][str(request_date.month)]) == request_date.day:
            request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
    return request_date

def select_days_to_request_leave_for_vacation_consecutive():
    i=1
    date_used=[]
    list_date=[]
    
    # < Go to my vacation to take used date > #
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.LINK_TEXT,"My Vacation Status"))).click()
    time.sleep(4)
    rows=driver.find_elements_by_xpath(data["rq_vc"]["list_request"])
    total_request=total_data(rows)
    while i<= total_request:
        if i == 1:
            if is_Displayed(data["rq_vc"]["check_list_re"]) == bool(True) :
               break
            else:
                date=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["request"])).text
                split_date_from_continuous_date(date,date_used)
        else:
            date=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["request"])).text
            split_date_from_continuous_date(date,date_used)
        i=i+1
    
    date= datetime.date.today() 
    start_date=choose_start_date(date_used,date)
    end_date= choose_end_date(start_date,date_used)
    if end_date == False:
        while end_date == False :
            end_date= choose_end_date(start_date,date_used)
            if end_date != False :
                list_date.append(start_date)
                list_date.append(end_date)
                break
            start_date=next_date(start_date)
    else:
        list_date.append(start_date)
        list_date.append(end_date)

    # < Select date from find for request vacation > #
    driver.find_element_by_link_text("Request Vacation").click()
    popup_time_card()
    for i in list_date:
        request_date=i
        current_month=driver.find_element_by_xpath(data["rq_vc"]["current_month"]).text[5:None] 
        if request_date !=  datetime.date.today() + relativedelta(month=request_date.month+1) + relativedelta(day=1) :
            if int(request_date.month) < 10 :
                request_month="0"+str(request_date.month)
            
            if current_month == request_month :
                result_click=click_date(request_date)
                if result_click== True:
                    msg("p","-Select vacation date <Pass> ")
                else:
                    msg("p","-Select vacation date <Fail> ")
                    
            else:
                driver.find_element_by_xpath(data["rq_vc"]["icon_next_month"]).click()
                result_click=click_date(request_date)
                if result_click== True:
                    msg("p","-Select vacation date <Pass> ")
                else:
                    msg("p","-Select vacation date <Fail> ")
                   
    return list_date

def select_days_to_request_leave():
    i=d=1
    date_used =[]
    
    # < Go to my vacation to take used days > #
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.LINK_TEXT,"My Vacation Status"))).click()
    time.sleep(4)
    rows=driver.find_elements_by_xpath(data["rq_vc"]["list_request"])
    total_request=total_data(rows)
    while i<= total_request:
        if i == 1:
            if is_Displayed(data["rq_vc"]["check_list_re"]) == bool(True) :
               break
            else:
                date=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["request"])).text
                split_date_from_continuous_date(date,date_used)
        else:
            date=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["request"])).text
            split_date_from_continuous_date(date,date_used)
        i=i+1
    
 
    # < Find unused days , not saturday , not sunday , not holiday to use for request vacation > #
    request_date= datetime.date.today() 
    if request_date.weekday() == 5 :
        request_date= request_date + relativedelta(day=request_date.day +2)
    if  request_date.weekday() == 6 :
        request_date= request_date + relativedelta(day=request_date.day +1)
    if str(request_date) in date_used  :
        request_date= request_date + relativedelta(day=request_date.day +1)
        if request_date.weekday() == 5 :
            request_date= request_date + relativedelta(day=request_date.day +2)
        if  request_date.weekday() == 6 :
            request_date= request_date + relativedelta(day=request_date.day +1)
        
        while str(request_date) in date_used  :
            if int(data["month"][str(request_date.month)]) == request_date.day:
                request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
            request_date= request_date + relativedelta(day=request_date.day +1)
            if request_date.weekday() == 5 :
                request_date= request_date + relativedelta(day=request_date.day +2)
                if int(data["month"][str(request_date.month)]) == request_date.day:
                    request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
                
            if  request_date.weekday() == 6 :
                request_date= request_date + relativedelta(day=request_date.day +1)
                if int(data["month"][str(request_date.month)]) == request_date.day:
                    request_date= request_date + relativedelta(month=request_date.month+1) + relativedelta(day=1)
               
               
  
    # < Select date from find for request vacation > #
    driver.find_element_by_link_text("Request Vacation").click()
    popup_time_card()
    current_month=driver.find_element_by_xpath(data["rq_vc"]["current_month"]).text[5:None] 
   
    if int(request_date.month) < 10 :
        request_month="0"+str(request_date.month)
       
    if current_month == request_month :
        result_click=click_date(request_date)
        if result_click== True:
            msg("p","-Select vacation date <Pass> ")
            return request_date
        else:
            msg("p","-Select vacation date <Fail> ")
            return False
            
    else:
        driver.find_element_by_xpath(data["rq_vc"]["icon_next_month"]).click()
        
        result_click=click_date(request_date)
       
        if result_click== True:
            msg("p","-Select vacation date <Pass> ")
            return request_date
        else:
            msg("p","-Select vacation date <Fail> ")
            return False
             
def click_date(request_date):
    
    if request_date.day < 25:
       
        for i in range(2,8) :
            for j in range(2,8):
                date_at_calendar=driver.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]/span")
                if str(date_at_calendar.text)==str(request_date.day):
                    date_at_calendar.click()
                    return True
        return False
    else:  
        for i in range(2,8) :
            for j in range(2,8):
                date_at_calendar=driver.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]/span")
                if str(date_at_calendar.text)==str(request_date.day):
                    date_at_calendar.click()
                    selected_date=driver.find_element_by_xpath(data["rq_vc"]["selected_date"]).text
                    if selected_date.rfind("[") > 0:
                        selected_date=selected_date[None: int(selected_date.rfind("["))].replace(" ", "")
                    else:
                        #selected_date=selected_date.replace(" ", "")
                        selected_date=selected_date[12: None].replace(" ", "")

                    if str(request_date)== selected_date:
                        return True
                    else:
                        date_at_calendar.click()
                        
        return False

def click_date_time_card(request_date):
    day=request_date.day
    for i in range(1,6) :
        for j in range(1,6):
            if i == 1 :
                date_to_click=driver.find_element_by_xpath(data["date_cu_tc"]+str(i)+"]/div["+str(j)+"]")
                date_at_calendar=date_to_click.text
                if day >25 and date_at_calendar == str(day) :
                    pass
                else:
                    if date_at_calendar == str(day):
                        date_to_click.click()
                        return True
            else:
                date_to_click=driver.find_element_by_xpath(data["date_cu_tc"]+str(i)+"]/div["+str(j)+"]")
                date_at_calendar=date_to_click.text
                if date_at_calendar == str(day):
                    date_to_click.click()
                    return True

def available_vacation():
   
    # < Get data of each vacation at available vacation table > #
    driver.find_element_by_link_text("Request Vacation").click()
    popup_time_card()
    i=1
    total_vacation=0
    all_vacation=[]
    tbody=driver.find_element_by_xpath(data["available_vacation"]["tbody"])
    rows=tbody.find_elements_by_tag_name("tr")
    total_vacation=total_data(rows)
    while i<= total_vacation:
        vacation={"total":"","used":"","remain":"","start":"","expiration":"","vacation_name":""}
        vacation_name=driver.find_element_by_xpath(data["rq_vc"]["tr"]+str(i)+"]/td[1]").text
        total_days=driver.find_element_by_xpath(data["rq_vc"]["tr"]+str(i)+"]/td[2]").text
        vacation["total"]=total_days
        used=driver.find_element_by_xpath(data["rq_vc"]["tr"]+str(i)+"]/td[3]").text 
        vacation["used"]=used
        remain=driver.find_element_by_xpath(data["rq_vc"]["tr"]+str(i)+"]/td[4]").text 
        vacation["remain"]=remain
        expiration_date=driver.find_element_by_xpath(data["rq_vc"]["tr"]+str(i)+"]/td[5]").text 
        vacation["expiration"]=expiration_date
        start_date=vacation_name[vacation_name.rfind("\n")+1:int(vacation_name.rfind("\n"))+11]
        vacation["start"]=start_date
        vacation_name_for_request=vacation_name[0:int(vacation_name.rfind("\n"))]+"["+vacation["start"]+" ~ "+vacation["expiration"] +"]"
        vacation["vacation_name"]=vacation_name_for_request
        all_vacation.append(vacation)
        i=i+1 
    return all_vacation

def total_vacation():
    
    # < Total vacation availabel of user > #
  
    i=1
    total_vacation_can_use=0
    time.sleep(3)
    tbody=driver.find_element_by_xpath(data["available_vacation"]["tbody"])
    rows=tbody.find_elements_by_tag_name("tr")
    total_vacation=total_data(rows)
    while i <= total_vacation:
        remain=driver.find_element_by_xpath(data["rq_vc"]["tr"]+str(i)+"]/td[4]").text 
        if str(remain.strip())!="0" :
            total_vacation_can_use +=1
        i=i+1
  
    return total_vacation_can_use

def hours_set_from_time_card(type_request):

    # < Specific working hours from time card  > #
    hour_use=driver.find_element_by_xpath(data["rq_vc"]["hour_use"]).text
    hour_use=hour_use[int(hour_use.rfind("Use:")): int(hour_use.rfind("] ["))]
    if type_request=="allday":
        if len(hour_use)==0:
            return 8
        else :
            return int(re.search(r'\d+',hour_use).group(0))
    elif type_request =="hour_unit":
        hour_use=driver.find_element_by_xpath(data["rq_vc"]["hour_use_h"]).text
        hour_use=hour_use[int(hour_use.rfind("Real Used:")+10): int(hour_use.rfind("H )"))]
        return int(re.search(r'\d+',hour_use).group(0)) 
       
    else:
        return 4  

def vacation_use_for_request():

    # < Information about number of selected vacation for request vacation > #
    vacation={"vacation_name":"","number_of_days":"","number_of_hours":""}
    
    vacation_name=driver.find_element_by_xpath(data["rq_vc"]["vacation_name"]).text

    vacation["vacation_name"]=vacation_name[None:int(vacation_name.rfind("("))-1] + vacation_name[int(vacation_name.rfind(")"))+2: None]
    days=vacation_name[int(vacation_name.rfind("(")+2) : int(vacation_name.rfind(")"))]
    if int(days.rfind("D")) >0 :
        vacation["number_of_days"]=vacation_name[int(vacation_name.rfind("("))+1: int(vacation_name.rfind("D"))]
        if int(days.rfind("H")) <0:
            vacation["number_of_hours"]="0"
        else:
            vacation["number_of_hours"]=vacation_name[int(vacation_name.rfind("D"))+1 : int(vacation_name.rfind("H"))]
    else:
        
        vacation["number_of_days"]="0"
        if int(days.rfind("H")) >0 :
            vacation["number_of_hours"]=vacation_name[int(vacation_name.rfind("("))+1: int(vacation_name.rfind("H"))]
        else:
            vacation["number_of_hours"]="0"
    if int(days.rfind("D")) <0 and int(days.rfind("H")) <0:
        vacation["number_of_days"]="0"
        vacation["number_of_hours"]="0"
    return vacation

def get_days_and_hour(data_column):
    # < Get days , hour of column data > /< 4.5D , 4D4H , - > #
    number_day={"day":"","hour":""}
    if data_column.replace(" ", "") =="-":
        number_day["day"]=float(0)
    elif data_column.rfind("D") < 0 :
        number_day["day"]=float(0)
    else :
        number_day["day"]=float( data_column[None : int(data_column.rfind("D"))])
        

    if data_column.rfind("H") < 0 :
        number_day["hour"]=float(0)
    else :
        number_day["hour"]=float(data_column[int(data_column.rfind("H")) -1: int(data_column.rfind("H"))])
    return number_day
       
def change_hour_to_day(tp1,tp2,oneday,plus,hour_use,use_hour_unit,type_request):

    # USE HOUR UNIT FOR REQUEST #
    # < The unit for calculation is hour ,convert to hour before calculation >#
    if use_hour_unit== True :
    
        # hour_use is int  ,ex hour_use=4 #
        # < Plus or minus data 2 column > #
        if tp2 !=" ":
            tp1=get_days_and_hour(tp1)
            tp2=get_days_and_hour(tp2)
            
            if plus=="plus":
                total_hour=int(tp1["hour"]) + int(tp2["hour"]) + int(tp1["day"]*oneday) + int(tp2["day"]*oneday)
                day=total_hour // oneday
                hour=total_hour % oneday
            
            if  plus=="minus":
                l1=int(tp1["day"])*oneday + int(tp1["hour"])
                l2=int(tp2["day"])*oneday + int(tp2["hour"])
                total_hour_remain=l1-l2
                if total_hour_remain < 0:
                    total_hour_remain=total_hour_remain*(-1)
                day=total_hour_remain // oneday
                hour=total_hour_remain % oneday
            
            if str(day)=="0" and str(hour)=="0":
                return "0"
            else:
                if str(day)=="0" :
                    return str(hour)+"H"
                if str(hour)=="0" :
                    return str(day)+"D"
        else:
        # < Plus or minus data of 1 column with number > #
            hour_use=int(hour_use)
            tp1=get_days_and_hour(tp1)
            if plus=="plus":
                if type_request == "half_day" or type_request == "hour_unit" :
                    hour_use=4
                    total_hour=int(tp1["hour"])  + int(tp1["day"]*oneday) + hour_use
                else:
                    total_hour=int(tp1["hour"])  + int(tp1["day"]*oneday) + hour_use*oneday
                day=total_hour // oneday
                hour=total_hour % oneday
            
            if  plus=="minus":
                l1=int(tp1["day"])*oneday + int(tp1["hour"])
                if type_request == "half_day" or type_request == "hour_unit" :
                    hour_use=4
                    total_hour_remain=l1 - hour_use
                   
                else:
                    total_hour_remain=l1 - int(hour_use)*oneday
              
                day=total_hour_remain // oneday
                hour=total_hour_remain % oneday

        
            
            if str(day)=="0" and str(hour)=="0":
                return "0"
            else:
                 
                if str(day)=="0" :
                    return str(hour)+"H"
                elif str(hour)=="0" :
                    return str(day)+"D"
                else:
                    return str(day)+"D " + str(hour)+"H"
    else:
        # NOT USE HOUR UNIT FOR REQUEST #
        # < The unit for calculation is days ,convert to days before calculation > #
        # < Hour user have to convert to day > #
        
        if tp2 !=" ":
            tp1=get_days_and_hour(tp1)
            tp2=get_days_and_hour(tp2)
           
            # DAY AFTER PLUS #
            #< Day after plus >#
            if plus=="plus":
                day=float(tp1["day"]) + float(tp2["day"])
            
            #< Day after minus >#
            if  plus=="minus":
                day=float(tp1["day"]) - float(tp2["day"])
                if day < 0:
                    day=day*(-1)
               
            if str(day)!="0" :
                if str(day)[int(str(day).rfind("."))+1: None] == "0":
                    return str(day)[None: int(str(day).rfind("."))]+"D"
            else:
                return "0"
        else:
            
            if type_request == "half_day" :
                hour_use=0.5
        # hour_use is fload  ,ex hour_use=0.5 #
        # < Plus or minus data of 1 column with number > #
            tp1=get_days_and_hour(tp1)
            if plus=="plus":
                day= float(tp1["day"]) + float(hour_use)
            
            if  plus=="minus":
                day= float(tp1["day"]) - float(hour_use)
                if day <0 :
                    day=day *(-1)
           
            if str(day)!="0.0" :      
                if str(day)[int(str(day).rfind("."))+1: None] == "0":
                    return str(day)[None: int(str(day).rfind("."))]+"D"
                else:
                    return str(day)+"D"
            else :
                return "0"
    
def select_user_from_depart():
    list_department=driver.find_elements_by_xpath(data["rq_vc"]["list_depart_cc"])    
    total_department=total_data(list_department)
    for i in range(1,total_department):
        time.sleep(1)
        depart_has_user=is_Displayed(data["rq_vc"]["single_depart"]+str(i)+data["rq_vc"]["single_depart1"]) 
        if depart_has_user == True :
            driver.find_element_by_xpath(data["rq_vc"]["single_depart"]+str(i)+data["rq_vc"]["single_depart1"]).click()
            total_user= driver.find_elements_by_xpath(data["rq_vc"]["list_user"])
            for i in range(1,len(total_user)+1):
                is_user=is_Displayed(data["rq_vc"]["sl_user"]+str(i)+data["rq_vc"]["sl_user1"]) 
                if is_user == True:
                    selected_cc_name=driver.find_element_by_xpath(data["rq_vc"]["user_name_cc"]+str(i)+data["rq_vc"]["user_name_cc1"]).text
                    driver.find_element_by_xpath(data["rq_vc"]["bt_cc_cc1"]+str(i)+data["rq_vc"]["bt_cc_cc2"]).click()
                    return selected_cc_name      
    return False              

def check_number_of_days_off(before,after,hour_use,vc_name,oneday,use_hour_unit,type_request):
   
    # < Check number of days before request > #
    numberex=param_excel["number"]
    total=True
    used=True
    remain=True
    msg("p","-[Available Vacation]")
    for vacation in before:
        if vacation["vacation_name"] == vc_name :
            vc_bf_use=vacation
            infor_before=infor(vc_bf_use,"Info Vacation before request",hour_use)
            days=change_hour_to_day(vc_bf_use["used"],vc_bf_use["remain"],oneday,"plus",hour_use,use_hour_unit,type_request)
           
            if vc_bf_use["total"]== days:
                msg_xlsx("p","fu",numberex,"  +Before Request Vacation : correct figures <Pass>")
            else:
                msg_xlsx("f","fu",numberex,"  +Before Request Vacation : correct figures <Fail>")
            break

    # < Check number of days after request > #
    for vacation in after: 
        if vacation["vacation_name"] == vc_name :
            vc_af_use=vacation
            infor_after=infor(vc_af_use,"Info Vacation after request",hour_use)
            if vc_af_use["total"] != vc_bf_use["total"] :
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : Total column <Fail>")
                total=False
            else:
                msg("p","  +After Request Vacation : Total column <Pass>")
        
           
            used_before_plus_used= change_hour_to_day(vc_bf_use["used"]," ",oneday,"plus",hour_use,use_hour_unit,type_request)
            if vc_af_use["used"] != used_before_plus_used:
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : Used column <Fail>")
                used=False
            else:
                msg("p","  +After Request Vacation : Used column <Pass>")

            remain_before_minus_used=change_hour_to_day(vc_bf_use["remain"]," ",oneday,"minus",hour_use,use_hour_unit,type_request)
            if vc_af_use["remain"] != remain_before_minus_used:
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : Remain column <Fail>")
                remain=False
            else:
                msg("p","  +After Request Vacation : Remain column <Pass>")
            
            if total== bool(True) and used== bool(True) and remain == bool(True) :
                msg_xlsx("p","fu",numberex,"  +After Request Vacation : correct figures <Pass>")
            else:
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : correct figures <Fail>")

            break
    
    msg("t",infor_before)
    msg("t",infor_after)
    
def check_number_of_days_cancel(before,after,hour_use,vc_name,oneday,use_hour_unit,type_request):
    # < Check number of days before request > #
    numberex=param_excel["number"]
    total=True
    used=True
    remain=True
    msg("p","-[Available Vacation]")
    for vacation in before:
        if vacation["vacation_name"] == vc_name :
            vc_bf_use=vacation
            infor(vc_bf_use,"Info Vacation before cancel",hour_use)
            days=change_hour_to_day(vc_bf_use["used"],vc_bf_use["remain"],oneday,"plus",hour_use,use_hour_unit,type_request)
            if vc_bf_use["total"]== days:
                msg_xlsx("p","fu",numberex,"  +Before Request Vacation : correct figures <Pass>")
            else:
                msg_xlsx("f","fu",numberex,"  +Before Request Vacation : correct figures <Fail>")
            break

    
    # < Check number of days after request > #
    for vacation in after: 
        if vacation["vacation_name"] == vc_name :
            vc_af_use=vacation
            infor(vc_af_use,"Info Vacation before cancel",hour_use)
            if vc_af_use["total"] != vc_bf_use["total"] :
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : Total column <Fail>")
                total=False
            else:
                msg("p","  +After Request Vacation : Total column <Pass>")
        
           
            used_before_plus_used= change_hour_to_day(vc_bf_use["used"]," ",oneday,"minus",hour_use,use_hour_unit,type_request)
            if vc_af_use["used"] != used_before_plus_used:
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : Used column <Fail>")
                used=False
            else:
                msg("p","  +After Request Vacation : Used column <Pass>")

            remain_before_minus_used=change_hour_to_day(vc_bf_use["remain"]," ",oneday,"plus",hour_use,use_hour_unit,type_request)
            if vc_af_use["remain"] != remain_before_minus_used:
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : Remain column <Fail>")
                remain=False
            else:
                msg("p","  +After Request Vacation : Remain column <Pass>")
            
            if total== bool(True) and used== bool(True) and remain == bool(True) :
                msg_xlsx("p","fu",numberex,"  +After Request Vacation : correct figures <Pass>")
            else:
                msg_xlsx("f","fu",numberex,"  +After Request Vacation : correct figures <Fail>")

            break

def select_approver():
    # SELECT APPROVER #
    scroll()
    msg("p", "-[Select Approver]")
    use_public_approval_line=is_Displayed(data["rq_vc"]["bt_select_approver"])
    select_approver={"result_approver":False,"approver_name":True,"approval_line":False,"approval_exception":False}

    if use_public_approval_line == True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["rq_vc"]["bt_select_approver"]))).click()
       
        # < Select approver by search user > #
        approver="TS2"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["rq_vc"]["delete_all"]))).click()
        ip_search_user=driver.find_element_by_xpath(data["rq_vc"]["search"])
        ip_search_user.click()
        ip_search_user.send_keys(approver)
        search_approver=False
        check_search_approver = False
        if ip_search_user.get_attribute('value') == approver :
            msg("p", "  +Enter user name to search <Pass>")
            
            time.sleep(3)
            check_no_approver=driver.find_elements_by_xpath(data["rq_vc"]["text_list_ap"])
            if len(check_no_approver) !=2:
                time.sleep(3)
                list_approver=driver.find_elements_by_xpath(data["rq_vc"]["list_approver"])    
                try :
                    total_approver=total_data(list_approver)
                    for i in range(1,total_approver + 1):
                        approver_name=driver.find_element_by_xpath(xpath("li",i,data["rq_vc"]["sl_approver"]))
                        if approver_name.text == approver :
                            search_approver=True
                            break
                except :
                    search_approver=False
                if search_approver == True :
                    approver_name.click()
                    if approver_name.is_enabled() == True :
                        check_search_approver= True
                        msg("p", "  +Select approver from result search <Pass>")
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["rq_vc"]["bt_add"]))).click()
                        driver.implicitly_wait(5)
                        if is_Displayed(data["rq_vc"]["check_bt_save"]) == bool(False) :
                            msg("p", "  +Click on Add button to add selected approver  <Pass>")
                            driver.find_element_by_xpath(data["rq_vc"]["bt_save"]).click()
                            driver.implicitly_wait(5)

                            if is_Displayed(data["rq_vc"]["bt_select_cc"])== bool(True):
                                msg("p", "  +Click on save button to save the selected approver <Pass>")
                                list_app=driver.find_elements_by_xpath(data["rq_vc"]["list_approver1"])
                                total_app=total_data(list_app)

                                if total_app==0:
                                    msg_xlsx("f","fu",re_vc,"  +Save selected approver <Fail>")
                                else:
                                    result_app=False
                                    for i in range(1,total_app+1):
                                        app_name=driver.find_element_by_xpath(data["rq_vc"]["approver_name1"]+"div["+str(i)+data["rq_vc"]["approver_name2"]).text
                                        if app_name.strip()==approver.strip():
                                            msg("p", "  +Save selected approver <Pass>")
                                            result_app=True
                                            select_approver["result_approver"]=True
                                            select_approver["approver_name"]=approver
                                            return select_approver
                                        
                                    if result_app== False :
                                        msg_xlsx("f","fu",re_vc, "  +Save selected approver <Fail>")
                                        return select_approver
                            else:
                                msg_xlsx("f","fu",re_vc,"  +Click on save button to save the selected approver <Fail>")
                        else:
                            msg_xlsx("f","fu",re_vc, "  +Click on Add button to add selected approver <Fail>")
                    else:
                        msg_xlsx("f","fu",re_vc, "  +Select approver from result search <Fail>")
                        
                else:
                    msg("p", "  +The searcher is not in the list of approvers <Pass>")
            
            else:
                msg("p", "  +The searcher is not in the list of approvers <Pass>")

        else:
            msg_xlsx("f","fu",re_vc,"  +Enter user name to search <Fail>")
            
            

        if check_search_approver == False :
            # < Select approver from list approver > #
            ip_search_user.clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["rq_vc"]["delete_all"]))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["rq_vc"]["bt_save"]))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["rq_vc"]["bt_select_approver"]))).click()
        
            time.sleep(4)
            check_no_approver=driver.find_elements_by_xpath(data["rq_vc"]["text_list_ap"])
        
            if len(check_no_approver) !=0 :
                selected_user=driver.find_element_by_xpath(data["rq_vc"]["sl_ap_firt"])
                user_name=selected_user.text
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,data["rq_vc"]["sl_ap_firt"]))).click()
                
                button=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,data["rq_vc"]["bt_ap_firt"])))
                is_selected= button.is_selected()

                if is_selected== True :
                    msg("p", "  +Click on user from list approver to select approver <Pass>")
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,data["rq_vc"]["bt_add"]))).click()

                    if is_Displayed(data["rq_vc"]["check_bt_save"]) == bool(False) :
                        msg("p", "  +Click on Add button to add selected approver  <Pass>")

                        driver.find_element_by_xpath(data["rq_vc"]["bt_save"]).click()
                        if is_Displayed(data["rq_vc"]["bt_select_cc"])== bool(True):
                            msg("p", "  +Click on save button to save the selected approver <Pass>")
                            scroll()
                            from_element = driver.find_element_by_xpath(data["rq_vc"]["bt_select_approver"])
                            to_element = driver.find_element_by_xpath(data["rq_vc"]["bt_select_cc"])
                            scrolling_to_target(to_element)
                        
                            list_app=driver.find_elements_by_xpath(data["rq_vc"]["list_approver1"])
                            total_app=total_data(list_app)
                        
                            if total_app==0:
                                msg_xlsx("f","fu",re_vc,"  +Save selected approver <Fail>")
                            else:
                                
                                for i in range(1,total_app+1):
                                    app_name=driver.find_element_by_xpath(data["rq_vc"]["approver_name3"]+str(i)+data["rq_vc"]["approver_name4"]).text
                                    if app_name.strip()==user_name.strip():
                                        msg("p", "  +Save selected approver <Pass>")
                                        select_approver["result_approver"]=True
                                        select_approver["approver_name"]=user_name.strip()
                                        result_app=True
                                        break
                                        
                                    
                                if select_approver["result_approver"]== False :
                                    msg_xlsx("f","fu",re_vc,"  +Save selected approver <Fail>")
                        else:
                            msg_xlsx("f","fu",re_vc,"  +Click on save button to save the selected approver <Fail>")
                            
                    else:
                        msg_xlsx("f","fu",re_vc,"  +Click on Add button to add selected approver <Fail>")
                        
                else :
                    msg_xlsx("f","fu",re_vc,"  +Click on user from list approver to select approver <Fail>")
                    
            else:
                msg_xlsx("p","fu",re_vc,"-No approver to choose <Pass>")
            return select_approver
    else:
        if is_Displayed(data["rq_vc"]["bt_quick_approver"])== bool(True): 
            msg("p", "  +Use public approval line <Pass>")
            select_approver["result_approver"]=True
            select_approver["approval_line"]=True
            list_approver=[]
            list_app=driver.find_elements_by_xpath(data["rq_vc"]["list_approver1"])
            total_app=total_data(list_app)
            for i in range(1,total_app+1):
                app_name=driver.find_element_by_xpath(data["rq_vc"]["approver_name1"]+"div["+str(i)+data["rq_vc"]["approver_name2"]).text
                list_approver.append(app_name)
            select_approver["approver_name"]= list_approver
            return select_approver 

        else:
            msg("p", "  +Requester is approval exception <Pass>")
            select_approver["result_approver"]=True
            select_approver["approval_exception"]=True
            return select_approver

def function_search():
    #[Function search]#
    try:
        orgex=param_excel["sl_org"]
        searchex=param_excel["search"]
        user_name="TS2"
        result_select_user={"search":"False","select_ogr":"False"}
        driver.find_element_by_xpath(data["rq_vc"]["bt_select_cc"]).click()
        if is_Displayed(data["rq_vc"]["bt_add_cc"])== bool(True):
            driver.find_element_by_xpath(data["rq_vc"]["dele_all_cc"]).click()

            # < Search user > #
            list_departmaent=driver.find_elements_by_xpath(data["rq_vc"]["org_search"])
            before_search=len(list_departmaent)
            firt_department=driver.find_element_by_xpath(data["rq_vc"]["firt_depart"]).text
            ip_search_user=driver.find_element_by_xpath(data["rq_vc"]["search"])
            driver.implicitly_wait(5)
            ip_search_user.click()
            ip_search_user.send_keys(user_name)
            ip_search_user.send_keys(Keys.RETURN)
            
            if ip_search_user.get_attribute('value') == user_name :
                msg("p", "  +Enter user name to search <Pass>")
                
                time.sleep(1)
                cc=driver.find_element_by_xpath(data["rq_vc"]["cc_namea"]).text
                if cc== "No data." :
                    search_cc=False
                    msg_xlsx("p","fu",searchex,"  +Search user <Pass>")

                else:
                    time.sleep(2)
                    list_departmaent1=driver.find_elements_by_xpath(data["rq_vc"]["org_search"])
                    after_search=len(list_departmaent1)
                    if before_search != after_search :
                        msg_xlsx("p","fu",searchex, "  +Search user <Pass>")
                        result_select_user["search"]=True
                    else:
                        firt_department1=driver.find_element_by_xpath(data["rq_vc"]["firt_depart"]).text
                        if firt_department ==firt_department1:
                            msg_xlsx("f","fu",searchex, "  +Search user <Fail>")
                        else:
                            msg_xlsx("p","fu",searchex, "  +Search user <Pass>")
                            result_select_user["search"]=True      
            else:
                msg_xlsx("f","fu",searchex, "  +Enter user name to search <Fail>")

            # < Select user from Org > #
            ip_search_user.clear()
            driver.find_element_by_xpath(data["rq_vc"]["bt_save"]).click()
            driver.find_element_by_xpath(data["rq_vc"]["bt_select_cc"]).click()
            selected_cc= select_user_from_depart() 
            if selected_cc != False :
                msg_xlsx("p","fu",orgex,"  +Select user form Org  <Pass>")
                result_select_user["select_ogr"]=True      
            else:
                msg_xlsx("f","fu",orgex,"  +Select user form Org  <Fail>")
            driver.find_element_by_xpath(data["rq_vc"]["bt_save"]).click()
           
    except:
        driver.find_element_by_link_text("My Vacation Status").click()

def select_cc_enter_reason():
    # SELECT CC #
    time.sleep(3)
    scroll()
    msg("p", "-[Select CC]")
    driver.find_element_by_xpath(data["rq_vc"]["bt_select_cc"]).click()

    if is_Displayed(data["rq_vc"]["bt_add_cc"])== bool(True):
        msg("p", "  +Click on Select CC button <Pass>")

        driver.find_element_by_xpath(data["rq_vc"]["dele_all_cc"]).click()
        selected_cc= select_user_from_depart() 
        if selected_cc != False :
            msg("p", "  +Click on user form Org to select cc <Pass>")
            time.sleep(1)
            driver.find_element_by_xpath(data["rq_vc"]["bt_add_cc"]).click()
            msg("p", "  +Click on Add button <Pass>")

            driver.find_element_by_xpath(data["rq_vc"]["bt_save"]).click()
            msg("p", "  +Click on save button <Pass>")

            time.sleep(1)   
            if is_Displayed(data["rq_vc"]["bt_select_cc"])== bool(True):
                msg("p", "  +Click on save button to save the selected cc <Pass>")

                list_cc=driver.find_elements_by_xpath(data["rq_vc"]["list_cc"])
                total_cc=total_data(list_cc)

                if total_cc==0:
                    msg_xlsx("f","fu",re_vc, "  +Select CC <Fail>")
                else:
                    i=1
                    result_cc=False
                    while i<=total_cc :
                        cc_name=driver.find_element_by_xpath(data["rq_vc"]["cc_name1"]+"div["+str(i)+data["rq_vc"]["cc_name2"]).text
                        if cc_name.strip()==selected_cc.strip():
                            msg("p", "  Select CC <Pass>")
                            result_cc=True
                            break
                        i=i+1
                    if result_cc== False :
                        msg_xlsx("f","fu",re_vc, "  +Select CC<Fail>")
            else:
                msg_xlsx("f","fu",re_vc, "  +Click on save button to save the selected cc <Fail>")

        else:
            msg_xlsx("f","fu",re_vc, "  +Click on user form Org to select cc <Fail>")
    else:
        msg_xlsx("f","fu",re_vc, "  +Click on Select CC button <Fail>")


    # ADD REASON #
    scroll()
    if is_Displayed(data["rq_vc"]["reason"])== bool(True):
        reason=driver.find_element_by_xpath(data["rq_vc"]["reason"])
        reason.click()
        reason.send_keys(data["rq_vc"]["reason_text"])
        if reason.get_attribute('value') == data["rq_vc"]["reason_text"]:
            msg("p", "-Enter reason <Pass>")
        else:
            msg_xlsx("f","fu",re_vc, "-Enter reason <Fail>")
    else:
        msg("p", "-No use reason <Pass>")
    
def hour_used(use_hour_unit,type_use):
    if bool(use_hour_unit) == bool(True) :
        if type_use=="allday":
            hour_use= 1
        elif type_use=="hour_unit":
            hour_use=hours_set_from_time_card(type_use)
        else:
            hour_use=0.5
            
        return float(hour_use)
    else:
        if type_use=="allday":
            hour_use= 1 
        
        else:
            hour_use=4/10
        return float(hour_use)

def check_use_hour_unit_half_day(total_vc):
    # < Choose vacation name to request > #
    use_hour_unit=False
    all_vacation=[]
    available_vacation={"available_vacation":""}
    
    
    if total_vc == 0 :
        available_vacation["available_vacation"]=0
        all_vacation.append(available_vacation)
        #msg("p","-There is no vacation to request")
    else:
        i=1
        available_vacation["available_vacation"]=total_vc
        all_vacation.append(available_vacation)
        while i <= total_vc:
            time.sleep(1)
            usage_settings={"vacation_name":"","number_of_days":"","number_of_hours":"","use_hour_unit":"","use_half_day":"","hour_use":""}
            driver.find_element_by_css_selector(data["rq_vc"]["select_vacation"]).click()
            driver.find_element_by_xpath("//body/div[4]/div/div/div[" + str(i) +"]").click()
            vacation = vacation_use_for_request()
            usage_settings["vacation_name"]=vacation["vacation_name"]
            usage_settings["number_of_days"]=vacation["number_of_days"]
            usage_settings["number_of_hours"]=vacation["number_of_hours"]

            if is_Displayed(data["rq_vc"]["hour_unit"]) == bool(True) :
                use_hour_unit= True
                usage_settings["use_hour_unit"]=True
            else:
                usage_settings["use_hour_unit"]=False

            if is_Displayed(data["rq_vc"]["radi_am"])== bool(True):
                usage_settings["use_half_day"]=True
                if use_hour_unit == True:
                    usage_settings["hour_use"]=hour_used(use_hour_unit,"half_am")
            else:
                usage_settings["use_half_day"]=False
            all_vacation.append(usage_settings)
            i=i+1

    return all_vacation    
            
def select_vacation_use_hour_unit_half_day(total_vc,list_vc_use_half,hour_use,type_vc):
    i=1
    while i<=total_vc:
        time.sleep(1)
        driver.find_element_by_css_selector(data["rq_vc"]["select_vacation"]).click()
        driver.find_element_by_xpath("//body/div[4]/div/div/div[" + str(i) +"]").click()
        vacation_name=driver.find_element_by_xpath(data["rq_vc"]["vacation_name"]).text
        vacation_name=vacation_name[None:int(vacation_name.rfind("("))-1] + vacation_name[int(vacation_name.rfind(")"))+2: None]
        for vacation in list_vc_use_half:
            if vacation["vacation_name"]== vacation_name :
                if type_vc=="hour-unit":
                    if float(vacation["number_of_hours"]) >= 1 or float(vacation["number_of_days"]) >= hour_use:
                        return vacation_name
                else:
                    if float(vacation["number_of_hours"]) >= hour_use or float(vacation["number_of_days"]) >= hour_use:
                        return vacation_name
        i=i+1      
                        
    return False

def check_result_request():
    try :
        notification=driver.execute_script('return document.getElementById("noty_layout__topRight").innerText')
        content_notification=notification.split("\n")
        if content_notification[0]=="success":
            return "pass"
        else:
            return "noti_error"+content_notification[1]
    except:
        time.sleep(1)
        if is_Displayed(data["my_vt"]["vc_history"]) == bool(True):
            return "pass"
        else:
            return "fail"

def view_detail_used(type_request,use_hour_unit):
    
    if type_request=="all_day":
        return "1D"
    elif type_request=="vacation_consecutive":
        return "2D"

    else:
        if use_hour_unit == True:
            return "4H"
        else:
            return "0.5D"

def check_approver_reason(type_request,approver):
   
    result_reason= False
    result_approver=False
    if type_request=="all_day":
        reason=driver.find_element_by_xpath(data["rq_vc"]["content_reason"]).text
        data["rq_vc"]["reason_text"]

        if reason == data["rq_vc"]["reason_text"] :
            msg("p", "-View detail : Show reason <Pass> " , )
            result_reason=True
        else:
            msg_xlsx("f","fu",detailex,"-View detail : Show reason <Fail> "  )

        
        content_approver=False
        if approver["approval_exception"]== True:
            if is_Displayed(data["rq_vc"]["approval_exception"]) == bool(False):
                msg("p", "-View detail user is approval exception: Approver <Pass> " )
                result_approver=True
                
            else:
                msg_xlsx("f","fu",detailex, "-View detail user is approval exception: Approver <Fail> " )

        else:
            i=j=1
            if is_Displayed(data["rq_vc"]["approval_exception"]) == bool(True):
                time.sleep(2)
                list_approver=driver.find_elements_by_xpath(data["rq_vc"]["content_vc_approver"])
                total_approver=total_data(list_approver)
                if approver["result_approver"]== True :
                    while i<= total_approver :
                        approver_name=driver.find_element_by_xpath(xpath2(data["rq_vc"]["ct_approver_name"],i,data["rq_vc"]["ct_approver_name1"])).text
                        if approver_name.strip() == approver["approver_name"].strip():
                            msg("p", "-View detail : Approver <Pass> " )
                            result_approver=True
                            content_approver= True
                            break
                        i=i+1
                    if content_approver== False :
                        msg_xlsx("f","fu",detailex, "-View detail : Approver <Fail> "  )
                else:
                    while j <= total_approver :
                        approver_name=driver.find_element_by_xpath(xpath2(data["rq_vc"]["ct_approver_name"],j,data["rq_vc"]["ct_approver_name1"])).text
                        if approver_name == approver["approver_name"][0]:
                            msg("p", "-View detail use approval line: Approver <Pass> " , )
                            result_approver=True
                            content_approver= True
                            break
                        j=j+1
                    if content_approver== False :
                        msg_xlsx("f","fu",detailex,"-View detail use approval line : Approver <Fail> " )
            else:
                msg_xlsx("f","fu",detailex,"-View detail Approver <Fail> ")
        if result_reason == True and result_approver== True :
            return True
        else :
            return False
          
def check_created_request(info_vc,type_request,use_hour_unit ,approver):
    i=1
    result=False
    result_vc_date=False
    result_number_use=False
    result_re_date=False
    time.sleep(4)
    try:
        driver.find_element_by_xpath(data["rq_vc"]["bt_refresh"]).click()
        list_request=driver.find_elements_by_xpath(data["rq_vc"]["list_request"])
        total_request=total_data(list_request)
        
        if total_request >= 1 :
            while i<= total_request:
                vacation_request={"vc_name":"","vc_date":"","request_date":"","status":"Request"}
                if approver["approval_exception"]== True:
                    vacation_request["status"]="Approved"
                    info_vc["status"]="Approved"
                vacation_request["vc_name"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_name"])).text
                vacation_request["vc_date"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_vc_date"])).text
                vacation_request["request_date"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_date"])).text
                vacation_request["status"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_status"])).text
                vacation_request["vc_date"]= vacation_request["vc_date"].replace("\n", "")
                vacation_request["vc_name"]=vacation_request["vc_name"].replace("\n", "").replace(" ", "")
            
                if info_vc["vc_name"]==vacation_request["vc_name"] and info_vc["vc_date"]==vacation_request["vc_date"] and info_vc["request_date"]==vacation_request["request_date"] and info_vc["status"]==vacation_request["status"] :
                    msg_xlsx("p","fu",re_vc,"-Request vacation is displayed in vacation request list <Pass>")

                    # view detail request vacation  #
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,xpath3("tr",str(i),data["rq_vc"]["ic_detail"],i-1,data["rq_vc"]["ic_detail1"])))).click()
                    time.sleep(2)

                    vc_date=driver.find_element_by_xpath(data["rq_vc"]["content_vc_date"]).text
                    if type_request=="all_day":
                        vc_date=vc_date.replace("(", "").replace(")", "")

                    elif type_request=="vacation_consecutive":
                        vc_date=vc_date
                        vacation_request["vc_date"]=vacation_request["vc_date"][None:21]

                    else:
                        vc_date=vc_date[None: int(vc_date.rfind("H"))-1] +vc_date[int(vc_date.rfind("H")): len(vc_date)-1] 


                    if vc_date == vacation_request["vc_date"] :
                        msg("p", "-View detail : vacation date <Pass> ")
                        result_vc_date=True
                    else:
                        msg_xlsx("f","fu",detailex,"-View detail : vacation date <Fail> " )
                    

                    use=driver.find_element_by_xpath(data["rq_vc"]["content_vc_use"]).text
                    days_use=view_detail_used(type_request,use_hour_unit)
                
                    if use == days_use :
                        msg("p", "-View detail : Number of days use <Pass> " )
                        result_number_use=True
                    else:
                        msg_xlsx("f","fu",detailex,"-View detail : Number of days use <Fail> ")
                    

                    request_date=driver.find_element_by_xpath(data["rq_vc"]["content_request_date"]).text
                    if request_date == vacation_request["request_date"] :
                        msg("p", "-View detail : Request date <Pass> "  )
                        result_re_date=True
                    else:
                        msg_xlsx("f","fu",detailex,"-View detail : Request date <Fail> " )
                
                    result_view_approver_and_reason=check_approver_reason(type_request,approver)
                    if type_request=="all_day":
                        if result_vc_date== True and result_number_use== True and result_re_date== True and result_view_approver_and_reason== True:
                            msg_xlsx("p","fu",detailex,"-View detail request vacation <Pass>")
                        else:
                            msg_xlsx("f","fu",detailex,"-View detail request vacation <Fail>")
                    else:
                        if result_vc_date== True and result_number_use== True and result_re_date== True :
                            msg_xlsx("p","fu",detailex,"-View detail request vacation <Pass>")
                        else:
                            msg_xlsx("f","fu",detailex,"-View detail request vacation <Fail>")

                    result = True
                    break
                i=i+1

           
            if result == False:
                msg_xlsx("f","fu",re_vc,"-Request vacation is displayed in vacation request list <Fail>")
        else: 
            msg_xlsx("f","fu",re_vc,"-Request vacation is displayed in vacation request list <Fail>")
    except:
            driver.find_element_by_link_text("My Vacation Status").click()

def time_comparison(request_date,today):
    
    if request_date.rfind("~")> 0 :
       request_date=request_date[int(request_date.rfind("~"))+1: None]
    request_date = datetime.datetime.strptime(request_date.replace("-", "/").replace("2021", "21"), "%y/%m/%d")
    today = datetime.datetime.strptime(today.replace("-", "/").replace("2021", "21"), "%y/%m/%d")
    if request_date < today :
        return False  
    else:
        return True

def select_hour_use_hour_unit():
    
    driver.find_element_by_xpath(data["rq_vc"]["hour_unit"]).click()
    driver.find_element_by_xpath(data["rq_vc"]["hour_start"]).click()
    start_options=driver.find_elements_by_xpath(data["rq_vc"]["start_option"])
    if len(start_options) > 1:
        driver.find_element_by_xpath(data["rq_vc"]["sl_hour_start"]).click()
    else:
        msg_xlsx("p","fu",re_vc,"-No hour start to choose <Pass>")
        return False

    driver.find_element_by_xpath(data["rq_vc"]["hour_end"]).click()
    end_options=driver.find_elements_by_xpath(data["rq_vc"]["end_option"])
    if len(end_options) > 1:
        driver.find_element_by_xpath(data["rq_vc"]["sl_hour_end"]).click()
    else:
        msg_xlsx("p","fu",re_vc,"-No hour end to choose <Pass>")
        return False
    
    hour_selected=driver.find_element_by_xpath(data["rq_vc"]["selected_date"]).text
    hour_selected=hour_selected[int(hour_selected.rfind("(")): int(hour_selected.rfind(")"))+1]
    return hour_selected

def info_request_list(i):
    infor_request={"no":"","vacation_name":"","vacation_date":"","use":"","request_date":"","status":"","icon_cancel":"","vacation_time":""}
    infor_request["no"]=str(i)
    infor_request["vacation_name"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_name"])).text
    infor_request["vacation_date"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_vc_date"])).text
    infor_request["use"]=driver.find_element_by_xpath(xpath(data["rq_vc"]["tr_re_use"],str(i),data["rq_vc"]["re_use"])).text
    infor_request["request_date"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_date"])).text
    infor_request["status"]=driver.find_element_by_xpath(xpath("tr",str(i),data["rq_vc"]["re_status"])).text
    infor_request["vacation_time"]=infor_request["vacation_date"][None: int(infor_request["vacation_date"].rfind("\n"))]
    return infor_request

def count_all_vacation_request():
    # Get all status from list request vacation #
    i=1
    time.sleep(3)
    total_request=0

    if is_Displayed(data["rq_vc"]["check_list_re"]) == bool(False) : 
        driver.find_element_by_xpath(data["mn_pro"]["ic_to_end_page"]).click()
        end_page_text=driver.find_element_by_xpath(data["mn_pro"]["page_current"]).text
        end_page=int(end_page_text)
        driver.find_element_by_xpath(data["mn_pro"]["ic_to_first_page"]).click()
        
        while i <= end_page:
            if i == end_page :
                time.sleep(3)
                total_re=driver.find_elements_by_xpath(data["mn_pro"]["list_re_vc"])
                total_request=total_request+total_data(total_re)
            else:
                total_request=total_request+20
            i=i+1
    return total_request

def two_requests_are_the_same(request1,request2):
    if request1["vacation_name"]==request2["vacation_name"] and request1["vacation_date"]==request2["vacation_date"] and request1["use"]==request2["use"] and request1["request_date"]==request2["request_date"]:
        return True
    else: 
        return False
               
def login(domain):
    
    msg("n","LOGIN")
    driver.get("http://"+domain+"/ngw/app/#/sign")
    driver.implicitly_wait(10)


    driver.find_element_by_id("log-userid").send_keys(data["user"])
    msg("p","-Input id <Pass>")
   
    driver.switch_to.frame(driver.find_element_by_id("iframeLoginPassword"))
    driver.find_element_by_id("p").send_keys(data["pass"])
    msg("p","-Input pass  <Pass>")
    driver.switch_to.default_content()

    driver.find_element_by_id("btn-log").send_keys(Keys.RETURN)
    msg("p","-Click on Login button  <Pass>")
    
def access_menu_vacation(domain):

    
    #window#
    driver.get("http://"+domain+"/ngw/app/#/nhr")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["iframe_vc"])))
    driver.switch_to.frame(driver.find_element_by_xpath(data["iframe_vc"]))
    #
   
    if is_Displayed(data["menu_vc"]) == True :
        driver.find_element_by_xpath(data["menu_vc"]).click()
        if is_Displayed(data["sm_my_vc_sta"]) == True :
            result= True
            msg("n","[ACCESS VACATION]")
            msg("p","-Access Menu Vacation <Pass>")
            popup_time_card()
            
        else:
            result=False
            msg("f","-Access Menu Vacation <Fail>")
    else :
        result=False
        msg("p","-No Menu Vacation <Pass>")
    return result

def vacation_displayed_in_time_card(date_request):
    try :
        i=1
        time_sh=param_excel_tc["sub_calendar"]
        vaca=param_excel_tc["vacation"]
        current_date = datetime.date.today()
        month_request=date_request.month
        current_month = current_date.month
        number_of_clicks=int(month_request - current_month)

        driver.find_element_by_xpath(data["menu_tc"]).click()
        driver.find_element_by_link_text("Timesheets").click()
        
        if is_Displayed(data["tab_calen_tc"]) == True :

            if is_Displayed(data["no_work_tc"]) == False :
                msg_xlsx("p","fu",vaca,"-Account not added Work Policy ,Vacation does not show in time card <Pass>")
            else:
                time.sleep(2)
                driver.find_element_by_css_selector(data["date_tc"]).click()
                if number_of_clicks == 0 :
                    click_date_time_card(date_request)
                else:
                    while i <= number_of_clicks :
                        driver.find_element_by_css_selector(data["ic_next_tc"]).click()
                        click_date_time_card(date_request)

                if is_Displayed(data["row_vaca_tc"]) == True :
                    msg_xlsx("p","fu",vaca,"-Vacation is displayed in in time card <Pass>")
                else:
                    msg_xlsx("f","fu",vaca,"-Vacation is displayed in in time card <Fail>")

        else:
            msg_xlsx("f","ac",time_sh,"-Access submenu TimeSheets <Fail>")
        driver.find_element_by_xpath(data["menu_vc"]).click()
    except:
        driver.find_element_by_xpath(data["menu_vc"]).click()

def time_clockin():
    try :
        time_clock_in= False
        driver.find_element_by_xpath(data["menu_tc"]).click()
        driver.find_element_by_link_text("Timesheets").click()
        
        if is_Displayed(data["tab_calen_tc"]) == True :
            if is_Displayed(data["no_work_tc"]) == True :
                clock_in=driver.find_element_by_xpath(data["time_clock_in"]).text
                if clock_in.rfind("00")>0 :
                    time_clock_in=clock_in

                driver.find_element_by_xpath(data["menu_vc"]).click()
                return time_clock_in           
    except:
        driver.find_element_by_xpath(data["menu_vc"]).click()

def collect_clock_in_from_time_card(time_clock_in,type_request,request_date):
    if time_clock_in != False :
        clock_in=time_clock_in[None: int(time_clock_in.rfind("("))]
        clock_in_hour=time_clock_in[None: int(time_clock_in.rfind(":"))]

        if type_request=="hour_unit":
            time_end=int(clock_in_hour) + 2
            vacation_date = str(request_date)+" [ Use: 2H ] "+ "[ " + clock_in + "~ " + str(time_end) +":00 ]"
        else:
            time_end=int(clock_in_hour) + 4 
            vacation_date = str(request_date)+" [ Use: 4H ] "+ "[ " + clock_in + "~ " + str(time_end) +":00 ]"
        return vacation_date
   
def sm_re_vc_request_vacation_all_day(request_date,result_select_approver,approver):
    # [REQUEST VACATION : ALL DAY] #

    result_date=True
    result_select_vc= False
    use_hour_unit= False
    vacation_request={"vc_name":"","vc_date":"","request_date":request_date,"status":"Request"}

    # Update status for request #
    if approver["approval_exception"] == True:
        vacation_request["status"]="Approved"

    # < Choose date to request [go to my vacation to check used dates and select date to request vacation] > #
    vc_date=select_days_to_request_leave()
    if vc_date != False:
        vacation_request["vc_date"]=str(vc_date)+"All day Off"
    else:
        result_date=False

    select_approver()

    # < Choose vacation name to request > #
    total_vc=total_vacation()
    number_before_request=available_vacation()
    oneday=hours_set_from_time_card("allday")
    infor_vacation=check_use_hour_unit_half_day(total_vc)
    
    
    # Check there are any vacations using hour unit => change the way to check the number of leave days #
    i=1
    while i<=total_vc:
        if infor_vacation[i]["use_hour_unit"]== True:
            use_hour_unit= True
            break
        i=i+1

    # Check the remaining days of each vacation are enough to request #
    i=1
    while i<=total_vc:
        time.sleep(1)
        driver.find_element_by_css_selector(data["rq_vc"]["select_vacation"]).click()
        driver.find_element_by_xpath("//body/div[4]/div/div/div[" + str(i) +"]").click()
        vc_use_for_request = vacation_use_for_request()
        hour_use=hour_used(use_hour_unit,"allday")
        remain_days=vc_use_for_request["number_of_days"]
        remain_hours=vc_use_for_request["number_of_hours"]
        vc_name=vc_use_for_request["vacation_name"]

        # If vacation is other vacation can use this vacation to request #
        if float(remain_days)== 0 and float(remain_hours) == 0:
            result_select_vc= True
            vacation_request["vc_name"]=vc_name.replace(" ", "")
            msg("p", "-Select Vacation to request <Pass>")
            msg("p", "  +Vacation name : " +vc_name + "<Pass>" )
            break

        # If vacation is grant/regular , need to check there are enough days to request #
        else :
            if float(remain_days) >= hour_use :
                result_select_vc= True
                vacation_request["vc_name"]=vc_name.replace(" ", "")
                msg("p", "-Select Vacation to request <Pass>")
                msg("p", "  +Vacation name : " +vc_name + "<Pass>" )
                
                break 
        i=i+1
    # Vacation does not have enough days to choose #
    if result_select_vc== False:
        msg_xlsx("p","fu",re_vc,"-No vacation to request <Pass>")
    
    # < Select cc - Enter reason > #
    select_cc_enter_reason()

    
    # < Send request vacation , if selected vacation and selected approver > #  
    if result_select_vc == bool(True) and result_select_approver  ==bool(True) and result_date==bool(True):
        driver.find_element_by_xpath(data["rq_vc"]["bt_request_be"]).click()
        driver.find_element_by_css_selector(data["rq_vc"]["bt_request_af"]).click()

        result_request=check_result_request()
        if result_request== "pass":
            msg_xlsx("p","fu",re_vc,"-Request vacation (All day)  <Pass>")

            # < Check created request and view detail request > #
            check_created_request(vacation_request,"all_day",use_hour_unit,approver)

            # < Check number of days off after request vacation at available vacation > #
            number_after_request=available_vacation()
            check_number_of_days_off(number_before_request,number_after_request,hour_use,vc_name,oneday,use_hour_unit,"all_day")
            
            # < Vacation is displayed in in time card > #
            vacation_displayed_in_time_card(vc_date)

            # < Cancel Request and number of vacation is updated  > #
            sm_my_vc_cancel_request(oneday,use_hour_unit)
        
        elif result_request== "fail":
            msg_xlsx("p","fu",re_vc,"-Can't request (All day) <Pass>")
        else:
            msg_xlsx("p","fu",re_vc,"-Conditions for request vacation are not valid (All day) <Pass>")
            msg("p", "-Msg :",result_request)
    
def sm_re_vc_request_vacation_half_am(request_date,result_select_approver,approver):
    #[REQUEST VACATION : HALF DAY (AM)]#

    result_date=True
    vacation_request={"vc_name":"","vc_date":"","request_date":request_date,"status":"Request"}


    # Time clockin form time card #
    time_clock_in=time_clockin()

    # Update status for request #
    if approver["approval_exception"] == True:
        vacation_request["status"]="Approved"


    # < Choose date to request [go to my vacation to check used dates and select date to request vacation] > #
    vacation_request["request_date"]=str(datetime.date.today())
    vc_date=select_days_to_request_leave()
    if vc_date != False:
        vacation_request["vc_date"]=str(vc_date)+"Half Day (AM)"
    else:
        result_date=False

    # < Choose vacation name to request > #
    number_before_request=available_vacation()
    oneday=hours_set_from_time_card("allday")
    use_half_day= 0
    use_hour_unit= False
    result_select_vc=False
    total_vc=total_vacation()
    list_vc_use_half=[]
    infor_vacation=check_use_hour_unit_half_day(total_vc)
    
    # Check there are any vacations using hour unit => change the way to check the number of leave days #
    # Check there are any vacations using half day #
    if total_vc==0:
        msg_xlsx("p","fu",re_vc,"-No vacation to request ( Half day am ) <Pass>")

    else:
        for i in range(1,len(infor_vacation)):
            if infor_vacation[i]["use_hour_unit"]== True:
                use_hour_unit= True
                break
        for i in range(1,len(infor_vacation)):
            if infor_vacation[i]["use_half_day"]== True:
                list_vc_use_half.append(infor_vacation[i])
                use_half_day= use_half_day+1

        if  use_half_day == 0:
            msg_xlsx("p","fu",re_vc,"-No vacation use half day am <Pass>")
        else:
            hour_use=hour_used(use_hour_unit,"half_am")

            result_select_vc=select_vacation_use_hour_unit_half_day(total_vc,list_vc_use_half,hour_use,"half-day")
            if  result_select_vc != False :
                vacation_request["vc_name"]=result_select_vc.replace(" ", "")
                msg("p", "-Select Vacation to request <Pass>")
                msg("p", "  +Vacation name  : " + result_select_vc + "<Pass>" )
                
                driver.find_element_by_xpath(data["rq_vc"]["radi_am"]).click()
                time_request=driver.find_element_by_xpath(data["rq_vc"]["selected_date"]).text
                time_time_card=collect_clock_in_from_time_card(time_clock_in,"half-day",vc_date)
               
                
                if time_request == time_time_card:
                    msg("p", "-Time clockin use for request vacation <Pass>")
                else:
                    msg("f", "-Time clockin use for request vacation <Fail>")

            else:
                msg_xlsx("p","fu",re_vc,"-The number of days is not enough to request by half day <Pass>")
    
    
    # < Send request vacation , if selected vacation and selected approver > # 
    if result_select_vc != bool(False) and result_select_approver  ==bool(True) and result_date == bool(True):
        click_on_request_button()
        result_request=check_result_request()
        if result_request== "pass":
            msg_xlsx("p","fu",re_vc, "-Request vacation ( Half day am ) <Pass>")

            # 
            msg("t","Time from time card :"+time_time_card)
            msg("t","Time from request vacation :"+ time_request)

            # Print information vacation #
            information_vacation("Information vacation :",vacation_request)

            # Check created request and view detail request #
            check_created_request(vacation_request,"half_day",use_hour_unit,approver)

            # Check number of days off after request vacation #
            number_after_request=available_vacation()
            check_number_of_days_off(number_before_request,number_after_request,hour_use,result_select_vc,oneday,use_hour_unit,"half_day")


            # Cancel Request and number of vacation is updated #
            sm_my_vc_cancel_request(oneday,use_hour_unit)
            
        elif result_request== "fail":
            msg_xlsx("p","fu",re_vc,"-Can't request ( Half day am ) <Pass>")
        else:
            msg_xlsx("p","fu",re_vc,"-Conditions for request vacation are not valid ( Half day am ) <Pass>")
            msg("p", "-Msg :",result_request)
    
def sm_re_vc_request_vacation_half_pm(request_date,result_select_approver,approver):
    #[REQUEST VACATION : HALF DAY (PM)]#
    result_date=True
    vacation_request={"vc_name":"","vc_date":"","request_date":request_date,"status":"Request"}

    # < Update status for request > #
    if approver["approval_exception"] == True:
        vacation_request["status"]="Approved"


    # < Choose date to request [go to my vacation to check used dates and select date to request vacation] > #
    vacation_request["request_date"]=str(datetime.date.today())
    vc_date=select_days_to_request_leave()

    if vc_date != False:
        vacation_request["vc_date"]=str(vc_date)+"Half Day (PM)"
    else:
        result_date=False


    # < Choose vacation name to request - Check vacation allow half-day request and enough vacation days to request> #
    number_before_request=available_vacation()
    oneday=hours_set_from_time_card("allday")
    use_half_day= 0
    use_hour_unit= False
    result_select_vc=False
    total_vc=total_vacation()
    list_vc_use_half=[]
    infor_vacation=check_use_hour_unit_half_day(total_vc)

    if total_vc == 0:
        msg_xlsx("p","fu",re_vc,"-No vacation to request ( Half day pm ) <Pass>")
    else:
        for i in range(1,len(infor_vacation)):
            if infor_vacation[i]["use_hour_unit"]== True:
                use_hour_unit= True
                break
        for i in range(1,len(infor_vacation)):
            if infor_vacation[i]["use_half_day"]== True:
                list_vc_use_half.append(infor_vacation[i])
                use_half_day= use_half_day+1

        if  use_half_day == 0:
            msg_xlsx("p","fu",re_vc, "-No vacation use half day pm  <Pass>")
        else:
            hour_use=hour_used(use_hour_unit,"half_pm")
            result_select_vc=select_vacation_use_hour_unit_half_day(total_vc,list_vc_use_half,hour_use,"half-day")
            if  result_select_vc != False :
                vacation_request["vc_name"]=result_select_vc.replace(" ", "")
                msg("p", "-Select Vacation to request <Pass>")
                msg("p", "  +Vacation name  : " + result_select_vc + "<Pass>" )
                driver.find_element_by_xpath(data["rq_vc"]["radi_pm"]).click()
            else:
                msg_xlsx("p","fu",re_vc, "-The number of days is not enough to request by half day <Pass>")
    
    # < Send request vacation , if selected vacation and selected approver > # 
    if result_select_vc != bool(False) and result_select_approver  ==bool(True) and result_date== bool(True):
        click_on_request_button()
        result_request=check_result_request()
        if result_request== "pass":
            msg_xlsx("p","fu",re_vc,"-Request vacation ( Half day pm ) <Pass>")

            # Print information vacation #
            infor_vacation("Information vacation :",vacation_request)

            # Check created request and view detail request #
            check_created_request(vacation_request,"half_day",use_hour_unit,approver)

            # < Check number of days off after request vacation > #
            number_after_request=available_vacation()
            check_number_of_days_off(number_before_request,number_after_request,hour_use,result_select_vc,oneday,use_hour_unit,"half_day")

            # < Cancel Request and number of vacation is updated  > #
            sm_my_vc_cancel_request(oneday,use_hour_unit)
           
        elif result_request== "fail":
            msg_xlsx("p","fu",re_vc,"-Can't request ( Half day pm ) <Pass>")
        else:
            msg_xlsx("p","fu",re_vc, "-Conditions of use for request vacation are not valid  ( Half day pm ) <Pass>")
            msg("p", "-Msg :",result_request)
    
def sm_re_vc_request_vacation_hour_unit(request_date,result_select_approver,approver):
    #[REQUEST VACATION : HOUR UNIT]#
    result_date=True
    vacation_request={"vc_name":"","vc_date":"","request_date":request_date,"status":"Request"}

    # Update status for request #
    if approver["approval_exception"] == True:
        vacation_request["status"]="Approved"


    # < Choose date to request [go to my vacation to check used dates and select date to request vacation] > #
    vacation_request["request_date"]=str(datetime.date.today())
    vc_date=select_days_to_request_leave()
   
    if vc_date == False:
        result_date=False
        

    # < Choose vacation name to request > #
    number_before_request=available_vacation()
    oneday=hours_set_from_time_card("allday")
    use_hour_unit= 0
    result_select_vc=False
    total_vc=total_vacation()
    list_vc_use_hour_unit=[]
    infor_vacation=check_use_hour_unit_half_day(total_vc)
    

    if total_vc==0:
        msg_xlsx("p","fu",re_vc,"-No vacation to request vacation ")
    else:
        for i in range(1,len(infor_vacation)):
            if infor_vacation[i]["use_hour_unit"]== True:
                list_vc_use_hour_unit.append(infor_vacation[i])
                use_hour_unit= use_hour_unit+1
        if  use_hour_unit == 0:
            msg_xlsx("p","fu",re_vc, "-No vacation use hour unit <Pass>")
        else:
            hour_selected=select_hour_use_hour_unit()
            if hour_selected != False :
                vacation_request["vc_date"]=str(vacation_request["vc_date"])+ hour_selected
                hour_use=hour_used(use_hour_unit,"hour_unit")
                result_select_vc=select_vacation_use_hour_unit_half_day(total_vc,list_vc_use_hour_unit,hour_use,"hour-unit")
                if  result_select_vc != False :
                    msg_xlsx("p","fu",re_vc,"-Select Vacation to request <Pass>")
                    msg("p", "  +Vacation name  : " + result_select_vc + "<Pass>" )
                    
                    driver.find_element_by_xpath(data["rq_vc"]["hour_unit"]).click()
                    time.sleep(3)
                    driver.find_element_by_xpath(data["rq_vc"]["hour_start"]).click()
                    driver.find_element_by_xpath(data["rq_vc"]["sl_hour_start"]).click()
                    time.sleep(3)
                    
                    driver.find_element_by_xpath(data["rq_vc"]["hour_end"]).click()
                    driver.find_element_by_xpath(data["rq_vc"]["sl_hour_end"]).click()
                    
                    
                    vacation_request["vc_date"]=driver.find_element_by_xpath(data["rq_vc"]["selected_date"]).text
                    
                else:
                    msg_xlsx("p","fu",re_vc, "-The number of days is not enough to request by hours unit <Pass>")
   
    
    # < Send request vacation > #
    if result_select_approver == bool(True) and result_date == True :
        
        click_on_request_button()
        result_request=check_result_request()
        if result_request== "pass":
            msg_xlsx("p","fu",re_vc,"-Request vacation <Pass>")
            check_created_request(vacation_request,"hour_unit",use_hour_unit,approver)
            # < Check number of days off after request vacation > #
            #number_after_request=available_vacation()
            #check_number_of_days_off(number_before_request,number_after_request,hour_use,result_select_vc,oneday,use_hour_unit)
        elif result_request== "fail":
            msg_xlsx("p","fu",re_vc,"-Can't request <Pass>")
        else:
            msg_xlsx("p","fu",re_vc, "-Conditions for request vacation are not valid <Pass>")
            msg("p", "-Msg :",result_request)

def sm_re_vc_request_vacation_consecutive(request_date,result_select_approver,approver):

    # [REQUEST VACATION : CONSECUTIVE VACATION] #

    result_date=True
    result_select_vc= False
    use_hour_unit= False
    vacation_request={"vc_name":"","vc_date":"","request_date":request_date,"status":"Request"}

    # Update status for request #
    if approver["approval_exception"] == True:
        vacation_request["status"]="Approved"

    # < Choose vacation name to request > #
    total_vc=total_vacation()
    number_before_request=available_vacation()
    oneday=hours_set_from_time_card("allday")
    infor_vacation=check_use_hour_unit_half_day(total_vc)
    
    
    # Check there are any vacations using hour unit => change the way to check the number of leave days #
    i=1
    while i<=total_vc:
        if infor_vacation[i]["use_hour_unit"]== True:
            use_hour_unit= True
            break
        i=i+1



    # < Choose date to request [go to my vacation to check used dates and select date to request vacation] > #
    vc_date=select_days_to_request_leave_for_vacation_consecutive()
    if vc_date != False:
        vacation_request["vc_date"]= str(vc_date[0])+"~" +str(vc_date[1])+"All day Off-All day Off"
    else:
        result_date=False

    # Check the remaining days of each vacation are enough to request #
    i=1
    while i<=total_vc:
        time.sleep(1)
        driver.find_element_by_css_selector(data["rq_vc"]["select_vacation"]).click()
        driver.find_element_by_xpath("//body/div[4]/div/div/div[" + str(i) +"]").click()
        vc_use_for_request = vacation_use_for_request()
        hour_use=2
        remain_days=vc_use_for_request["number_of_days"]
        remain_hours=vc_use_for_request["number_of_hours"]
        vc_name=vc_use_for_request["vacation_name"]
        # If vacation is other vacation can use this vacation to request #
        if float(remain_days)== 0 and float(remain_hours) == 0:
            result_select_vc= True
            vacation_request["vc_name"]=vc_name.replace(" ", "")
            msg("p", "-Select Vacation to request <Pass>")
            msg("p", "  +Vacation name : " +vc_name + "<Pass>" )
            break

        # If vacation is grant/regular , need to check there are enough days to request #
        else :
            if float(remain_days) >= hour_use :
                result_select_vc= True
                vacation_request["vc_name"]=vc_name.replace(" ", "")
                msg("p", "-Select Vacation to request <Pass>")
                msg("p", "  +Vacation name : " +vc_name + "<Pass>" )
                
                break 
        i=i+1
    # Vacation does not have enough days to choose #
    if result_select_vc== False:
        msg_xlsx("p","fu",re_vc,"-No vacation to request <Pass>")
    
    
    
    # < Send request vacation , if selected vacation and selected approver > #  
    if result_select_vc == bool(True) and result_select_approver  ==bool(True) and result_date==bool(True):
        driver.find_element_by_xpath(data["rq_vc"]["bt_request_be"]).click()
        driver.find_element_by_css_selector(data["rq_vc"]["bt_request_af"]).click()

        result_request=check_result_request()
        if result_request== "pass":
            msg_xlsx("p","fu",re_vc,"-Request vacation (Vacation Consecutive)  <Pass>")

            # Check created request and view detail request #
            check_created_request(vacation_request,"vacation_consecutive",use_hour_unit,approver)

            # < Check number of days off after request vacation > #
            number_after_request=available_vacation()
            check_number_of_days_off(number_before_request,number_after_request,hour_use,vc_name,oneday,use_hour_unit,"vacation_consecutive")

            # < Cancel Request and number of vacation is updated  > #
            sm_my_vc_cancel_request(oneday,use_hour_unit)
           

        elif result_request== "fail":
            msg_xlsx("p","fu",re_vc,"-Can't request (Vacation Consecutive) <Pass>")
        else:
            msg_xlsx("p","fu",re_vc,"-Conditions for request vacation are not valid (Vacation Consecutive) <Pass>")
            msg("p", "-Msg :",result_request)
    
def sm_my_vc_cancel_request(oneday,use_hour_unit):
    
    #[Cancel Request]#
    try:
        i=1
        check_number=False
        result_cancel=False
        result_find=False
        time_cancel=True
        list_status=["request"]
        cancelex=param_excel["cancel_request"]
        today= str(datetime.date.today()).replace(" ","")

        number_before_cancel=available_vacation()
        driver.find_element_by_link_text("My Vacation Status").click()
        time.sleep(3)
        rows=driver.find_elements_by_xpath(data["rq_vc"]["list_request"])
        total_request=total_data(rows)
        
        if is_Displayed(data["rq_vc"]["check_list_re"]) == bool(True) :
            msg_xlsx("p","fu",cancelex,"-No request to cancel request <Pass>")
        
        else:
            # Get all requests that can be used for cancel #
            time.sleep(3)
            list_request=driver.find_elements_by_xpath(data["rq_vc"]["list_request"])
            total_request=total_data(list_request)
            while i<= total_request:
                infor_request=info_request_list(i)
                if is_Displayed(xpath2(data["rq_vc"]["re_ic"],str(i-1),"')]")) == bool(True) : 
                    
                    # If vacation request is approved , check vacation date (> or = ) today => Can cancel #
                    if infor_request["status"] not in list_status :
                        time_cancel=time_comparison(infor_request["vacation_time"],today) 

                    if time_cancel== True :
                        result_find=True
                        status_before_cancel=infor_request["status"]
                        request_to_cancel=infor_request
                        driver.find_element_by_xpath(xpath2(data["rq_vc"]["re_ic"],str(i-1),"')]")).click()

                        if is_Displayed(data["rq_vc"]["bt_cancel_request"]) == bool(True) :  
                            msg("p", "-Click on cancel request icon <Pass>")
                            driver.find_element_by_xpath(data["rq_vc"]["bt_cancel_request"]).click()
                            time.sleep(1)

                            if is_Displayed(data["rq_vc"]["bt_cancel"]) == bool(False) : 
                                msg_xlsx("p","fu",cancelex,"-Cancel request <Pass>")
                                result_cancel=True
                            else:
                                msg_xlsx("f","fu",cancelex,"-Cancel request <Fail>")
                            break 
                        else:
                            msg_xlsx("f","fu",cancelex,"-Click on cancel request icon <Fail>")
                i=i+1 
            

            # If the request is canceled successfully, check the request has changed status #
            if result_cancel==True:
                i=1
                driver.find_element_by_link_text("My Vacation Status").click()
                while i<= total_request:
                    infor_request=info_request_list(i)
                    find_request_canceled=two_requests_are_the_same(request_to_cancel,infor_request)

                    if find_request_canceled== True:
                        if status_before_cancel=="Request" :
                            if infor_request["status"]== "Canceled":
                                msg_xlsx("p","fu",cancelex,"-Request'status change to Canceled  <Pass>")
                                check_number = True
                                break
                            else:
                                msg_xlsx("f","fu",cancelex,"-Request'status change to Canceled  <Fail>")
                                break
                        else:
                            # Status before is "Approved" ,"Approved[1/3],..."
                            if  status_before_cancel=="Approved" :
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,xpath3("tr",str(i),data["rq_vc"]["ic_detail"],i-1,data["rq_vc"]["ic_detail1"])))).click()
                                time.sleep(2)
                                list_approver=driver.find_elements_by_xpath(data["rq_vc"]["content_vc_approver"])
                                total_approver=total_data(list_approver)
                                if total_approver== 0:
                                    if infor_request["status"]== "Canceled":
                                        msg_xlsx("p","fu",cancelex,"-Request'status change to Canceled  <Pass>")
                                        check_number = True
                                        break
                                        
                                    else:
                                        msg_xlsx("f","fu",cancelex,"-Request'status change to Canceled  <Fail>")
                                        break

                            if infor_request["status"]== "User cancel":
                                msg_xlsx("p","fu",cancelex,"-Request'status change to User cancel  <Pass>")
                                break
                            else:
                                msg_xlsx("f","fu",cancelex,"-Request'status change to User cancel  <Fail>")
                                break
                        
                    i=i+1 
            if check_number == True :
                hours_used=float(re.search(r'\d+',infor_request["use"]).group(0)) 
                vc_name=infor_request["vacation_name"].replace("\n","")
                vc_name=vc_name[None: int(vc_name.rfind("~"))] + " ~ " +vc_name[ int(vc_name.rfind("~"))+1:None]
                number_after_cancel=available_vacation()
                hours=infor_request["use"].strip()
                
                if hours =="1D" or hours =="2D":
                    type_request = "all_day"
                elif hours =="0.5D" or hours =="4H":
                    type_request ="half_day"
                else:
                    type_request ="hour_unit"

                check_number_of_days_cancel(number_before_cancel,number_after_cancel,hours_used,vc_name,oneday,use_hour_unit,type_request)
            

            if result_find== False:
                msg_xlsx("p","fu",cancelex,"-No request to cancel request <Pass>")
    except:
        driver.find_element_by_link_text("My Vacation Status").click()

def submenu_request_vacation():

    msg("n", "SUB MENU : REQUEST VACATION ")
    msg("n", "I.REQUEST VACATION")
    requestex=param_excel["request"]
    request_date=str(datetime.date.today())
    driver.find_element_by_link_text("Request Vacation").click()
        
    msg("n", "Select approver")
    result_select_approver=False
    approver=select_approver()
    if approver["result_approver"] == True:
        result_select_approver= True
    else:
        if approver["approval_line"]==True:
            result_select_approver= True
        if approver["approval_exception"]== True:
            result_select_approver= True

    driver.find_element_by_link_text("Request Vacation").click()
    total_vc=total_vacation()
    
    if total_vc== 0 :
        msg_xlsx("p","fu",requestex,"-No vacation to request <Pass>")

    else:
        '''
        msg("n", "Request Vacation : All Day ")
        sm_re_vc_request_vacation_all_day(request_date,result_select_approver,approver)
        
        
        msg("n", "Request Vacation : Consecutive Vacation ")
        sm_re_vc_request_vacation_consecutive(request_date,result_select_approver,approver)
       
        '''
        msg("n", "REQUEST VACATION : HALF DAY (AM) ")
        sm_re_vc_request_vacation_half_am(request_date,result_select_approver,approver)

        '''
        msg("n", "REQUEST VACATION : HALF DAY (PM)")
        sm_re_vc_request_vacation_half_pm(request_date,result_select_approver,approver)
        '''

        #msg("n", "REQUEST VACATION : HOUR UNIT")
        #sm_re_vc_request_vacation_hour_unit(request_date,result_select_approver,approver)

'''
# linux #
def request():   
    result_access_menu_vacation =access_menu_vacation()
    if result_access_menu_vacation ==  True :
        submenu_request_vacation()
'''

# Window #
def request(domain):   
    login(domain)
    result_access_menu_vacation =access_menu_vacation(domain)
    if result_access_menu_vacation ==  True :
        submenu_request_vacation()
       

    

    
    