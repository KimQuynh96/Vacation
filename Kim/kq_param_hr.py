import time, json,datetime
from datetime import date
date_time=str( datetime.date.today()).replace("-",":")+","+ str(datetime.datetime.now().time())[None:str(datetime.datetime.now().time()).rfind(".")]
print(date_time)
def log():
    par={
        "login":{"menu":"Vacation","submenu":"Log In","testcase":"Log in","status":"Pass","description":"Login successful","date":date_time,"tester":"Kim Quynh"},
    }
    return json.dumps(par)

def submenu_my_vacation():
    par={
        "sl_org":{"menu":"Vacation","submenu":"My Vacation","testcase":"Select user from Org","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "search":{"menu":"Vacation","submenu":"My Vacation","testcase":"Search","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_re_settlement":{"menu":"Vacation","submenu":"Request Settlement","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "submenu_re_settle":{"menu":"Vacation","submenu":"Request Settlement","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_infor_my":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "submenu_view":{"menu":"Vacation","submenu":"View CC","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "submenu_schedule":{"menu":"Vacation","submenu":"Vacation Schedule","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "submenu_my":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "cancel_request":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"Cancel Request","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "re_ad":{"menu":"Vacation","submenu":"My Vacation","testcase":"Request Vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "re_detail":{"menu":"Vacation","submenu":"My Vacation","testcase":"View Detail ","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "number":{"menu":"Vacation","submenu":"My Vacation","testcase":"Number of days","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "filter1":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"Filter by status","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "filter2":{"menu":"Vacation","submenu":"View CC","testcase":"Filter by status","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "submenu_depart_vc":{"menu":"Vacation","submenu":"My Dept Vacation","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "detail_history":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"View Detail ","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "detail_my_depart":{"menu":"Vacation","submenu":"My Dept Vacation","testcase":"View Detail ","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "detail_cc":{"menu":"Vacation","submenu":"View CC","testcase":"View Detail ","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "delete_request":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"Delete Request","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "request":{"menu":"Vacation","submenu":"My Vacation Status","testcase":"Request vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},

    }
    return json.dumps(par)

def submenu_admin():
    par={
        "menu":{"menu":"Vacation","submenu":"Menu Vacation","testcase":"Access Menu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_vc":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "create_vc":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Create Vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_mn":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "manager":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Add Manager","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "modify_manager":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Modify Permission","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "delete_manager":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Delete Manager","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "basic":{"menu":"Vacation","submenu":"Basic Settings","testcase":"Approval Exception","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "arbitrary_decision":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Arbitrary Decision Setting","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_ap_setting":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_bc":{"menu":"Vacation","submenu":"Basic Settings","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_create_vc":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_mn_his":{"menu":"Vacation","submenu":"Manager History","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "permiss":{"menu":"Vacation","submenu":"Admin Settings","testcase":"Permission with sub menu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "delete_vc":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Delete vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "filter_type":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Filter","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "use_sett":{"menu":"Vacation","submenu":"Basic Settings","testcase":"Use Settlement","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "use_hour_un":{"menu":"Vacation","submenu":"Basic Settings","testcase":"Use Hour unit","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "use_vc_schedule":{"menu":"Vacation","submenu":"Basic Settings","testcase":"Use vacation schedule","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "detail_vc":{"menu":"Vacation","submenu":"Create Vacation","testcase":"View detail vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_detail":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "delete_ad":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Delete Arbitrary Decision ","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "delete_ax":{"menu":"Vacation","submenu":"Basic Settings","testcase":"Delete Approval Exception","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "Search_vc":{"menu":"Vacation","submenu":"Create Vacation","testcase":"Search","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "search_manager":{"menu":"Vacation","submenu":"Manager Settings","testcase":"Search","status":"","description":"","date":date_time,"tester":"Kim Quynh"},

    }
    return json.dumps(par)

def submenu_manager():
    par={
        "vc_approve":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Vacation Approve","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "vc_reject":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Vacation Reject","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_vc_approve":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "delete":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Delete Request","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "vc_cancel":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Vacation Cancel","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "vc_approve_cancel":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Approve Cancel","status":"","description":"","date":date_time,"tester":"Kim Quynh"},

    }
    return json.dumps(par)

def submenu_manager_pro():

    par={
        "tab_vc_approve":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_vc_adjust":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_vc_approve":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_vc_peruser":{"menu":"Vacation","submenu":"Vacation Per User","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_vc_adjust":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "grant":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Grant Vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "sub_menu_settlement":{"menu":"Vacation","submenu":"Settlement Management","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_vc_settlement":{"menu":"Vacation","submenu":"Settlement Management","testcase":"Access Tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "view_detail_request":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"View detail  ","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "adjust":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Adjust Vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "register":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Register Usage History","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "search":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Search","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "filter1":{"menu":"Vacation","submenu":"Vacation Approve","testcase":"Filter by Status","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "org":{"menu":"Vacation","submenu":"Vacation Adjust","testcase":"Select user from org","status":"","description":"","date":date_time,"tester":"Kim Quynh"},

    }
    return json.dumps(par)

def time_card():
    par={
        "sub_calendar":{"menu":"Time Card","submenu":"TimeSheets","testcase":"Access Submenu","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "tab_calendar":{"menu":"Time Card","submenu":"TimeSheets","testcase":"Access tab","status":"","description":"","date":date_time,"tester":"Kim Quynh"},
        "vacation":{"menu":"Time Card","submenu":"TimeSheets","testcase":"Vacation","status":"","description":"","date":date_time,"tester":"Kim Quynh"},

    }
    return json.dumps(par)