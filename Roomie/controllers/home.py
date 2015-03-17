# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index(): 
    return(dict(message="test"))


@auth.requires_login()
def home():
    user_id = auth.user.id
    redirect(URL('profile','view_profile', args=(user_id)))
    return(dict(form=form))
