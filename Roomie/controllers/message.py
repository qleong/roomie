__author__ = 'Quintin'

@auth.requires_login()
def index():
    return dict()

@auth.requires_login()
def view_conversations():
    user_id = auth.user.id
    conversations = get_conversations(user_id)

    for conversation in conversations:
        name = None
        if(int(conversation.recipient) == int(user_id)):
            name = get_user_name(conversation.sender)
        elif(int(conversation.sender) == int(user_id)):
            name = get_user_name(conversation.recipient)
        conversation.name = name

    return dict(conversations=conversations)

@auth.requires_login()
def send_message():
    sender = auth.user.id
    recipient = request.args[0]

    conversation = get_existing_conversation(sender, recipient)
    conversation_id = conversation.id if conversation != None else None
    #If conversation between users exist, just go to the thread
    if(conversation != None):
        redirect(URL('message', 'view_messages', args=[conversation_id]))

    #Otherwise start a new conversation
    form = SQLFORM.factory(Field('topic',label='Title',),
                           Field('message_content', 'text', label='Message'),
                           )
    form.add_button('Cancel', URL('profile', 'view_profile', args=[recipient]))

    if(form.process().accepted):
        #Add a new conversation and insert one message_item, redirect to the conversation thread
        conversation_id = db.conversation.insert(sender=sender, recipient=recipient, topic=form.vars.topic)
        db.message_item.insert(sender=sender, recipient=recipient, conversation_id=conversation_id,body=form.vars.Message)
        redirect(URL('profile', 'view_profile', args=[recipient]))

    return dict(form=form)

def view_messages():
    conversation_id = request.args[0]
    messages = get_messages(conversation_id)
    sender = None
    recipient = None
    if(messages != None):
        sender = str(get_user_name(messages[0].sender))
        recipient = str(get_user_name(messages[0].recipient))

    form = SQLFORM.factory(Field('message', 'text',required=IS_NOT_EMPTY()))
    if(form.process().accepted):
        user = auth.user_id
        receive = messages[0].recipient if messages[0].recipient != user else messages[0].sender
        db.message_item.insert(sender=user,recipient=receive,conversation_id=conversation_id,body=form.vars.message)

        redirect(URL('message','view_messages',args=[conversation_id]))

    return dict(messages=messages,sender=sender,recipient=recipient,form=form)


def get_messages(conversation_id):
    query = db(db.message_item.conversation_id==conversation_id).select(orderby=~db.message_item.ts_sent)
    return query

def get_conversations(user_id):
    conversations = db((db.conversation.recipient==user_id)|(db.conversation.sender==user_id)).select(db.conversation.id, \
            db.conversation.sender,db.conversation.recipient, db.conversation.topic)
    return conversations

def get_user_name(user_id):
    query = db(db.user_profile.user_id==user_id).select(db.user_profile.first_name, db.user_profile.last_name).first()
    name = str(query.first_name) + " " + str(query.last_name)
    return name

def get_existing_conversation(user1, user2):
    result = db(((db.conversation.sender==user1)&(db.conversation.recipient==user2)|\
        ((db.conversation.sender==user2)&(db.conversation.recipient==user1)))).select(db.conversation.id).first()
    return result
