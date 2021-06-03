from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.

#authentication functions
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth.decorators import login_required
from   datetime import datetime, date


# import our database tables
from archef import  models
# from typing import Final




#global user variable
#cur_logged_user = models.ArchefUser()

def user_login(request):
    failed=0
    models.Shab.objects.all().delete()
    print("done models.Shab.all().delete() ")
    models.Decision.objects.all().delete()
    print("done models.Decision.all().delete() ")
    models.DecisionRecord.objects.all().delete()
    print("done models.DecisionRecord.all().delete() ")
   
    context={}
    if request.method == 'POST':

        #get user data and authenticate him
        user_main_id = request.POST['user_name']
        password = request.POST['user_password']
        #global cur_logged_user
        #cur_logged_user = models.ArchefUser.objects.filter(pk = user_main_id).first()
        cur_logged_user = models.ArchefUser.objects.filter(pk = user_main_id).first()
        #print( str(cur_logged_user))
        if cur_logged_user:
            user = authenticate( username= cur_logged_user.user.username, password = password)
        #print("user_id is: " + user_name)
        #print("user_id is: " + password)
        #print("user: " + str(user))
        # if a valid user loged in
            if user:
                if user.is_active:
                    login(request, user)
                    print("user {} is logged in the system at {}".format(request.user.username, str(datetime.now())))
                    return  HttpResponseRedirect(reverse('archef:start_page'))
                else:
                    print("user account is disabled")
            else:
                failed =1
        else:
           print("not authorized user is trying to log in the system")
           failed =1
        #    context = {'failed' : failed}
        #    return render(request, 'archef/user_login.html', context = context)

    context = {'failed' : failed}
    return render(request,'archef/user_login.html',  context = context)







@login_required
def start_page(request):
        return render(request,'archef/start_page.html')



@login_required
def edit(request, record_id):
        success = 0
        record = models.DecisionRecord.objects.filter(id = record_id).last()
        decision_id = models.Decision.objects.filter(id = record.decision.id).last().id

        if request.method == 'POST' and has_right_to_edit(request, decision_id):
            #print(decision)
            year = request.POST['year']
            markaz = request.POST['markaz']
            mosalsal = request.POST['mosalsal']
            name = request.POST['m_name']
            national_num= request.POST['national_num']
            change_type = request.POST['change_type']
            ### errors due to chabs change their old data by moving to other gorvernorants
            shab_old = models.Shab.objects.filter(year = year, markaz=markaz, mosalsal = mosalsal).first()
            shab_new = models.Shab(year = year,markaz = markaz, mosalsal = mosalsal, name =name, nat_id=national_num )
            #shab_new.save()
            if shab_old :
                    shab_old.delete()
                    shab_new.save()


            ## update record
            models.DecisionRecord.objects.filter(id = record_id).update(year = year,markaz= markaz,mosalsal= mosalsal, name = name,
                                            national_num= national_num, change_type= change_type )

            success = 1
            record = models.DecisionRecord.objects.filter(id = record_id).last()
            decision_id = models.Decision.objects.filter(id = record.decision.id).last().id
            url = 'archef:edit_redirect'
            # url = reverse(url)
            return redirect(url,decision_id)

        record = models.DecisionRecord.objects.filter(id = record_id).first()
        #print('Record data', str(record))
        context = {
            'record':record,
            'success':success,
        }
        return render(request,'archef/edit.html', context = context)



@login_required
def delete(request, record_id):

        record = models.DecisionRecord.objects.filter(id = record_id).last()
        decision = models.Decision.objects.filter(id = record.decision.id).last()

        cur_user = User.objects.filter(username = request.user.username).first()
        cur_user_id = models.ArchefUser.objects.filter(user = cur_user).first().user_main_id
        dec_user_id =decision.user.user_main_id

        if has_right_to_edit(request, decision.id):
            record.delete()


        url = 'archef:edit_redirect'
        # url = reverse(url)
        return redirect(url,decision.id)


def has_right_to_edit(request , decision_id):
        cur_user = User.objects.filter(username = request.user.username).first()
        cur_user_id = models.ArchefUser.objects.filter(user = cur_user).first().user_main_id
        dec_user_id =decision.user.user_main_id

        if dec_user_id == cur_user_id  or request.user.groups.filter(name = 'Administrators').exists():
            return True
        else:
            return False

