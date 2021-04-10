from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView
from blog.models import Post 

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


