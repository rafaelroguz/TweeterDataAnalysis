from quicksort import sort_list


# Lista de todas las aplicaciones desde las que se realizaron los tweets con sus conteos
element_list = []


# Verifica si la aplicación ya se está contabilizando o es una nueva
def is_in_list(element, field):
    # La lista está vacía
    if len(element_list) == 0:
        return False

    # Verifica que la aplicación se encuentre en la lista
    for elmt in element_list:
        if element == elmt[field]:
            return True

    return False


# Incrementamos el contador de tweets para una aplicación
def increment_element(element, field):
    idx = 0

    for elmt in element_list:
        if element == elmt[field]:
            element_list[idx]["count"] = element_list[idx]["count"] + 1
            return True

        idx = idx + 1

    return False


# Añadimos una nueva aplicación a la lista de fuentes de tweets
def add_element(element, field):
    new_element = {
        field: element,
        "count": 1
    }

    element_list.append(new_element)


# Imprime la lista de dispositivos con la cantidad de tweets de cada uno
def print_elements(elmt_list, field):
    for elmt in elmt_list:
        print(field + ": " + elmt[field])
        print("total: " + str(elmt["count"]))


# Organiza las aplicaciones desde las que se realizaron los tweets, aumentando el contendo de tweet por aplicación o
# añadiendo nuevas aplicaciones al conteo
def generate_source_list(tweets):
    #element_list = []
    field = "source"

    for tweet in tweets:
        if is_in_list(tweet[field], field):
            increment_element(tweet[field], field)
        else:
            add_element(tweet[field], field)

    new_list = sort_list(element_list, "count")

    print_elements(new_list, field)

    return new_list


# Organiza las aplicaciones desde las que se realizaron los tweets, aumentando el contendo de tweet por aplicación o
# añadiendo nuevas aplicaciones al conteo
def generate_country_list(tweets):
    element_list = []
    field = "country"

    for tweet in tweets:
        print(element_list[0])
        if not is_in_list(tweet["place"]["country"], field):
            add_element(tweet["place"]["country"], field)
        else:
            increment_element(tweet["place"]["country"], field)

    new_list = sort_list(element_list, "count")

    print_elements(new_list, field)

    return new_list


