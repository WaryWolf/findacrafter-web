import psycopg2
#import psycopg2.exensions

class Armory(object):

    def __init__(self):
        self.conn = psycopg2.connect(database="armory", user="readonly", password="reader", host="localhost")
        self.cur = self.conn.cursor()
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, self.cur)

    def doesRealmExist(self, realmid):
        self.cur.execute("SELECT 1 FROM information_schema.tables \
                          WHERE table_schema = 'public' and table_name = 'characters_{0}' LIMIT 1;".format(realmid))
        #return bool(self.cur.rowcount)
        if self.cur.rowcount == 0:
            return False
        else:
            return True

    def doesRealmExist2(self, realmid):
        self.cur.execute("SELECT * from realms WHERE realm_id = %s;", [realmid])
        if self.cur.rowcount == 0:
            return False
        else:
            return True

    def getRealms(self):
        self.cur.execute("SELECT * FROM realms ORDER BY realm ASC")
        return self.cur.fetchall()

    def getRealmID(self, name):
        self.cur.execute("SELECT realm_id FROM realms WHERE realm = '{0}';".format(name))
        return self.cur.fetchone()

    def getRealmName(self, realmid):
        self.cur.execute("SELECT realm FROM realms WHERE realm_id = '{0}';".format(realmid))
        return self.cur.fetchone()

    def getRealmConnections(self, realmid):
        self.cur.execute("SELECT realms.realm, realms.realm_id FROM connections, realms WHERE \
                          realms.realm_id = connections.realm_id AND id IN \
                    ( SELECT id FROM connections WHERE realm_id = '{0}')".format(realmid))
        return self.cur.fetchall()

    def getRealmConnectionsFromName(self, name):
        self.cur.execute("SELECT realms.realm_id, realms.realm FROM realms, connections WHERE realms.realm_id = connections.realm_id \
                    AND connections.id in (SELECT id FROM connections, realms WHERE realms.realm_id = connections.realm_id \
                    AND realms.realm = '{0}');".format(name))
        return self.cur.fetchall()


    def getRealmCrafters(self, realmid, recipeid, faction):
        self.cur.execute("SELECT name, last_active, last_checked, faction FROM characters_{0} c, char_recipe_{0} r\
                    WHERE c.char_id = r.char_id \
                    AND r.recipe_id = '%s' \
                    AND c.faction LIKE %s ORDER BY c.last_active DESC LIMIT 100;".format(realmid), [recipeid, faction])
        return self.cur.fetchall()


    def getRecipeID(self, recipestring):
        self.cur.execute("SELECT recipe_id, name FROM recipes WHERE name ILIKE '%%' || %s || '%%';", [recipestring])
        return self.cur.fetchall()

    def getAllRecipes(self):
        self.cur.execute("SELECT name FROM recipes;")
        return self.cur.fetchall()
