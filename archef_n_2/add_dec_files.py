
#configure setting for import files
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archef_n_2.settings')
import django
django.setup()
from archef import models
#
i=0
for decision in models.Decision.objects.all():
     if i % 100 == 0:
        print("")
     if decision.dec_year == 2017:
            path ='/' + str(decision.dec_year) + '/' + str(decision.dec_num)+ ".jpg"
        
     elif decision.dec_year == 2019 and (decision.dec_num >= 656 and decision.dec_num <= 1705)
        path ='/' + str(decision.dec_year) + '/' + ( '0' * (4-len( str(decision.dec_num) ) ) ) + str(decision.dec_num)+".bmp":
     else :
            path ='/' + str(decision.dec_year) + '/' + ( '0' * (4-len( str(decision.dec_num) ) ) ) + str(decision.dec_num)+".jpg"
        
     decision.decision_file = path
     decision.save()
     i +=1


i =0
for decision in models.Decision.objects.all():
    if decision.dec_year == 2019 and (decision.dec_num >= 656 and decision.dec_num <= 1705):
        path ='/' + str(decision.dec_year) + '/' + ( '0' * (4-len( str(decision.dec_num) ) ) ) + str(decision.dec_num)+".bmp"
        decision.decision_file = path
        decision.save()
        i +=1
        
print("2019 dec between 656 and 1705 are %d" %(i))

        