from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Friendships
from django.db.models import Q
import datetime
#import model


#useful functions NOT VIEWS



# VIEWS BEGIN-----------GET Requests----------------------------------------------------------------

#REGISTER AND LOGIN PAGE 
def main(request):
    request.session['logged_in'] = "False"
    return render (request, "main.html")


def friends(request): #to display friends and not friends
    if request.session['logged_in'] == "True":
        id = int(request.session['uid']) # set when logged in or registered
        user = User.objects.get(id=id)
        users = User.objects.filter(~Q(id=id)) # all users except for logged in
        friends = user.the_friender.all()
        friend_list = []
        for friend in friends:
            friend_list.append(friend.friended_user)
            
        user_list = []
        for user in users:
            user_list.append(user)
        # Only be able to add users not already friends with tough one!
        if not friends:
            not_friends = users
        elif friends:
            not_friends = []
            
            for user in user_list:
                i = 0
                withold = False
                while i < len(friend_list):
                    if user == friend_list[i]:
                        withold = True
                        i += 1
                    i +=1
                if withold == False:
                    not_friends.append(user)

        context = {
            "user": user,
            "friends": friends,
            "not_friends": not_friends
            
        }
        return render (request, "friends.html", context)
    else:
        return redirect('/main') #if not authed, send to main


def view_profile(request, id): # to view a user's profile
    if request.session['logged_in'] == "True": 
        user = User.objects.get(id=id)
        context = {
            "user": user
        }
        return render (request, "profile.html", context)
    else:
        return redirect('/main')
        #only let authenticated users view profiles

# Views for POST requests---AND Actions---------------------------
def register(request):
    if request.method == 'POST':
        #first ensure errors are handled
        errors = User.objects.user_validator(request.POST)
        if request.POST['password'] != request.POST['confirm']:
            messages.error (request, "Passwords do not match.")
        #add something for if not older than 16 
        
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect ('/main')
        
        else:
            #hash the password
            pass_to_hash = request.POST['password']
            pass_hash = bcrypt.hashpw(pass_to_hash.encode(), bcrypt.gensalt()).decode()
            # add user to db
            user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email = request.POST['email'], password=pass_hash, dob=request.POST['dob'])
            # make session data correct
            request.session['logged_in'] = "True"
            request.session['uid'] = user.id
        return redirect ('/friends')

def login(request):
    if request.method == 'POST':
        #first ensure errors are handled
        errors = User.objects.user_login_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect ('/main')
        else:
            #get user
            user = User.objects.get(email=request.POST['email'])
           
            if user:
                #check password
                given_password = request.POST['password']
                
               
                
                is_working = bcrypt.checkpw(given_password.encode(), user.password.encode())
                
                if bcrypt.checkpw(given_password.encode(), user.password.encode()):
                    request.session['logged_in'] = "True"
                    request.session['uid'] = user.id
                    return redirect('/friends')
                else:
                    messages.error(request, "email or password is incorrect")
                    return redirect('/main')

def add_friend(request, fid): #fid = user to friend
    #get logged in id from session
    id = int(request.session['uid'])
    user = User.objects.get(id=id)
    friend = User.objects.get(id=fid)
    
    friendship = Friendships.objects.create(friender=user, friended_user=friend)
    
    return redirect ('/friends')

def remove_friend(request, fid):
    #get logged in id from session
    id = int(request.session['uid'])
    user = User.objects.get(id=id)
    friended = User.objects.get(id=fid)
    friend = Friendships.objects.filter(friended_user=friended)
    friend.delete()
    return redirect('/friends')

def logout(request):
    request.session['logged_in'] = "False"
    del request.session['uid']
    return redirect('/main')










