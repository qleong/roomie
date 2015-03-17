# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index():
    user_id = request.args(0) or auth.user.id
    information = get_profile(user_id)
    return dict(user_id=user_id, info=information)

@auth.requires_login()
def view_profile():
    user_id = request.args(0) or auth.user.id
    information = get_profile(user_id)
    if(information == None):
        redirect(URL('profile', 'create_profile'))

    friend = None
    if(user_id != auth.user_id):
        friend = is_friend(auth.user_id, user_id)
    else:
        friend = False

    form = SQLFORM.factory(Field('review', requires=IS_NOT_EMPTY()))
    if(form.process().accepted):
        review = form.vars.review
        db.review.insert(friend_id=auth.user_id, user_id=user_id, review_content=review)
        redirect(URL('profile', 'view_profile', args=[user_id]))

    reviews = get_reviews(user_id)

    roomies = get_roomies(user_id)
    friend_info = {}
    for row in roomies:
        lookup = row.user_id if row.user_id != auth.user.id else row.friend_id
        the_name = get_user_name(lookup)
        the_pic = db(db.user_profile.user_id==lookup).select().first().image
        friend_info[lookup] = [the_name, the_pic]

    return dict(user_id=user_id, profile=information, friend=friend, form=form, reviews=reviews,roomies=roomies, friend_info=friend_info)

@auth.requires_login()
def create_profile():
    user_id = auth.user.id
    form = SQLFORM(db.user_profile)

    if(form.process().accepted):
        redirect(URL('profile','view_profile',args=(user_id)))

    return dict(form=form)


@auth.requires_login()
def edit_profile():
    user_id = auth.user.id
    profile = db(db.user_profile.user_id==user_id).select().first()
    form = SQLFORM(db.user_profile, profile)

    #Add a cancel button that takes user back to their profile
    form.add_button('Cancel', URL('profile', 'view_profile'))

    if(form.process().accepted):
        redirect(URL('profile','view_profile',args=(user_id)))
    return dict(form=form)

@auth.requires_login()
def request_roomie():
    roomie = request.args[0]
    user = auth.user.id

    exist = db((db.roomies.friend_id==roomie)&(db.roomies.user_id==user)).select().first()
    if(exist == None):
        db.roomies.insert(user_id=user, friend_id=roomie, accepted=0)

    redirect(URL('profile','view_profile',args=[roomie]))

@auth.requires_login()
def view_pending_request():
    request = get_pending_request()
    names = {}
    for row in request:
        names[row.user_id] = get_user_name(row.user_id)
    return dict(requests=request,names=names)

@auth.requires_login()
def accept_request():
    user_id = auth.user.id
    friend_id = request.args[0]
    row_id = db((db.roomies.friend_id==user_id)&(db.roomies.user_id==friend_id)).select(db.roomies.id).first()
    db.executesql("UPDATE roomies SET accepted=1 WHERE id = " + str(row_id.id) + " ;")
    redirect(URL('profile','view_pending_request'))

@auth.requires_login()
def decline_request():
    user_id = auth.user.id
    friend_id = request.args[0]
    row_id = db((db.roomies.friend_id==user_id)&(db.roomies.user_id==friend_id)).select(db.roomies.id).first()
    db.executesql("DELETE FROM roomies WHERE id = " + str(row_id.id) + " ;")
    redirect(URL('profile','view_pending_request'))

def get_user_name(user_id):
    query = db(db.user_profile.user_id==user_id).select(db.user_profile.first_name, db.user_profile.last_name).first()
    name = str(query.first_name) + " " + str(query.last_name)
    return name

def get_pending_request():
    query = db((db.roomies.friend_id==auth.user.id)&(db.roomies.accepted==0)).select()
    return query

def get_profile(user_id):
    profile = db(db.user_profile.user_id==user_id).select().first()
    return profile

def has_profile_image(user_id):
    image = db(db.user_profile.user_id==user_id).select(db.user_profile.image).first()
    if(image == ''):
        return True
    else:
        return False

def is_friend(user_id, friend_id):
    query = db((db.roomies.user_id==user_id)&(db.roomies.accepted==1)).select()
    if(query != None):
        for row in query:
            if friend_id == row.friend_id:
                return True
    else:
        return False
    return False

def get_reviews(user):
    reviews = db(db.review.user_id==user).select()
    return reviews

def get_roomies(user_id):
    friends = db(((db.roomies.friend_id==user_id)|(db.roomies.user_id==user_id))&(db.roomies.accepted==1)).select()
    return friends