from django.shortcuts import render, redirect
from apiclient import discovery

API_KEY = os.environ.get('BOOKS_API_KEY')
books = discovery.build('books', 'v1', developerKey=API_KEY)

def home(request):
    text  = ["'Never trust anyone who has not brought a book with them.'", "'Until I feared I would lose it, I never loved to read. One does not love breathing.'", "'Books are mirrors: you only see in them what you already have inside you.'" ]
    authors = ['Lemony Snicket, Horseradish', 'Harper Lee, To Kill a Mockingbird', 'Carlos Ruiz Zafón, The Shadow of the Wind']
    quotes = zip(text, authors)

    displaybooks = 'no'
    data = {}

    # Searching for a book
    if 'query' in request.GET:
        displaybooks = 'yes'
        query = request.GET['query']
        data = books.volumes().list(q=query, langRestrict="en", maxResults=4).execute()
        for book in data['items']:
            try:
                book['volumeInfo']['authors'] = ", ".join(book['volumeInfo']['authors'])
            except:
                continue
        data = data['items']

    return render(request, 'home.html', {'books': data, 'displaybooks': displaybooks, 'quotes': quotes})

def details(request, book_id):
    book = books.volumes().get(volumeId=book_id).execute()
    book['volumeInfo']['authors'] = ", ".join(book['volumeInfo']['authors'])
    result = book['volumeInfo']

    # Calculate time required to finish the book
    words = result['pageCount'] * 275
    time_hours = words / 250 / 60
    time_returned = '{0:2.0f} hours and {1:02.0f} minutes'.format(*divmod(time_hours * 60, 60))

    # Redirect to main search page when a book is searched
    if 'query' in request.GET:
        q = "/?query=" + request.GET['query'].replace(" ", "+")
        return redirect(q)


    return render(request, 'details.html', {'book': result, 'time_hours': time_hours, 'time': time_returned, 'words': words, 'days': time})


def about(request):
    # Redirect to main search page when a book is searched
    if 'query' in request.GET:
        q = "/?query=" + request.GET['query'].replace(" ", "+")
        return redirect(q)

    return render(request, 'about.html')