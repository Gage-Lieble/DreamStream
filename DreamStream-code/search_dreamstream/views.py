
from django.shortcuts import render
import urllib.request
import json
from .forms import *

api_key = "LoFyrtSVsn0C1Up2hVUgcoJZWIdLAHtLFFDN4ghd"
def index(request):

    featured_movies_list = ['The%20Batman', 'Firestarter', 'Spiderman%20no%20way%20home', 'Us', 'Step%20brothers', 'Dude%20wheres%20my%20car', 'Pet%20sematary', 'Star%20Wars:%20The%20Rise%20of%20Skywalker', 'Free%20Guy', 'Conjuring']
    featured_dict = {}
    for items in featured_movies_list:
        url_results = f"https://api.watchmode.com/v1/autocomplete-search/?apiKey={api_key}&search_value={items}"
        with urllib.request.urlopen(url_results) as url:
                output = json.loads(url.read().decode())
        poster_featured = output['results'][0]['image_url']
        title_featured = output['results'][0]['name']
        featured_dict[poster_featured]=title_featured
    form = TitleForm()
    usern = request.user
    context = {'form': form, 'usern': str(usern), 'featured': featured_dict}
    return render(request, 'search_dreamstream/index.html', context)

def results(request):

    if request.method == 'POST': 
        # Extracts info from api based on user input
        req = request.POST['search'].replace(' ','%20') # Removes spaces
        form_title = f"https://api.watchmode.com/v1/autocomplete-search/?apiKey={api_key}&search_value={req}" # Access the movie titles ID
        with urllib.request.urlopen(form_title) as url:
            title = json.loads(url.read().decode()) # Converts the title to ID number
        
        if len(title['results']) > 0:
            title_detail = f"https://api.watchmode.com/v1/title/{title['results'][0]['id']}/details/?apiKey={api_key}" # Returns single result The [0] changes which movie to select
            title_sources = f"https://api.watchmode.com/v1/title/{title['results'][0]['id']}/sources/?apiKey={api_key}"
            all_results = f"https://api.watchmode.com/v1/title/{title}/details/?apiKey={api_key}" # NOT NEEDED
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
                        price = 'Subs'
                        list_link[links] = [name.title() , price, quality]
                if links not in list_link:
                        list_link[links] = [name.title() , f'${float(price)}', quality]
            price_filtered = sorted(list_link.items(), key=lambda t:t[1][1])# Filters the price from lowest to highest
            list_link = dict(price_filtered)
            
            # Movie details - title, desc
            title_name = details['title'] # Stores title
            poster = details['poster'].replace('https://cdn.watchmode.com/posters/', '') # Cover poster
            trailer = details['trailer'] # Trailer link
            overview = details['plot_overview']
            rating = details['user_rating']
            release_date = details['release_date']

            # Similar Titles
            similar_results = {}
            result_counter = 1
            while result_counter < len(title['results']):
                try:
                    similar_search = f"https://api.watchmode.com/v1/title/{title['results'][result_counter]['id']}/details/?apiKey={api_key}"
                    with urllib.request.urlopen(similar_search) as url:
                            details_similar = json.loads(url.read().decode())
                except: 
                    pass
                similar_title = details_similar['title']
                similar_poster = details_similar['poster']
                result_counter += 1
                
                similar_results[similar_title] = similar_poster
            usern = request.user
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
                'usern': str(usern),
                
                }
            return render(request, 'search_dreamstream/results.html', context)
        else:
            form = TitleForm(request.POST, initial={'search': req})
            context ={'usersearch': req, 'form': form}
            return render(request, 'search_dreamstream/404.html', context)


# Accepts 'sim' as a string which is used to search
def similar_results(request, sim):

        req = sim.replace(' ','%20') # Removes spaces
        form_title = f"https://api.watchmode.com/v1/autocomplete-search/?apiKey={api_key}&search_value={req}" # Access the movie titles ID
        with urllib.request.urlopen(form_title) as url:
            title = json.loads(url.read().decode()) # Converts the title to ID number
        
        title_detail = f"https://api.watchmode.com/v1/title/{title['results'][0]['id']}/details/?apiKey={api_key}" # Returns single result The [0] changes which movie to select
        title_sources = f"https://api.watchmode.com/v1/title/{title['results'][0]['id']}/sources/?apiKey={api_key}"
        all_results = f"https://api.watchmode.com/v1/title/{title}/details/?apiKey={api_key}" # NOT NEEDED
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
                    price = 'Subs'
                    list_link[links] = [name.title() , price, quality]
            if links not in list_link:
                    list_link[links] = [name.title() , f'${float(price)}', quality]
        price_filtered = sorted(list_link.items(), key=lambda t:t[1][1])# Filters the price from lowest to highest
        list_link = dict(price_filtered)
    
        # Movie details - title, desc
        title_name = details['title'] # Stores title
        poster = details['poster'].replace('https://cdn.watchmode.com/posters/', '') # Cover poster
        trailer = details['trailer'] # Trailer link
        overview = details['plot_overview']
        rating = details['user_rating']
        release_date = details['release_date']
        usern = request.user
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
            'usern': str(usern)
            }
        return render(request, 'search_dreamstream/similar.html', context)