@login_required
def edit_d(request, decision_id):
        success = 0
        if request.method == 'POST' and has_right_to_edit(request, decision_id):
            decision_num = int(request.POST['decision_num'])
            decision_year = request.POST['decision_year']

            if 'decision_date' in request.POST and request.POST['decision_date'] != '' :
                decision_date = request.POST['decision_date']
            else:
                decision_date = models.Decision.objects.filter(id = decision_id).first().dec_date

            part = request.POST['part']

            if 'url' in request.FILES:
                    file = request.FILES['url']
                    file = '/'+str( datetime.now().year)+'/'+str(file)
            else :
                file = models.Decision.objects.filter(id = decision_id).first().decision_file


            models.Decision.objects.filter(id = decision_id).update(dec_num= decision_num, dec_year = decision_year,dec_date= decision_date,related_part= part,decision_file = file )
            success=1
            url = 'archef:edit_redirect'
            # url = reverse(url)
            return redirect(url,decision_id)
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # decision =models.Decision.objects.filter(id = decision_id).last()
            # records = models.DecisionRecord.objects.filter(decision =decision ).reverse()
            #
            # context = {'records':records , 'user_name':request.user.username , 'decision' :decision, 'not_searched':1, 'new_decision':models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1}
            # #return render(request,'archef/store.html', context )
            # return render(request,'archef/store.html',context= context)


        decision = models.Decision.objects.filter(id = decision_id).first()
        #print('Record data', str(record))
        context = {
            'decision':decision,
            'success':success,
        }
        return render(request,'archef/edit_d.html', context = context)


@login_required
def edit_redirect(request, decision_id):
    if request.method == "POST":
        return store(request)
        #return redirect('archef:store',request)
    decision =models.Decision.objects.filter(id = decision_id).last()
    records = models.DecisionRecord.objects.filter(decision =decision ).reverse()
    context = {'records':records , 'user_name':request.user.username , 'decision' :decision, 'not_searched':1, 'new_decision':models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1}
    #return render(request,'archef/store.html', context )
    return render(request,'archef/store.html',context= context)





@login_required
def search(request):
    if request.method == "POST":
        year = request.POST['year']
        markaz = request.POST['markaz']
        mosalsal = request.POST['mosalsal']
        #get all decisions for this number if found
        records = models.DecisionRecord.objects.filter(year=year, markaz=markaz, mosalsal = mosalsal)
        record = records.first()
        #get shab data even if it does not have any chane
        shab = models.Shab.objects.filter(year = year, markaz=markaz, mosalsal = mosalsal).first()
        if not shab and record:
            shab = models.Shab(year = year,markaz = markaz, mosalsal = mosalsal, name = record.name, nat_id=record.national_num )
            #update shab records data base table
            shab.save()
        #print(shab)
        # for record in records:
        #      print(record.decision.decision_file)
        return view_results(request, {'records':records, 'record':shab})
    else:
        return render(request,'archef/search.html')



@login_required
def view_results(request , data):
     return render(request,'archef/view.html', context = data)



@login_required
def user_logout(request):
    logout(request)
    #return to home page
    return HttpResponseRedirect(reverse('user_login'))

from datetime import datetime
decision = models.Decision()

