

import pandas as pd

#configure setting for import files
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archef_n_2.settings')
import django
django.setup()
from archef import models

####################################
##  STEP ONE : READ excel sheets
####################################
#decisons excel shhet
data = pd.read_excel (r'F:\khaled_nozom\archef_n_2\archef_db\data_11\sheet.xlsx')

#parts excel sheet
parts = pd.read_excel (r'F:\khaled_nozom\archef_n_2\archef_db\data_11\parts.xlsx')


#read k_change table id, name
k_change = pd.read_excel (r'F:\khaled_nozom\archef_n_2\archef_db\data_11\k_change.xlsx')

#read changes
changes = pd.read_excel (r'F:\khaled_nozom\archef_n_2\archef_db\data_11\changes.xlsx')

###############################################################################################


####################################
##  STEP ONE : EXtract Relevant tables
####################################
# read full decisions sheet
dec_num = pd.DataFrame(data, columns= ['dec_num'])
dec_year= pd.DataFrame(data, columns= ['dec_year'])
dec_date = pd.DataFrame(data, columns= ['dec_date'])
related_part_id = pd.DataFrame(data, columns= ['related_part'])
dec_id =  pd.DataFrame(data, columns= ['sheet_change_id'])


#read parts sheet
part_id = pd.DataFrame(parts, columns= ['id'])
part_name = pd.DataFrame(parts, columns= ['part'])


#k_change sheet
k_change_id = pd.DataFrame(k_change, columns= ['id'])
k_change_name = pd.DataFrame(k_change, columns= ['k_change'])


#changes sheet
year = pd.DataFrame(changes, columns= ['milad'])
markaz= pd.DataFrame(changes, columns= ['c_mar'])
mosalsal = pd.DataFrame(changes, columns= ['mosalsal'])
related_dec_id = pd.DataFrame(changes, columns= ['id_sheet_change'])
related_k_change_id = pd.DataFrame(changes, columns= ['k_change'])


###################################################################################3
#----------------------------------------------------------------------------
####################################################################################3

####################################
##  STEP Three : Convert pandas data frames from step one to  a 2-d lists
####################################

#convert data from pandas frame to a list
#decision table
dec_num = dec_num.values.tolist()
dec_year = dec_year.values.tolist()
dec_date = dec_date.values.tolist()
related_part_id = related_part_id.values.tolist()
dec_id = dec_id.values.tolist()


#changes table
year = year.values.tolist()
markaz = markaz.values.tolist()
mosalsal = mosalsal.values.tolist()
related_dec_id = related_dec_id.values.tolist()
related_k_change_id = related_k_change_id.values.tolist()

#####
# parts table
part_id = part_id.values.tolist()
part_name = part_name.values.tolist()

#k_change table
k_change_id = k_change_id.values.tolist()
k_change_name = k_change_name.values.tolist()


###################################################################################3
#----------------------------------------------------------------------------
####################################################################################3

####################################
##  STEP four : convert 2-d lists from step Three  to a 1-d lists  just parts and k_change
####################################
part_id_1d =[]
part_name_1d = []
for i in range(len(part_id)):
    part_id_1d.append(part_id[i][0])
    part_name_1d.append(part_name[i][0])

#####
k_change_id_1d = []
k_change_name_1d = []
for i in range(len(k_change_id)):
    k_change_id_1d.append(k_change_id[i][0])
    k_change_name_1d.append(k_change_name[i][0])






###################################################################################3
#----------------------------------------------------------------------------
####################################################################################3

####################################
##  STEP five : convert 2-d lists from step Three  to a 1-d lists  just parts and k_change
####################################

#convert date from ms to actual year/month/day
#, ids from a 2-d list to a 1-d
#, year and dec_num to a 1-d list
dec_date_1d = []
dec_date_py = []
dec_id_1d = []
dec_num_1d = []
dec_year_1d = []
import datetime
import math
length_decisions = len(dec_date)
for i in range(length_decisions):
    try :
        dec_date_1d.append( (dec_date[i][0] / 1000000) if ( (not math.isnan(dec_date[i][0]))) else  datetime.datetime.now().timestamp() * 1000)
    except :
        dec_date_1d.append(datetime.datetime.now().timestamp() * 1000)
    #print(dec_date_1d[i])
    #dec_date_1d.append(dec_date[i][0])
    dec_date_py.append(datetime.datetime.fromtimestamp(dec_date_1d[i]/1000.0))
    #print(str(dec_date_py[i].date()) +" i:"+str(i))
    try :
        dec_id_1d.append( int(dec_id[i][0])  if not math.isnan(dec_id[i][0] ) else  0)
    except :
        dec_id_1d.append(0)
    #dates = pd.to_datetime(dec_date_1d, unit='ms').to_pydatetime()
    #print(dates)
    try:
        dec_num_1d.append(int(dec_num[i][0]) if not math.isnan(dec_num[i][0])  else 1)
    except :
        dec_num_1d.append(1)
    try:
        dec_year_1d.append(int (dec_year[i][0]) if not math.isnan(dec_year[i][0]) else 2015)
    except :
        dec_year_1d.append( 2015)



###################################################################################3
#----------------------------------------------------------------------------
####################################################################################3

####################################
##  STEP six : SAVE UNIQUE DECISIONS TO THE DB
####################################

