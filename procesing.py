import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pymongo import MongoClient
from wordcloud import STOPWORDS
from wordcloud import WordCloud

from generate_plot_list import generate_source_list
from generate_plot_list import generate_country_list

# Creamos una conexión con el servidor
client = MongoClient(
    "mongodb://rafael:S7BNKu4WAj2z3ca6@nonstructureddatamanagementclass-shard-00-00-xa2lb.mongodb.net:27017,"
    "nonstructureddatamanagementclass-shard-00-01-xa2lb.mongodb.net:27017,"
    "nonstructureddatamanagementclass-shard-00-02-xa2lb.mongodb.net:27017/twitter_db?ssl=true&replicaSet"
    "=NonStructuredDataManagementClass-shard-0&authSource=admin&retryWrites=true")

# Nuestra base de datos se llamará "nintendo"
db_name = "nintendo"

# Intentamos realizar una conexión con la base de datos. Si la BD no existe, la crea.
db = client[db_name]

# Recuperamos el nombre de todas las bases de datos en el servidor
db_list = client.list_database_names()

# Revisamos si la base de datos existe
if db_name in db_list:
    print("\nLa base de datos \"" + db_name + "\" existe!")

# Una colección es un grupo de documentos almacenados en MongoDB
# Nuestra colección se llamara "tweets"
collection_name = "tweets"

# Crea una nueva colección o recupera el contenido de una existente
# Si la colección se está creando, MongoDB no la va a crear hasta que se le inserte documentos
collection = db[collection_name]

# Recuperamos el nombre de todas las colecciones
collection_list = db.list_collection_names()

# Revisamos si la colección existe. Si la colección creada no tiene elementos, MongoDB no la va a crear hasta
# insertar un documento
if collection_name in collection_list:
    print("La coleccion \"" + collection_name + "\" existe!\n")


# Imprime el contenido del tweet recuperado de MongoDB
def print_single_tweet(tweet):
    print("\ncreated_at: " + str(tweet["created_at"]))
    print("text: " + tweet["text"])
    print("user.name: " + tweet["user"]["name"])
    print("user.screen_name: " + tweet["user"]["screen_name"])
    print("user.location: " + str(tweet["user"]["location"]))
    print("user.url: " + str(tweet["user"]["url"]))
    print("user.description: " + str(tweet["user"]["description"]))
    print("source: " + tweet["source"])
    print("extended_tweet: " + tweet["extended_tweet"])
    print("retweeted: " + str(tweet["retweeted"]))
    print("lang: " + tweet["lang"])
    print("place.country: " + tweet["place"]["country"])
    print("place.full_name: " + tweet["place"]["full_name"])
    print("place.name: " + tweet["place"]["name"])
    print("truncated: " + str(tweet["truncated"]))


# Imprimimos todos los tweets de un conjunto dado
def print_tweets(tweets):
    for tweet in tweets:
        print_single_tweet(tweet)


# Verifica que el tweet no sea uno relacionado con términos que no son relevantes para nosotros
def is_valid_tweet(tweet):
    # Dados los tags usados para recopilar los tweets, no todos resultaron tener información útil. Así que se tiene
    # una lista de tweets cuyo tema no es de nuestro interés
    filter_list = [
        "64",
        "classic",
        "n64",
        "#lookingfor",
        "$239.99",
        "#splatoon2",
        "wii"
    ]

    for fw in filter_list:
        if fw in tweet:
            return False

    return True


# Retorna una lista de tweets sin aquellos que contenga términos que no nos interesan
def clean_tweets(tweets):
    tweets_cleaned = []

    for tweet in tweets:
        if is_valid_tweet(tweet["text"].lower()):
            tweets_cleaned.append(tweet)

    return tweets_cleaned


# Genera una imagen .png con una nube de palabras de los términos más usados en los tweets
def generate_wordcloud(tweets):
    print("\nGenerando nube de palabras...\n")

    text = ""

    for tweet in tweets:
        # Concatenamos todo el texto de los tweets en una sola variable para poder procesarlo
        text = text + tweet["text"] + "\n"
        print(tweet["text"] + "\n")

    # Cargamos la lista de stopwords y añadimos más que consideramos no relevantes para mostrar en la nube de palabras
    # Las stopwords son palabras que serán ignoradas
    stopwords = set(STOPWORDS)
    stopwords.add("nintendodirect")
    stopwords.add("smash")
    stopwords.add("bros")
    stopwords.add("smashbros")
    stopwords.add("supersmashbros")
    stopwords.add("ultimate")
    stopwords.add("smashbrosultimate")
    stopwords.add("supersmashbrosultimate")
    stopwords.add("co")
    stopwords.add("nintendo")

    # Cargamos la máscara que usaremos para darle forma a la nube
    mask = np.array(Image.open("mario.png"))

    # Genera una nube de palabras. Las stopwords serán ignoradas y no apareceran en la gráfica
    wordcloud = WordCloud(width=1079, height=1623, max_words=10000, relative_scaling=1, stopwords=stopwords,
                          mask=mask, contour_color="white").generate(text)

    # Guardamos la nube de palabras generada en una imagen en la misma carpeta del script
    wordcloud.to_file("wordcloud.png")


def generate_devices_plot(tweets):
    print("\nGenerando gráfica de dispositivos...\n")

    source_list = generate_source_list(tweets)

    labels = []
    sizes = []

    src_count = 0
    max_src = 7

    src_plot = []

    for src in source_list:
        if src_count < max_src:
            src_plot.append(src)
            src_count = src_count + 1

        if src_count == max_src:
            src_plot.append({
                "source": "Others",
                "count": 1
            })

            src_count = src_count + 1

        if src_count > max_src:
            src_plot[max_src]["count"] = src_plot[max_src]["count"] + 1

    for src in src_plot:
        labels.append(src["source"])
        sizes.append(src["count"])

    plt.pie(sizes, labels=labels, shadow=True, radius=10, autopct="%0.2f%%")
    plt.axis("equal")
    plt.savefig("piechart.png")


def generate_country_plot(tweets):
    print("\nGenerando gráfica de países...\n")

    country_list = generate_country_list(tweets)


# MAIN BODY------------------------------------------------------------------------------------------------------------#

# eng_tweets = collection.find({"lang": "en"})
# eng_tweets = clean_tweets(eng_tweets)
# generate_wordcloud(eng_tweets)

all_tweets = collection.find()
all_tweets = clean_tweets(all_tweets)
generate_devices_plot(all_tweets)

coutry_tweets = collection.find({"place.country": {"$ne": ""}})
coutry_tweets = clean_tweets(coutry_tweets)
generate_country_plot(coutry_tweets)