@login_required
def store(request):

    #user = User.objects.get(username =request.user.username )
    #ar_user = models.ArchefUser.objects.filter(user =user ).first()


    # get or return data to/from user

    #print(request.user)
    if request.method =='POST':
        if 'decision_num_search' in request.POST:
            #print(type(request.POST['year_search']))
            #print(request.POST['year_search'])
            if request.POST['year_search'] =='':
               dec_year = datetime.now().year
            else :
                dec_year = request.POST['year_search']

            global decision
            decision =models.Decision.objects.filter(dec_num =request.POST['decision_num_search'] , dec_year = dec_year ).first()
            #decisions =models.Decision.objects.filter(dec_num=request.POST['decision_num_search']  )
            #print(decision)
            #decision = decisions.last()
            records = models.DecisionRecord.objects.filter(decision =decision ).reverse()

            context = {'records':records , 'user_name':request.user.username , 'decision' :decision, 'not_searched':1, 'new_decision':models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1}
            #return render(request,'archef/store.html', context )
            return render(request,'archef/store.html',context= context)

        elif 'submit_new_decision' in request.POST :
            decision_num = int(request.POST['decision_num'])
            decision_year = int(request.POST['decision_year'])
            decision_date = request.POST['decision_date']
            if request.POST['decision_date'] == '':
                decision_date = date.today()
            part = request.POST['part']
            file = request.FILES['url']
            #file = null
            #print( file)
            #print(file.url)
            #get current user
            user = User.objects.filter(username = request.user.username).first()
            #print( str(user))
            ar_user = models.ArchefUser.objects.filter(user = user).first()
            #print( ar_user)
            decision = models.Decision(dec_num= decision_num, dec_year = decision_year,dec_date= decision_date,user =  ar_user,related_part= part,decision_file = file )

            #print(decision.decision_file.path)
            #print(decision.decision_file.url)
            if len (models.Decision.objects.filter(dec_num =decision.dec_num , dec_year = decision.dec_year)) >= 1:
                context = {"decision":"1"}
                return render(request,'archef/error.html',context)
            else:
                decision.save()
                #print('hello')
                records = models.DecisionRecord.objects.filter(decision =decision ).reverse()
                context = {'records':records , 'user_name':request.user.username , 'decision' :decision, 'not_searched':1,  'new_decision':models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1}
            #return render(request,'archef/store.html', context )
                return render(request,'archef/store.html',context= context)
            #decision.save(force_insert=True)

        elif 'submit_sub_form' in  request.POST:
            year = request.POST['year']
            markaz = request.POST['markaz']
            mosalsal = request.POST['mosalsal']
            shab = models.Shab.objects.filter(year = year, markaz=markaz, mosalsal = mosalsal).first()
            #get all decisions for this number if found
            records = models.DecisionRecord.objects.filter(year=year, markaz=markaz, mosalsal = mosalsal)
            record = records.first()
            #get shab data even if it does not have any change
            shab = models.Shab.objects.filter(year = year, markaz=markaz, mosalsal = mosalsal).first()
            if not shab :
                #check if there is a records , any record
                record = models.DecisionRecord.objects.filter(year=year, markaz=markaz, mosalsal = mosalsal).first()
                if record:
                    #print("no shab and record f_time")
                    shab = models.Shab(year = year,markaz = markaz, mosalsal = mosalsal, name = record.name, nat_id=record.national_num )
                    #update shab records data base table
                    shab.save()
                else :
                    shab = models.Shab(year = year,markaz = markaz, mosalsal = mosalsal, name = "", nat_id=None )
                    #print("no shab no record ")
            try:
                new_decision = models.Decision.objects.filter(
                    dec_year=datetime.now().year).last().dec_num+1
            except:
                new_decision = 1
            context = {'shab': shab, 'user_name': request.user.username,
                       'decision': decision,  'not_searched': 0, 'new_decision': new_decision}
            #return render(request,'archef/store.html', context )
            return render(request,'archef/store.html',context= context)

        elif 'submit_new_record' in request.POST:
            if has_right_to_edit(request, decision.id):
                #print(decision)
                year = request.POST['year']
                markaz = request.POST['markaz']
                mosalsal = request.POST['mosalsal']
                name = request.POST['m_name']
                national_num= request.POST['national_num']
                change_type = request.POST['change_type']
                ### errors due to chabs change their old data by moving to other gorvernorants
                shab_old = models.Shab.objects.filter(year = year, markaz=markaz, mosalsal = mosalsal).first()
                shab_new = models.Shab(year = year,markaz = markaz, mosalsal = mosalsal, name =name, nat_id=national_num )
                #shab_new.save()
                if shab_old :
                    if shab_old.nat_id != shab_new.nat_id: #update old shab data with the new data
                        shab_old.delete()
                        shab_new.save()



                record = models.DecisionRecord(year = year,markaz= markaz,mosalsal= mosalsal, name = name,
                                                national_num= national_num, change_type= change_type, decision=decision )
                #see if this record already exists in the current decision
                if len (models.DecisionRecord.objects.filter(decision=decision , national_num = national_num)) >= 1:
                    #print(str(national_num))
                    #raise ValueError ("هذا الشاب تم تسجيله بالفعل فى القرار ")
                    context = {"decision_record":"1"}
                    return render(request,'archef/error.html', context)
                else:
                    record.save()

            records = models.DecisionRecord.objects.filter(decision =decision ).reverse()

            context = {'records':records , 'user_name':request.user.username , 'decision' :decision, 'not_searched':1, 'new_decision':models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1}
            #return render(request,'archef/store.html', context )
            return render(request,'archef/store.html',context= context)
           # return HttpResponse(request)
        elif 'last_decision' in request.POST:
            decision  = models.Decision.objects.last()
            #print(decision.dec_year)
            records = models.DecisionRecord.objects.filter(decision =decision ).reverse()
            #print(records)
            try :
                new_decision = models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1
            except :
                new_decision = 1
            context = {'records': records, 'user_name': request.user.username,
                       'decision': decision, 'not_searched': 1, 'new_decision': new_decision}
            #return render(request,'archef/store.html', context )
            return render(request,'archef/store.html',context= context)

    #print(decision)
    # related to main if
    #else:
    try:
        context = {'new_decision':models.Decision.objects.filter(dec_year = datetime.now().year).last().dec_num+1}
    except :
        context = {'new_decision': 1 }
    return render(request,'archef/store.html', context = context)
