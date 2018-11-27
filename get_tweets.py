#Este script sirve para recuperar los tweets vía streaming. Se debe ejecutar y permitir recopilar la información por un periodo
#de tiempo que se desee. En caso de que la conexión se pierda, es necesario volver a ejecutar el script.

#Importamos las bibliotecas necesarias

#tweepy permite realizar conexión con Twitter y recuperar tweets
import tweepy

#Permite realizar conexión con el servidor de MongoDB, y realizar distintas queries
import pymongo
from pymongo import MongoClient

#Creamos una conexión con el servidor
client = MongoClient("mongodb://rafael:S7BNKu4WAj2z3ca6@nonstructureddatamanagementclass-shard-00-00-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-01-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-02-xa2lb.mongodb.net:27017/twitter_db?ssl=true&replicaSet=NonStructuredDataManagementClass-shard-0&authSource=admin&retryWrites=true")

#Nuestra base de datos se llamará "mongo_test"
db_name = "nintendo"

#Se conecta a una base de datos especificada. Si no existe, la crea
#Creamos la base de datos "mongo_test" o nos conectamos a ella
db = client[db_name]

#Recuperamos el nombre de todas las bases de datos en el servidor
db_list = client.list_database_names()

#Revisamos si la base de datos existe
if db_name in db_list:
    print("La base de datos \"" + db_name + "\" existe!")

#Nuestra colección se llamará "tweets"
#Una colección es un grupo de documentos almacenados en MongoDB
collection_name = "tweets"

#Crea una nueva colección o recupera el contenido de una existente
#Si la colección se está creando, MongoDB no la va a crear hasta que se le inserte documentos
collection = db[collection_name]

#Recuperamos el nombre de todas las colecciones
collection_list = db.list_collection_names()

#Revisamos si la colección existe. Si la colección creada no tiene elementos, MongoDB no la va a crear hasta insertar un documento
if collection_name in collection_list:
    print("La coleccion \"" + collection_name + "\" existe!\n")

#override tweepy.StreamLis#client = MongoClient()tener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    #Para cada tweet recuperado, guardamos la fecha, nombre de usuario, conteo de retweets, idioma y contenido
    def on_status(self, status):
        tweet = {
            "created_at": status.created_at,
            "text": status.text,
            "user": {
                "name": status.user.name,
                "screen_name": status.user.screen_name,
                "location": status.user.location,
                "url": status.user.url,
                "description": status.user.description
            },
            "source": status.source,
            "extended_tweet": "", 
            "retweeted": status.retweeted,
            "lang": status.lang,
            "place": {
                "country": "",
                "full_name": "",
                "name": ""
            },
            "truncated": status.truncated
        }

        if (hasattr(status, "extended_tweet")):
            if (hasattr(status.extended_tweet, "full_text")):
                tweet["extended_tweet"] = status.extended_tweet.full_text
        if (hasattr(status, "place")):
            if (hasattr(status.place, "country")): 
                tweet["place"]["country"] = status.place.country
            if (hasattr(status.place, "full_name")): 
                tweet["place"]["full_name"] = status.place.full_name
            if (hasattr(status.place, "name")): 
                tweet["place"]["name"] = status.place.name

        #Imprimimos los tweets para verificar que el stream sigue activo
        print(status.text + "\n")

        inserted = collection.insert_one(tweet)

consumer_key = 'y1i3Hhy3GUMOx9jvulw4Y8B1z'
consumer_secret = 'GG5DsFKTNPKz8PabBDY7a7sbm9gjVlYJqx3y3ifBAGpS5MGEL0'
access_token = '240873982-qDYkFUqP8WSjD4M0LtBRn9w0ixPMFmvWcuj3lBlg'
access_token_secret = 'ahVTnCMzhaCBZNyWzRd4agB0eiWB23O92cY1ft6ba6BQy'

#Datos de acceso a la api. Reemplazar con los propios apenas den autorización
'''consumer_key = '0zLVRnLCdP0JuUxjsMlB5P6id'
consumer_secret = 'UEOvI6l0QFgaWxIzee3LJMOt5C59M5YhL9yh40dOq0ZGBXs85n'
access_token = '940271662959906816-CEzHkOji1IYR1Z1VZeXdSYDrNetgRVT'
access_token_secret = 'wXev8vS56LhX06adGOgDX8HFTrAcjhwSztQGBGlzQePVA'''

#Se realiza la validación con la api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Autenticación a la api
api = tweepy.API(auth)

#Iniciamos un nuevo stream de tweets
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode='extended')

#Establecemos que los tweets que queremos recibir
myStream.filter(track=['Nintendo', 'NintendoDirect', 'NintendoSwitch', 'SmashBros', 'SuperSmashBros', 'SuperSmashBrosUltimate', 'SmashBrothers', 'SuperSmashBrothers', 'SuperSmashBrothersUltimate', 'SmashUltimate'])