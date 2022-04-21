from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import FilmModelForm
from movies.models import Film, Genre, Attachment


def index(request):
    """Metoda připravuje pohled pro domovskou stránku - šablona index.html"""

    # Uložení celkového počtu filmů v databázi do proměnné num_films
    #num_films =
    # Do proměnné films se uloží 3 filmy uspořádané podle hodnocení (sestupně)
    #films =

    """ Do proměnné context, která je typu slovník (dictionary) uložíme hodnoty obou proměnných """
    context = {
        'num_films': Film.objects.all().count(),
        'films': Film.objects.order_by('-release_date')[:3],
        'top_ten' : Film.objects.order_by('-rate')[:10],
        'genres_list' : Genre.objects.order_by('name').all()
    }

    """ Pomocí metody render vyrendrujeme šablonu index.html a předáme ji hodnoty v proměnné context k zobrazení """
    return render(request, 'index.html', context=context)


""" Třída dědí z generické třídy ListView, která umí vypsat z databáze všechny objekty určeného modelu """


class FilmListView(ListView):
    # Nastavení požadovaného modelu
    model = Film
    # Pojmenování objektu, v němž budou šabloně předána data z modelu (tj. databázové tabulky)
    context_object_name = 'films_list'
    # Umístění a název šablony
    template_name = 'film/list.html'

    def get_queryset(self):
        if 'genre_name' in self.kwargs:
            return Film.objects.filter(genres__name=self.kwargs['genre_name']).all()
        else:
            return Film.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['num_films']= len(self.get_queryset())
        if 'genre_name' in self.kwargs:
            context['view_title'] = self.kwargs['genre_name']
        else:
            context['view_title'] = 'Filmy'
        return context


""" Třída dědí z generické třídy DetailView, která umí vypsat z databáze jeden objekt určeného modelu """


class FilmDetailView(DetailView):
    # Nastavení požadovaného modelu
    model = Film
    # Pojmenování objektu, v němž budou šabloně předána data z modelu (tj. databázové tabulky)
    context_object_name = 'film_detail'
    # Umístění a název šablony
    template_name = 'film/detail.html'


class GenreListView(ListView):
    model = Genre
    context_object_name = 'film_genre'
    template_name = 'blocks/genres_list.html'
    queryset = Genre.objects.all()


class NewFilmListView(ListView):
    model = Film
    template_name = 'blocks/new_films.html'
    context_object_name = 'films'
    queryset = Film.objects.order_by('-release_date').all()

class FilmCreate(CreateView):
    model = Film
    fields = ['title', 'plot', 'release_date', 'runtime', 'poster', 'rate', 'genres']
    initial = {'rate': '5'}

class FilmUpdate(UpdateView):
    model = Film
    template_name = 'movies/film_bootstrap_form.html'
    form_class = FilmModelForm
    #fields = '__all__'

class FilmDelete(DeleteView):
    model = Film
    success_url = reverse_lazy('films')



