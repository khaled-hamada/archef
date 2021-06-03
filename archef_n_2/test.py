
import pandas as pd


#
# #parts excel sheet
# parts = pd.read_excel (r'E:\python\SaleWebDesign.com-Python-Django\SaleWebDesign.com-Python-Django\My_Projects\archef_n_2\archef_db\parts.xlsx')
#
#
# #read k_change table id, name
# k_change = pd.read_excel (r'E:\python\SaleWebDesign.com-Python-Django\SaleWebDesign.com-Python-Django\My_Projects\archef_n_2\archef_db\k_change.xlsx')
#
#
# #read parts sheet
# part_id = pd.DataFrame(parts, columns= ['id'])
# part_name = pd.DataFrame(parts, columns= ['part'])
#
#
# #k_change sheet
# k_change_id = pd.DataFrame(k_change, columns= ['id'])
# k_change_name = pd.DataFrame(k_change, columns= ['k_change'])
#
#
#
# #####
# # parts table
# part_id = part_id.values.tolist()
# part_name = part_name.values.tolist()
#
# #k_change table
# k_change_id = k_change_id.values.tolist()
# k_change_name = k_change_name.values.tolist()
#
# part_id_1d =[]
# part_name_1d = []
# for i in range(len(part_id)):
#     part_id_1d.append(part_id[i][0])
#     part_name_1d.append(part_name[i][0])
#
# #####
# k_change_id_1d = []
# k_change_name_1d = []
# for i in range(len(k_change_id)):
#     k_change_id_1d.append(k_change_id[i][0])
#     k_change_name_1d.append(k_change_name[i][0])
#
#
#
#
# for i in range(len(k_change_id_1d)):
#     print(str(k_change_id_1d[i])+" : "+ k_change_name_1d[i] )
#
#
# # print(part_id_1d)
# # print(part_name_1d)
# # print(k_change_id_1d)
# # print(k_change_name_1d)
#

data = pd.read_excel (r'E:\python\SaleWebDesign.com-Python-Django\SaleWebDesign.com-Python-Django\My_Projects\archef_n_2\archef_db\sheet.xlsx')
dec_date = pd.DataFrame(data, columns= ['dec_date'])
#dates = pd.to_datetime(dec_date, unit='ms').to_pydatetime()
dec_date = dec_date.values.tolist()
dec_date_1d = []
dec_date_py = []

import datetime
import math
length = len(dec_date)
for i in range(length):
    try :
        dec_date_1d.append( (dec_date[i][0] / 1000000) if ( (not math.isnan(dec_date[i][0]))) else  datetime.datetime.now().timestamp() * 1000)
    except :
        dec_date_1d.append(datetime.datetime.now().timestamp() * 1000)
    #print(dec_date_1d[i])
    #dec_date_1d.append(dec_date[i][0])
    dec_date_py.append(datetime.datetime.fromtimestamp(dec_date_1d[i]/1000.0))
    print(str(dec_date_py[i].date()) +" i:"+str(i))

    #dates = pd.to_datetime(dec_date_1d, unit='ms').to_pydatetime()
    #print(dates)
