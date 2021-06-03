import pandas as pd

#configure setting for import files
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archef_n_2.settings')
import django
django.setup()
from archef import models


data = pd.read_excel(r'F:\khaled_nozom\archef_n_2\archef_db\new_moalid\moalid_2004.xlsx')


print("Done reading excel sheet")
# read full sheet
#year = pd.DataFrame(data, columns= ['MILAD'])
markaz= pd.DataFrame(data, columns= ['C_MAR'])
mosalsal = pd.DataFrame(data, columns= ['MOSALSAL'])
nat_id = pd.DataFrame(data, columns= ['KAWMY_NUM'])
name = pd.DataFrame(data, columns= ['SH_NAME'])

print("Done reading excel sheet Columns")

#convert data from pandas frame to a list
#year = year.values.tolist()
markaz = markaz.values.tolist()
mosalsal = mosalsal.values.tolist()
nat_id = nat_id.values.tolist()
name = name.values.tolist()

dup_counter = 0
import math
length = len(markaz)
print("Done converting pandas data frames to lists with %d shabs "%(length))
for i in range(length):
    #s_year =  int(year[i][0]) if not math.isnan(year[i][0])  else 0
    s_year = 2004
    s_markaz =int (markaz[i][0]) if not math.isnan(markaz[i][0]) else 0
    s_mosalsal =int (mosalsal[i][0]) if not math.isnan(mosalsal[i][0]) else 0
    s_nat_id = int(nat_id[i][0]) if not math.isnan(nat_id[i][0]) else 0
    try:
        s_name = name[i][0] if not math.isnan(name[i][0]) else ''
    except :
        s_name = name[i][0]
    #print(str(s_year)+" "+str(s_markaz)+" "+str(s_mosalsal)+" "+str(s_nat_id)+" "+str(s_name)+" ")
    shab = models.Shab(year = s_year, markaz = s_markaz,mosalsal =  s_mosalsal,nat_id =  s_nat_id,name = s_name)
    shab.save()
    # if len (models.Shab.objects.filter(year=s_year ,  markaz = s_markaz,mosalsal =  s_mosalsal)) >= 1:
    #     print("current dup counter:%d" %(dup_counter))
    #     dup_counter += 1
    #     continue 

    # else:
    #     print("Remaing shabs %d "%(length-i))
    #     shab.save()
    if (i%1000) == 0:
        print("remaining shabs in the excel file %d from the total: %d"%(length-i, length))
print("Done storing all shabs data which are %d "%(length)) 

