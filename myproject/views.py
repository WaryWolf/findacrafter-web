from pyramid.i18n import TranslationStringFactory
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from db import Armory
import time


def faq(request):
    #print request.client_addr
    return render_to_response(  'templates/faq.jinja2', 
                                { 'a': 1 },
                                request = request )

def recipes(request):
    text = request.params.get('term', '')    
    db = Armory()
    recs = [str(element) for (element,) in db.getAllRecipes()]
    db.close()
    return [x for x in recs if text.lower() in x.lower()]


def error(errstr):
    return Response("Error: " + errstr)


def search(request):
    db = Armory()
    realms = db.getRealms()
    db.close()
    return render_to_response(  'templates/search-new.jinja2',
                                { 'realms': realms },
                                request = request )


def results(request):
    servid = request.matchdict['server']
    faction = request.matchdict['faction']
    recipe = request.matchdict['recipe']

    db = Armory()

    if not db.doesRealmExist2(servid):
        return error("Invalid Realm")

    if faction not in ['A', 'H', 'B']:
        return error("Invalid Faction")

    recipeids = db.getRecipeID(recipe)

    if len(recipeids) == 0:
        return error("That search matched 0 recipes :(")

    if len(recipeids) > 1:
        #return error()   #make this redirect to a "did you mean...?" page
        return render_to_response( 'templates/results-new.jinja2',
                                    { 'toobroad': True,
                                    'res': recipeids,
                                    'resnum': len(recipeids),
                                    'servid': servid,
                                    'faction': faction },
                                    request = request )

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
    db.close()

    if len(res) == 0:
        return error("We couldn't find any crafters for that item on your server. Sorry!")

    return render_to_response( 'templates/results-new.jinja2',
                                { 'res': res,
                                'recipeid': recipeid,
                                'recipename': recipename,
                                'count': totalcount },
                                request = request )

