from pyramid.i18n import TranslationStringFactory
from pyramid.response import Response
from pyramid.view import view_config
import psycopg2
import colander
from deform import Form
from deform import ValidationFailure
import deform
from db import Armory
import time


@view_config(route_name='recipes',renderer='json')
def recipes(request):
    text = request.params.get('term', '')    
    db = Armory()
    recs = [str(element) for (element,) in db.getAllRecipes()]
    return [x for x in recs if text.lower() in x.lower()]


def error(errstr):
    return Response("Error: " + errstr)


@view_config(renderer='templates/search-new.jinja2',route_name='search')
def newform(request):
    db = Armory()
    realms = db.getRealms()
    return {'realms': realms }


@view_config(renderer='templates/results-new.jinja2',route_name='find')
def results2(request):
    servid = request.matchdict['server']
    faction = request.matchdict['faction']
    recipe = request.matchdict['recipe']

    db = Armory()

    if not db.doesRealmExist2(servid):
        print "1"
        return error("Invalid Realm")

    if faction not in ['A', 'H', 'B']:
        print "2"
        return error("Invalid Faction")

    recipeids = db.getRecipeID(recipe)

    if len(recipeids) == 0:
        print "3"
        return error("That search matched 0 recipes :(")

    if len(recipeids) > 1:
        print "4"
        #return error()   #make this redirect to a "did you mean...?" page
        return {
                'toobroad': True,
                'res': recipeids,
                'resnum': len(recipeids),
                'servid': servid,
                'faction': faction
        }

    recipeid = recipeids[0][0]
    recipename = recipeids[0][1]
    
    if faction == 'B':
        faction = '%'

    connects = db.getRealmConnections(servid)

    if len(connects) == 0:
        connects = [(db.getRealmName(servid)[0],servid)]

    res = []
    
    totalcount = 0
    showcount = 0
    for realm in connects:

        realmid = realm[1]
        realmname = realm[0]
        realmcrafters = db.getRealmCrafters(realmid, recipeid, faction)

        for crafter in realmcrafters:
            totalcount += 1
            if showcount == 100:
                continue
            res.append((crafter[0], time.ctime(int(crafter[1])), time.ctime(int(crafter[2])), crafter[3], realmname))
            showcount += 1
    

    if len(res) == 0:
        print "6"
        return error("We couldn't find any crafters for that item on your server. Sorry!")

    return {'res': res,
            'recipeid': recipeid,
            'recipename': recipename,
            'count': totalcount
    }

'''
#@view_config(renderer='templates/site_view.pt',route_name='search')
def search(request):

    widget = deform.widget.AutocompleteInputWidget(
        size=60,
        min_length=3,
        values = '/recipes')

    db = Armory()
    realmnames = db.getRealms() 
    class RecipeSearch(colander.MappingSchema):
        server = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(values=realmnames)
            )
        recipe = colander.SchemaNode(
            colander.String(),
            widget = widget
            )
        faction = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(values=[
                ('', 'Faction'),
                ('A', 'Alliance'),
                ('H', 'Horde'),
                ('B', 'Both') ]
                )
            )

    search=RecipeSearch()  
    myform = Form(search, buttons=('submit',),action='/results')

    return {"form": myform.render()}
'''


'''
@view_config(renderer='templates/results.jinja2',route_name='results')
def results(request):

    if ('submit' in request.POST) and ('recipe' in request.POST) and ('server' in request.POST):


@view_config(renderer='templates/results.jinja2',route_name='results')
def results(request):

    if ('submit' in request.POST) and ('recipe' in request.POST) and ('server' in request.POST):


        db = Armory()
        reciperes = db.getRecipeID(request.POST.getone('recipe'))
        
        #print type(recipeid)
        #print str(recipeid)

        rc = len(reciperes)
        if rc > 1:
            return Response("<b>Sorry, your search was too broad and returned {0} results. Please try again.</b>".format(rc))
        elif rc == 0:
            return Response("<b>Sorry, your search returned 0 results. Please try again.</b>")
        recipeid = reciperes[0][0]
        recipename = reciperes[0][1]
        #print recipeid
        res = []

        if (db.doesRealmExist(request.POST.getone('server')) == False):
            return Response("<b>Sorry, that realm doesn't exist...</b>")
        #print request.POST.getone('server')
        
        connects = db.getRealmConnections(request.POST.getone('server'))
        #print str(connects)
        cc = len(connects)
        if cc == 0:
            connects = [(db.getRealmName(request.POST.getone('server'))[0],request.POST.getone('server')[0])]


        totalcount = 0
        showcount = 0
        for realm in connects:

            realmid = realm[1]
            realmname = realm[0]
            #print realmid
            #print realmname
            realmcrafters = db.getRealmCrafters(realmid, recipeid, faction)

            for crafter in realmcrafters:
                totalcount += 1
                if showcount == 100:
                    continue
                res.append((crafter[0], time.ctime(int(crafter[1])), time.ctime(int(crafter[2])), crafter[3], realmname))
                showcount += 1
        
        #craftcount = len(res) 
        #print str(res)
        if len(res) == 0:
            return Response("we couldn't find anyone from your realm who makes that recipe, sorry :(") 
        #return Response("<b>good work</b>")
        return {'res': res,
                'recipeid': recipeid,
                'recipename': recipename,
                'count': totalcount}
    else:

'''
