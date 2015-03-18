__author__ = 'Quintin'

from datetime import datetime

#Table that holds all of the conversations
db.define_table('conversation',
                Field('sender'),
                Field('recipient'),
                Field('topic'),
                Field('viewed'),
                Field('ts_update')
)



db.conversation.id.readable = db.conversation.id.writable = False
db.conversation.sender.required = True
db.conversation.sender.default = auth.user_id
db.conversation.recipient.required = True
db.conversation.topic.required = True
db.conversation.viewed.requires = IS_IN_SET([0,1])
db.conversation.viewed.default = 0
db.conversation.ts_update.default =  datetime.utcnow()


