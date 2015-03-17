__author__ = 'Quintin'


def index():
    form = SQLFORM.factory(
        Field('Search',
        required=True),
        submit_button="Search",

    )

    if(form.process().accepted):
        redirect(URL('search', 'display_conversations', args=[form.vars.Search]))

    return dict(form=form)

def search():
    form = SQLFORM.factory(
        Field('Search',
        required=True),
        submit_button="Search",
    )

    if(form.process().accepted):
        redirect(URL('search', 'result', args=[form.vars.Search]))

    return dict(form=form)

def result():
    form = SQLFORM.factory(
        Field('Search',
        required=True),
        submit_button="Search"
    )

    if(form.process().accepted):
        redirect(URL('search', 'result', args=[form.vars.Search]))

    search = request.args[0]
    name = perform_name_search(search)
    for item in name:
        item.display_name = item.first_name + " " + item.last_name
    city = perform_city_search(search)
    return dict(form=form, names=name, city=city)


def perform_name_search(search):
    result = db((db.user_profile.first_name==search)|(db.user_profile.last_name==search)).select()
    return result

def perform_city_search(city):
    result = db(db.user_profile.city_location==city).select()
    return result