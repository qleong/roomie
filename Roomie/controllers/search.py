__author__ = 'Quintin'


def index():
    #Displays a search form for the user
    form = SQLFORM.factory(
        Field('Search',
        required=True),
        submit_button="Search"
    )

    if(form.process().accepted):
        redirect(URL('search', 'display_conversations', args=[form.vars.Search]))

    return dict(form=form)

def search():
    #Displays search form
    form = SQLFORM.factory(
        Field('Search',
        required=True),
        submit_button="Search",
    )

    if(form.process().accepted):
        redirect(URL('search', 'result', args=[form.vars.Search]))

    return dict(form=form)

def result():
    #Retrieves and displays the results of the user's search query
    form = SQLFORM.factory(
        Field('Search',
        required=True),
        submit_button="Search"
    )

    if(form.process().accepted):
        redirect(URL('search', 'result', args=[form.vars.Search]))

    search = request.args[0]
    name = perform_name_search(search)

    #Gets the display names for all of the search query results
    for item in name:
        item.display_name = item.first_name + " " + item.last_name
    city = perform_city_search(search)
    return dict(form=form, names=name, city=city)


def perform_name_search(search):
    #Performs search by name
    result = db((db.user_profile.first_name==search)|(db.user_profile.last_name==search)).select()
    return result

def perform_city_search(city):
    #Peforms search by city
    result = db(db.user_profile.city_location==city).select()
    return result