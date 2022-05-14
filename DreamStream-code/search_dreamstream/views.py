
from django.shortcuts import render
import urllib.request
import json
from .forms import *

def index(request):
    form = TitleForm()
    context = {'form': form}
    return render(request, 'search_dreamstream/index.html', context)

def results(request):
##
    if request.method == 'POST': 
        # Extracts info from api based on user input
        req = request.POST['search'].replace(' ','%20') # Removes spaces
        form_title = f"https://api.watchmode.com/v1/search/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH&search_field=name&search_value={req}" # Access the movie titles ID
        with urllib.request.urlopen(form_title) as url:
            title = json.loads(url.read().decode()) # Converts the title to ID number
        title_detail = f"https://api.watchmode.com/v1/title/{title['title_results'][0]['id']}/details/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH" # Returns single result The [0] changes which movie to select
        title_sources = f"https://api.watchmode.com/v1/title/{title['title_results'][0]['id']}/sources/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH"
        all_results = f"https://api.watchmode.com/v1/title/{title}/details/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH" # NOT NEEDED
        with urllib.request.urlopen(title_detail) as url:
            details = json.loads(url.read().decode())
        with urllib.request.urlopen(title_sources) as url:
            sources = json.loads(url.read().decode()) # Stores searched data
        
        # Get links , name, price separeted
        index = 0
        list_link = {}
        while index < len(sources):
            links = sources[index]['web_url']
            name = sources[index]['name']
            price = sources[index]['price']
            quality = sources[index]['format']
            index += 1
            if price == None: # Removes 'none' from values and replaces with 'subscription'
                    price = 'Subscription'
                    list_link[links] = [name.title() , price, quality]
            if links not in list_link:
                    list_link[links] = [name.title() , f'${float(price)}', quality]
        price_filtered = sorted(list_link.items(), key=lambda t:t[1][1])# Filters the price from lowest to highest
        list_link = dict(price_filtered)
        
        # Movie details - title, desc
        title_name = details['title'] # Stores title
        poster = details['poster'] # Cover poster
        trailer = details['trailer'] # Trailer link
        overview = details['plot_overview']
        rating = details['user_rating']
        release_date = details['release_date']

        # Similar Titles
        similar_results = {}
        result_counter = 1
        while result_counter < len(title['title_results']):
            similar_search = f"https://api.watchmode.com/v1/title/{title['title_results'][result_counter]['id']}/details/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH"
            with urllib.request.urlopen(similar_search) as url:
                    details_similar = json.loads(url.read().decode())
            similar_title = details_similar['title']
            similar_poster = details_similar['poster']
            result_counter += 1
            
            similar_results[similar_title] = similar_poster

        context = {
            'details':details, 
            'sources': sources, 
            'allresults': all_results, 
            'links': list_link,
            'title': title_name, 
            'poster': poster, 
            'trailer': trailer, 
            'description': overview, 
            'rating': rating, 
            'release': release_date,
            'similarresults': similar_results,
            }
    return render(request, 'search_dreamstream/results.html', context)



# Accepts 'sim' as a string which is used to search
def similar_results(request, sim):

        req = sim.replace(' ','%20') # Removes spaces
        form_title = f"https://api.watchmode.com/v1/autocomplete-search/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH&search_value={req}" # Access the movie titles ID
        with urllib.request.urlopen(form_title) as url:
            title = json.loads(url.read().decode()) # Converts the title to ID number
        
        title_detail = f"https://api.watchmode.com/v1/title/{title['title_results'][0]['id']}/details/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH" # Returns single result The [0] changes which movie to select
        title_sources = f"https://api.watchmode.com/v1/title/{title['title_results'][0]['id']}/sources/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH"
        all_results = f"https://api.watchmode.com/v1/title/{title}/details/?apiKey=4HtxbZ3jYTQDph06miqguyFFmFxPk0yLusYXHcDH" # NOT NEEDED
        with urllib.request.urlopen(title_detail) as url:
            details = json.loads(url.read().decode())
        with urllib.request.urlopen(title_sources) as url:
            sources = json.loads(url.read().decode()) # Stores searched data
        
        # Get links , name, price separeted
        index = 0
        list_link = {}
        while index < len(sources):
            links = sources[index]['web_url']
            name = sources[index]['name']
            price = sources[index]['price']
            quality = sources[index]['format']
            index += 1
            if price == None: # Removes 'none' from values and replaces with 'subscription'
                    price = 'Subscription'
                    list_link[links] = [name.title() , price, quality]
            if links not in list_link:
                    list_link[links] = [name.title() , f'${float(price)}', quality]
        price_filtered = sorted(list_link.items(), key=lambda t:t[1][1])# Filters the price from lowest to highest
        list_link = dict(price_filtered)
        
        # Movie details - title, desc
        title_name = details['title'] # Stores title
        poster = details['poster'] # Cover poster
        trailer = details['trailer'] # Trailer link
        overview = details['plot_overview']
        rating = details['user_rating']
        release_date = details['release_date']
    
        context = {
            'details':details, 
            'sources': sources, 
            'allresults': all_results, 
            'links': list_link,
            'title': title_name, 
            'poster': poster, 
            'trailer': trailer, 
            'description': overview, 
            'rating': rating, 
            'release': release_date,
            }
        return render(request, 'search_dreamstream/similar.html', context)




