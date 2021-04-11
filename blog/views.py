from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView
from blog.models import Post

from django.views.generic import FormView

from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render 

class PostLV(ListView):
    model = Post 
    context_object_name = 'posts'
    paginate_by = 4

class PostDV(DetailView):
    model = Post

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = 'myfirstblog'
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = "http://127.0.0.1:8000/"+f"{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'

# Tag
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html' 

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post 

    def get_queryset(self): 
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context 

# FormView 
class SearchFormView(FormView): 
    form_class = PostSearchForm 
    template_name = "blog/post_search.html"

    def form_valid(self, form): 
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form 
        context['search_term'] = searchWord 
        context['object_list'] = post_list 

        return render(self.request, self.template_name, context)

