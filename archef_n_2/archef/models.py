from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

#import built in user model
from django.contrib.auth.models import User
#

## create our models
#first one is the part model




class Part(models.Model):
    name = models.CharField(max_length = 64)


    def __str__(self):
        return self.name




### second models
#2- user model

class ArchefUser(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_main_id = models.IntegerField(primary_key = True , validators=[MinValueValidator(1)])
    part = models.ForeignKey(Part, on_delete=models.CASCADE)


    def __str__(self):
        return  "user name : " + self.user.username + " , part: "+ self.part.name





### 3- model  --  decision

import datetime
class Decision(models.Model):
    #id = models.AutoField(primary_key=True)
    dec_num = models.IntegerField( )
    dec_year = models.IntegerField( validators=[MaxValueValidator(2100), MinValueValidator(1900)])
    dec_date = models.DateField(default = datetime.date.today)
    # user that  creates and regisers the decision
    user = models.ForeignKey(ArchefUser, on_delete=models.SET_NULL, null= True)
    related_part = models.CharField(max_length=64, default="nozom")
    decision_file = models.FileField(upload_to='%Y/',  null =True  )
    #decision_file = models.FileField(upload_to='files/',  null =True  )

    def __str__(self):
        return "decision number: "+str(self.dec_num)  + " realted part is : "+ self.related_part




##4- model ---   decsion_record

class DecisionRecord(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField(validators=[MaxValueValidator(2100), MinValueValidator(1900)])
    markaz = models.IntegerField()
    mosalsal = models.IntegerField()
    name = models.CharField(max_length = 256)
    national_num = models.IntegerField(  validators=[MaxValueValidator(40000000000000), MinValueValidator(20000000000000)])
    #national_num = models.CharField(primary_key=True, max_length=14, validators=[RegexValidator(r'^\d{1,10}$')])
    change_type = models.CharField(max_length=128)
    #many to one relationship
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)


    def __str__(self):
        return "name: "+ self.name  + ", change_type : "+self.change_type +", (dec num, dec year) --->> ("+str(self.decision.dec_num) + ", "+ str(self.decision.dec_year) +")"





class Shab(models.Model):
    year = models.PositiveIntegerField()
    markaz = models.PositiveIntegerField()
    mosalsal = models.PositiveIntegerField()
    nat_id = models.PositiveIntegerField(null = True)
    name = models.CharField(max_length = 264, null = True)


    def __str__(self):
         return "name: "+ self.name + ", nat_id: "+ str(self.nat_id)
