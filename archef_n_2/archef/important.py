import pandas as pd
from unidecode import unidecode

data = pd.read_excel (r'C:\Users\h\Desktop\New\dummy.xlsx') 

# read both main id and code 
df_id = pd.DataFrame(data, columns= ['Id'])
df_code = pd.DataFrame(data, columns= ['Code'])

lst_id = df_id.values.tolist()
lst_code = df_code.values.tolist()

# convert the data fram to a list 
codes_new = pd.read_excel (r'C:\Users\h\Desktop\New\codes_new.xlsx') 
df_code_new = pd.DataFrame(codes_new, columns= ['codes'])
lst_code_new = df_code_new.values.tolist()

# the required id 
Id_new_1d = [None]*len(lst_code_new )
#searched codes list 
searched = []


lst_id_1d=[]
lst_code_1d=[]


#convert main id and code to  a 1d list 
for i in range(len(lst_id)):
    lst_id_1d.append(lst_id[i][0])
    lst_code_1d.append(lst_code[i][0])



#convert secondary code to a 1d list 
lst_code_new_1d=[]
for i in range(len(lst_code_new)):
    lst_code_new_1d.append(lst_code_new[i][0])
    lst_code_new_1d[i] =unidecode(lst_code_new_1d[i][0:3]) +lst_code_new_1d[i][3]
    
    
    


   
#helper function     
def get_index(code):
    
    indeces = []
    for i in range(len(lst_code_new_1d)):
        if lst_code_new_1d[i] == code :
            indeces.append(i)

    return indeces



def search_list(code):
    for i in range(len(searched)):
        if code == searched[i]:
            return True
    return False



for i in range(len(lst_code_new_1d)):
    code = lst_code_new_1d[i]
    #skip this code as it has been already converted 
   # if search_list(code):
   #     continue 
    
    #if not save it to searched 
    searched.append(code)
    try :
        index = lst_code_1d.index(code)
        req_id = lst_id_1d[index]
    except:
        req_id = 0
    #get all indeices of this code in the new_code all at once 
   # indeces = get_index(code)
    
    #for z in range(len(indeces)):
     #   Id_new_1d[indeces[z]] = int( req_id)
     
    Id_new_1d[i] = int( req_id)
        

    
    
#print result 
for i in range(len(Id_new_1d)):
    if Id_new_1d[i] != 0:
        print("code:%s at index  %d and id:  %d  " %(lst_code_new_1d[i],i, Id_new_1d[i]))
    
    
    
    
    
    
    
# write data to an excel sheet 

# Writing to an excel  
# sheet using Python 
#import xlwt 
from xlwt import Workbook 
  
# Workbook is created 
wb = Workbook() 
  
# add_sheet is used to create sheet. 
sheet1 = wb.add_sheet('Sheet 1') 

sheet1.write(0, 0, 'New_Id') 

for i in range(1,len(Id_new_1d)+1):
    sheet1.write(i, 0,Id_new_1d[i-1] ) 
    
    

wb.save('example.xls') 
 
        
    
    
 
