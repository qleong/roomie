__author__ = 'Quintin'

from datetime import datetime


db.define_table('message_item',
                Field('conversation_id'),
                Field('sender'),
                Field('recipient'),
                Field('ts_sent'),
                Field('body')
)



db.message_item.id.readable = db.message_item.id.writable = False
db.message_item.conversation_id.required = True
db.message_item.body.required = True
db.message_item.ts_sent.required = True
db.message_item.sender.required = True
db.message_item.recipient.required = True
db.message_item.conversation_id.writable = False
db.message_item.ts_sent.writable = False
db.message_item.ts_sent.default =  datetime.utcnow()



