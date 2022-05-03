from os import link
from django.shortcuts import render
import urllib.request
import json
from .forms import *
with urllib.request.urlopen("https://api.watchmode.com/v1/title/3173903/details/?apiKey=QQ8NN2k69xKxln2jsCX7TNcolVbkfPFPbMJar1Ai") as url:
        data = json.loads(url.read().decode())

def index(request):
    form = TitleForm()
    context = {'form': form}
    return render(request, 'search_dreamstream/index.html', context)

def results(request):
##
    if request.method == 'POST': 
        # Extracts info from api based on user input
        req = request.POST['search'].replace(' ','%20') # Removes spaces
        form_title = f"https://api.watchmode.com/v1/search/?apiKey=QQ8NN2k69xKxln2jsCX7TNcolVbkfPFPbMJar1Ai&search_field=name&search_value={req}" # Access the movie titles ID
        with urllib.request.urlopen(form_title) as url:
            title = json.loads(url.read().decode()) # Converts the title to ID number
        title_detail = f"https://api.watchmode.com/v1/title/{title['title_results'][0]['id']}/details/?apiKey=QQ8NN2k69xKxln2jsCX7TNcolVbkfPFPbMJar1Ai" # Returns single result The [0] changes which movie to select
        title_sources = f"https://api.watchmode.com/v1/title/{title['title_results'][0]['id']}/sources/?apiKey=QQ8NN2k69xKxln2jsCX7TNcolVbkfPFPbMJar1Ai"
        all_results = f"https://api.watchmode.com/v1/title/{title}/details/?apiKey=QQ8NN2k69xKxln2jsCX7TNcolVbkfPFPbMJar1Ai"
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
            index += 1
            if price == None: # Removes 'none' from values and replaces with 'subscription'
                price = 'Subscription'
                list_link[links] = [name.title() , price]
            if links not in list_link:
                    list_link[links] = [name.title() , f'${float(price)}']
        price_filtered = sorted(list_link.items(), key=lambda t:t[1][1]) # Filters the price from lowest to highest
        list_link = dict(price_filtered)


    context = {'details':details, 'sources': sources, 'allresults': all_results, 'links': list_link,}
    return render(request, 'search_dreamstream/results.html', context)





