import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pymongo import MongoClient
from wordcloud import STOPWORDS
from wordcloud import WordCloud

from sources.generate_plot_list import generate_source_list
from sources.generate_plot_list import generate_country_list
from sources.generate_plot_list import generate_language_list

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

    tweet_list = []
    for tweet in tweets:
        tweet_list.append(tweet["text"])

    text = "\n".join(tweet_list)

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
    mask = np.array(Image.open("sources/mario.png"))

    # Genera una nube de palabras. Las stopwords serán ignoradas y no apareceran en la gráfica
    wordcloud = WordCloud(width=1079, height=1623, max_words=10000, relative_scaling=1, stopwords=stopwords,
                          mask=mask, contour_color="white").generate(text)

    # Guardamos la nube de palabras generada en una imagen en la misma carpeta del script
    wordcloud.to_file("plots/wordcloud.png")


# Genera una gráfica de pastel con las aplicacciones desde donde se realizaron la mayoría de los tweets
def generate_app_plot(tweets):
    print("\nGenerando gráfica de dispositivos...\n")

    # Obtenemos una lista de objetos con el nombre de la aplicación y el número de tweets
    source_list = generate_source_list(tweets)

    # Dado que hay una enorme cantidad de aplicaciones, sólo vamos a mostrar las 7 más usadas, y las demás se contarán
    # dentro de "Otras" aplicaciones

    src_count = 0
    max_src = 7
    src_plot = []

    # Revisamos la lista de aplicaciones y generamos una con las más usadas para hacer los tweets
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

    # Nombre de las aplicaciones
    labels = []
    # Número de tweets por aplicación
    sizes = []

    # Añadimos la información para las etiquetas en la gráfica
    for src in src_plot:
        labels.append(src["source"])
        sizes.append(src["count"])


    # Ajusta el tamaño de la gráfica para que se adapte al tamaño del contenido
    plt.tight_layout()
    # Ajustamos el tamaño de la letra
    plt.rcParams["font.size"] = 7.0
    # Añadimos un título
    plt.title("Most used applications")
    # Generamos una gráfica de pastel
    plt.pie(sizes, labels=labels, shadow=True, radius=10, autopct="%0.2f%%")
    plt.axis("equal")

    # Guardamos la gráfica en una imagen en la misma carpeta que este script
    plt.savefig("plots/applications.png", dpi=300)

    plt.show(block=False)
    plt.close()

# Genera una gráfica de barras con los países que más tweets realizaron.
# Dado que no todos los tweets tienen información de ubicación, esta lista de tweets tiene alrededor de 300+ tweets
def generate_country_plot(tweets):
    print("\nGenerando gráfica de países...\n")

    # Obtenemos una lista de objetos que contiene el nombre del país con el número de tweets
    country_list = generate_country_list(tweets)

    # Dado que la lista de países es bastante grande, sólo mostraremos los primeros 10 con más tweets

    country_count = 0
    max_country = 10
    country_chart = []

    # Generamos una lista con los 10 países que más tweetearon
    for country in country_list:
        if country_count < max_country:
            country_chart.append(country)
            country_count = country_count + 1

    # Nombre de los países
    labels = []
    # Número de tweets
    sizes = []

    # Añadimos la información a las etiquetas de la gráfica de barras
    for country in country_chart:
        labels.append(country["country"])
        sizes.append(country["count"])

    # Prepara la información necesaria para generar la gráfica de barras
    y_pos = np.arange(len(labels))
    plt.yticks(y_pos, labels)

    # Añadimos una etiqueta al eje vertical
    plt.ylabel("Country")
    # Añadimos una etiqueta al eje horizontal
    plt.xlabel("# of tweets")
    # Añadimos un título
    plt.title("Top 10 countries with the most tweets")
    # Ajusta el tamaño de la gráfica para que se adapte al tamaño del contenido
    plt.tight_layout()

    # Añade una etiqueta que muestra el número de tweets a lada de cada barra
    for i, v in enumerate(sizes):
        plt.text(v + 5, i - 0.1, str(v), color="#1F76B3", fontweight="bold")

    # Genera la gráfica
    plt.barh(y_pos, sizes)

    # Guarda la gráfica como imagen en la misma carpeta que este script
    plt.savefig("plots/countries.png", dpi=300)

    plt.show(block=False)
    plt.close()

# Genera una gráfica de pastel que representa los idiomas más usados en los tweets
def generate_language_plot(tweets):
    print("\nGenerando gráfica de idiomas...\n")

    # Obtenemos una lista de objetos con las siglas del idioma y el número de tweets en ese idioma
    language_list = generate_language_list(tweets)

    # Dado que hay una enorme cantidad de idiomas, sólo tomaremos un número limitado, definido por la variable max_lang
    lang_count = 0
    max_lang = 7
    lang_plot = []

    # Revisamos la lista de aplicaciones y generamos una con las más usadas para hacer los tweets
    for lang in language_list:
        if lang_count < max_lang:
            lang_plot.append(lang)
            lang_count = lang_count + 1

        if lang_count == max_lang:
            lang_plot.append({
                "language": "Others",
                "count": 1
            })

            lang_count = lang_count + 1

        if lang_count > max_lang:
            lang_plot[max_lang]["count"] = lang_plot[max_lang]["count"] + 1

    # Listado de idiomas a usar como etiquetas en la gráfica
    labels = []
    # Número de tweets por idioma
    sizes = []

    # Añadimos la información para las etiquetas en la gráfica
    for lang in lang_plot:
        labels.append(lang["language"])
        sizes.append(lang["count"])

    # Ajusta el tamaño de la gráfica para que se adapte al tamaño del contenido
    plt.tight_layout()
    # Ajustamos el tamaño de la letra
    plt.rcParams["font.size"] = 7.0
    # Añadimos un título
    plt.title("Most used languages")
    # Generamos una gráfica de pastel
    plt.pie(sizes, labels=labels, shadow=True, radius=10, autopct="%0.2f%%")
    plt.axis("equal")

    # Guardamos la gráfica en una imagen en la misma carpeta que este script
    plt.savefig("plots/languages.png", dpi=300)

    plt.show(block=False)
    plt.close()

# MAIN BODY------------------------------------------------------------------------------------------------------------#

# Recupera todos los tweets en idioma inglés
eng_tweets = collection.find({"lang": "en"})
eng_tweets = clean_tweets(eng_tweets)
generate_wordcloud(eng_tweets)

# Recupera todos los tweets
all_tweets = collection.find()
all_tweets = clean_tweets(all_tweets)
generate_app_plot(all_tweets)

# Recupera los tweets que contengan información en el campo "place.country"
coutry_tweets = collection.find({"place.country": {"$ne": ""}})
coutry_tweets = clean_tweets(coutry_tweets)
generate_country_plot(coutry_tweets)

generate_language_plot(all_tweets)