#save unique decisons to the db
#
decision_file = None
user = models.ArchefUser.objects.filter(user_main_id = 3324).first()
dup_counter_d = 0
for i in range(length_decisions):

    print("decisions counter:%d , remaing decisions:%d" %(i, length_decisions-i))
    try:
        s_related_part_id = int(related_part_id[i][0]) if not math.isnan(related_part_id[i][0]) else 9
    except :
        s_related_part_id= 9

    idx = part_id_1d.index(s_related_part_id)
    s_part_name = part_name_1d[idx]
    s_dec_num = dec_num_1d[i]
    s_dec_year = dec_year_1d[i]
    s_dec_date = dec_date_py[i]
    decision = models.Decision(dec_num = s_dec_num, dec_year=s_dec_year, dec_date= s_dec_date, decision_file=decision_file,
                                user = user, related_part = s_part_name)

    if len (models.Decision.objects.filter(dec_num =decision.dec_num , dec_year = decision.dec_year)) >= 1:
        #print("duplicate decision  dec num %d dec_year %d" %(s_dec_num, s_dec_year))
        dup_counter_d += 1
        continue
    else:
        if decision.dec_year == 2017:
            path ='/' + str(decision.dec_year) + '/' + str(decision.dec_num)+ ".jpg"
        
        elif decision.dec_year == 2019 and (decision.dec_num >= 656 and decision.dec_num <= 1705):
            path ='/' + str(decision.dec_year) + '/' + ( '0' * (4-len( str(decision.dec_num) ) ) ) + str(decision.dec_num)+".bmp"
        else :
            path ='/' + str(decision.dec_year) + '/' + ( '0' * (4-len( str(decision.dec_num) ) ) ) + str(decision.dec_num)+".jpg"
        
        decision.decision_file = path
        decision.save()
       
    #s_part_id = int(part_id[i][0]) if not math.isnan(part_id[i][0]) else 0
    #try:
    #    s_part_name = part_name[i][0] if not math.isnan(part_name[i][0]) else 'part_name'
    #except :
    #    s_part_name= part_name[i][0]
    #print(str(s_dec_num)+" "+str(s_dec_year)+" "+str(s_dec_date)+" "+str(s_related_part_id)+" "+str(s_part_name)+" ")
    #print(str(s_dec_num)+" "+str(s_dec_year)+" "+str(s_dec_date)+" "+str(s_related_part_id)+" ")
    #shab = models.Shab(year = s_year, markaz = s_markaz,mosalsal =  s_mosalsal,nat_id =  s_nat_id,name = s_name)
    #shab.save()
    #print(shab)




###################################################################################3
#----------------------------------------------------------------------------
####################################################################################3

####################################
##  STEP Seven : SAVE UNIQUE DECISION RECORDS  TO THEIR RELEVANT DECISIONs in the  DB
####################################
dup_counter_r = 0
length_records = len(year)
for i in range(length_records):
    print("records counter:%d , remaing records:%d" %(i, length_records-i))
    try:
        s_year =  int(year[i][0]) if not math.isnan(year[i][0])  else 0
    except:
        s_year = 0
    try:
        s_markaz =int (markaz[i][0]) if not math.isnan(markaz[i][0]) else 0
    except:
        s_markaz = 0
    try:
        s_mosalsal =int (mosalsal[i][0]) if not math.isnan(mosalsal[i][0]) else 0
    except:
        s_mosalsal = 0

    #get change type value
    try:
        s_k_change = int (related_k_change_id[i][0]) if not math.isnan(related_k_change_id[i][0]) else 0
        k_idx =k_change_id_1d.index(s_k_change)
        s_change_type =k_change_name_1d[k_idx]
    except:
        s_change_type = k_change_name_1d[0]


    shab = models.Shab.objects.filter(year = s_year, markaz = s_markaz,mosalsal =  s_mosalsal).first()
    #if there is a shab in our db register it
    name=""
    national_num=0
    #if we found a shab data
    if shab:
        #print(shab)
        name = shab.name
        national_num = shab.nat_id

    #get related decision

    try:
        s_dec_id = int (related_dec_id[i][0]) if not math.isnan(related_dec_id[i][0]) else 0
        #print("s_dec_id %d" %(s_dec_id))
        dec_idx = dec_id_1d.index(s_dec_id)
        s_dec_year = dec_year_1d[dec_idx]
        s_dec_num = dec_num_1d[dec_idx]
    except :
        #print("error getting dec data id=%d  idx: %d  year:%d  num:%d " %(s_dec_id, dec_idx, s_dec_year, s_dec_num))
        dup_counter_r += 1
        #print("error getting dec data id=%d " %(s_dec_id))
        continue

    decision = models.Decision.objects.filter(dec_num = s_dec_num, dec_year = s_dec_year).first()
        #if you find a related decision then save it else skip
    if decision:
            record = models.DecisionRecord(year = s_year,markaz= s_markaz,mosalsal= s_mosalsal, name = name,
                                            national_num= national_num, change_type= s_change_type, decision=decision )
            #see if this record already exists in the current decision
            if len (models.DecisionRecord.objects.filter(decision=decision , year = s_year, markaz = s_markaz,mosalsal =  s_mosalsal)) >= 1:
                #print(str(national_num))
                #raise ValueError ("هذا الشاب تم تسجيله بالفعل فى القرار ")
                #print("duplicate decision record for %d  %d %d \nIN dec num %d dec_year %d " %(s_year,s_markaz ,s_mosalsal,  s_dec_num, s_dec_year))
                dup_counter_r += 1
                continue

            else:
                record.save()
    #no decsion found
    else:
            #print("not decision found")
            continue



print("total decisions num: %d  , saved num: %d ,  duplicated dec. num: %d " %(length_decisions, length_decisions - dup_counter_d, dup_counter_d))

print("total records num: %d  , saved num: %d ,  duplicated records num: %d " %(length_records, length_records - dup_counter_r, dup_counter_r))

print("total num of decisions in the db until now is %d"%(len(models.Decision.objects.all() ) ) )
print("total num of decision records in the db until now is %d"%(len(models.DecisionRecord.objects.all() ) ) )