__author__ = 'Quintin'


db.define_table('review',
                Field('friend_id'),
                Field('user_id'),
                Field('review_content'))


db.review.friend_id.required = True
db.review.user_id.required = True
db.review.review_content.required = True