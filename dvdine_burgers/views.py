from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.core.paginator import Paginator


def home(request):
    return render(request, 'index.html')


def menu(request):
    return render(request, 'menu.html')


def contact(request):
    return render(request, 'contact.html')


def menu_view(request):
    """
    View used to paginate the menu page.
    Get 4 products per page.
    """
    starters = [{
        'name': 'Jamon & wild garlic croquetas',
        'image': 'images/jamon-and-wild-garlic-croquetas.png',
        'alt': 'Photo of a dish containing jamon and wild garlic croquetas.',
        'ingredients': 'milk, manchego, jamon iberico, eggs, panko breadcrumbs, olive oil, plain flour, wild garlic leaves.',
        },
        {
            'name': 'Fig burrata prosciutto tartine',
            'image': 'images/fig-burrata-prosciutto-tartine.png',
            'alt': 'Photo of 3 fig burrata prosciutto tartines.',
            'ingredients': 'prosciutto, figs, burrata, fig chutney, olive oil, balsamic vinegar, thyme, sourdough slices.',
        },
        {
            'name': 'Tomato bruschetta',
            'image': 'images/tomato-bruschetta.png',
            'alt': 'Photo with tomato bruschettas.',
            'ingredients': 'tomatoes, red onion, garlic, basil, balsamic vinegar, olive oil, baguette.',
        },
        {
            'name': 'Nutty chicken satay strips',
            'image': 'images/nutty-chicken-sate-strips.png',
            'alt': 'Photo dish of nutty chicken satay strips.',
            'ingredients': 'chicken, garlic, cucumber, soy sauce, lime, sweet chilli, curry powder, peanut butter.',
        },
    ]

    burgers = [
        {
            'name': 'DVDine Burger',
            'image': 'images/dvdine-burger.png',
            'alt': 'DVDine burger.',
            'ingredients': 'American cheese, bacon, gherkin, lettuce, red onion, special sauce, swiss cheese.',
        },
        {
            'name': 'American Cheese-Classic Single',
            'image': 'images/classic-single-cheese.png',
            'alt': 'Classic single cheese American burger.',
            'ingredients': 'American cheese, special sauce, lettuce, onion, tomato, house mayo.',
        },
        {
            'name': 'OG Burger',
            'image': 'images/og-burger.png',
            'alt': 'OG Burger.',
            'ingredients': 'American cheese, dirty mayo, gherkin, swiss cheese, white onion.',
        },
        {
            'name': 'Blue DVDine Burger',
            'image': 'images/blue-dvdine-burger.png',
            'alt': 'Blue DVDine Burger.',
            'ingredients': 'American cheese, bacon, blue cheese, blue cheese mayo, lettuce, jalapenos, red onion.',
        },
        {
            'name': 'Hell DVDine Burger',
            'image': 'images/hell-dvdine-burger.png',
            'alt': 'Hell DVDine Burger.',
            'ingredients': 'Bacon, habanero, ghost chilli sauce, jack cheese, lettuce, onion.',
        },
        {
            'name': 'Chilli Cheese Burger',
            'image': 'images/chilli-cheese-burger.png',
            'alt': 'Chilli cheese Burger.',
            'ingredients': 'American cheese, bacon, mustard, beef chilli, nacho cheese, jalapenos, sour cream, swiss.',
        },
        {
            'name': 'Chicken Buffalo Burger',
            'image': 'images/chicken-buffalo.png',
            'alt': 'Chicken buffalo burger.',
            'ingredients': 'Blue cheese mayo, lettuce, onion, grilled or fried chicken, buffalo sauce.',
        },
        {
            'name': 'Dirty Clucker Chicken Burger',
            'image': 'images/dirty-clucker.png',
            'alt': 'Dirty Clucker Chicken Burger.',
            'ingredients': 'Dirty mayo, double American cheese, gherkin, grilled or fried chicken.',
        },
    ]

    deserts = [
        {
            'name': 'Pistachio tiramisu',
            'image': 'images/pistachio-tiramisu.png',
            'alt': 'Pistachio tiramisu photo',
            'ingredients': 'Eggs, mascarpone, marsala, double cream, caster sugar, pistachio cream, amaretto, savoiardi sponge fingers.',
        },
        {
            'name': 'White chocolate cheesecake',
            'image': 'images/white-chocolate-cheesecake.png',
            'alt': 'White chocolate cheesecake photo',
            'ingredients': 'Digestive biscuits, butter, white chocolate, full-fat cream cheese, mascarpone, strawberries.',
        },
        {
            'name': 'Raspberry and pistachio parfait',
            'image': 'images/raspberry-pistachip-parfait.png',
            'alt': 'Raspberry  and pistachio parfait photo',
            'ingredients': 'Raspberries, eggs, sugar, double cream, pistachios',
        },
        {
            'name': 'Raspberry brûlée',
            'image': 'images/raspberry-brulee.png',
            'alt': 'Raspberry brûlée photo',
            'ingredients': 'Vanilla, lemon, double cream, raspberries, eggs, sugar',
        }
    ]

    drinks = [
        {
            'name': 'Still water',
            'image': 'images/water.png',
            'alt': 'Bottle of water unmarked',
            'ingredients': 'water',
        },
        {
            'name': 'Coke',
            'image': 'images/coke.png',
            'alt': 'Image of coca-cola bottle',
            'ingredients': 'Coca-Cola',
        },
        {
            'name': 'Lemonade soda',
            'image': 'images/lemonade.png',
            'alt': 'Photo of glass of lemonade.',
            'ingredients': 'Lemon, soda, honey',
        },
        {
            'name': 'Orange Juice',
            'image': 'images/orange-juice.png',
            'alt': 'Photo of glass of orange juice',
            'ingredients': 'Squeezed orange juice.',
        }
    ]

    category = request.GET.get('category', 'starters')
    page = request.GET.get('page', 1)

    # Select the list to paginate based on category
    if category == 'burgers':
        items = burgers
    elif category == 'deserts':
        items = deserts
    elif category == 'drinks':
        items = drinks
    else:
        # default to starters if category param is unknown
        category = 'starters'
        items = starters

    paginator = Paginator(items, 4)  # 4 items per page
    page_obj = paginator.get_page(page)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'menu.html', context)


def trigger_403(request):
    return HttpResponseForbidden(render(request, '403.html'))


def trigger_404(request):
    return HttpResponseNotFound(render(request, '404.html'))


def trigger_500(request):
    return HttpResponseServerError(render(request, '500.html'))
