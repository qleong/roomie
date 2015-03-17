# -*- coding: utf-8 -*-

def get_first_name():
    name = 'Nobody'
    if auth.user:
        name = auth.user.first_name
    return name

def get_last_name():
    name = ''
    if auth.user:
        name = auth.user.last_name
    return name


db.define_table('user_profile',
                Field('user_id', db.auth_user),
                Field('first_name'),
                Field('last_name'),
                Field('phone'),
                Field('email'),
                Field('state_location'),
                Field('city_location'),
                Field('gender'),
                Field('bio', 'text'),
                Field('image', 'upload')
                )


db.user_profile.id.readable = db.user_profile.id.writable = False
db.user_profile.user_id.writable = False
db.user_profile.user_id.readable = False
db.user_profile.first_name.default = get_first_name()
db.user_profile.last_name.default = get_last_name()
db.user_profile.user_id.default = auth.user_id
db.user_profile.phone.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$', error_message='not a phone number')
db.user_profile.email.requires = IS_EMAIL()
db.user_profile.image.required = True
db.user_profile.image.requires = IS_IMAGE()
db.user_profile.state_location.required = True
db.user_profile.state_location.requires = IS_IN_SET(L.STATES)
db.user_profile.gender.requires = IS_IN_SET(L.GENDERS)
db.user_profile.state_location.required = True
db.user_profile.city_location.required = True
db.user_profile.gender.required = True