__author__ = 'Quintin'


#Table that holds the roomie relationships
db.define_table('roomies',
    Field('user_id'),
    Field('friend_id'),
    Field('accepted')
)

db.roomies.user_id.required = True
db.roomies.friend_id.required = True
db.roomies.accepted.requires = IS_IN_SET([0,1])
db.roomies.accepted.default = 0