from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from user.models import SubCity
from django.contrib import messages
from .form import PropertyPostForm, PropertyImageFormSet 
from .models import PropertyPost, PropertyImage, Category
from django.views.generic import DetailView, ListView
from django.db.models import Q


def home(request):
    property = PropertyPost.objects.all().order_by("-updated_at")
    try:
        property = property[:3]
        for pro in property:
            pro.first_image = pro.get_first_image()

    except Exception:
        property = None

    try:
        appart_id = Category.objects.filter(category='Apartment').first()
        apartments = PropertyPost.objects.filter(category=appart_id.id).all().order_by("-updated_at")
        apartments = apartments[:3]
        for pro in apartments:
            pro.first_image = pro.get_first_image()
    except Exception:
        apartments = None
    print(apartments)
    try:
        studio_id = Category.objects.filter(category='Studio').first()
        studios = PropertyPost.objects.filter(category=studio_id.id).all().order_by("-updated_at")
        studios = studios[:3]
        for pro in studios:
            pro.first_image = pro.get_first_image()
    except Exception:
        studios = None
    try:
        other_id = Category.objects.filter(category='Other').first()
        others = PropertyPost.objects.filter(category=other_id.id).all().order_by("-updated_at")
        others = others[:3]
        for pro in others:
            pro.first_image = pro.get_first_image()
    except Exception:
        others = None
    context = {
         "properties": property,
         "apartments": apartments,
         "studios": studios,
         "others": others,
         "title": 'Home'
    }
    return render(request, "property/home.html", context)


def about(request):
    return render(request, 'property/about.html')

@login_required
def propertyPost(request, property_id=None):
    if property_id:
        property_instance = get_object_or_404(PropertyPost, id=property_id, user=request.user)
        is_update = True
    else:
        property_instance = None
        is_update = False

    if request.method == 'POST':
        prop_form = PropertyPostForm(request.POST, instance=property_instance)
        prop_img_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.filter(property=property_instance))

        if prop_form.is_valid() and prop_img_formset.is_valid():
            property_instance = prop_form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()

            for form in prop_img_formset:
                if form.cleaned_data:
                    image = form.cleaned_data.get('image')
                    delete = form.cleaned_data.get('DELETE')
                    if image and not delete:
                        max_size = 10 * 1024 * 1024  # 10 MB
                        if image.size > max_size:
                            messages.warning(request, 'Image size exceeds the limit (10 MB).')
                            return redirect('propertypost')  # Redirect to the same page
                        PropertyImage.objects.create(property=property_instance, image=image)
                    elif delete and form.instance.pk:
                        form.instance.delete()

            messages.success(request, 'Your property has been posted!' if not is_update else 'Your property has been updated!')
            return redirect('profile')
    else:
        prop_form = PropertyPostForm(instance=property_instance)
        prop_img_formset = PropertyImageFormSet(queryset=PropertyImage.objects.filter(property=property_instance))

    context = {
        'prop_form': prop_form,
        'prop_img_formset': prop_img_formset,
        'title': f"{request.user.first_name} property post",
        'property_post': True,
        'property_instance': property_instance,
        'is_update': is_update
    }

    return render(request, 'property/property_post.html', context)


@login_required
def delete_property_post(request, property_id):
    property_instance = get_object_or_404(PropertyPost, id=property_id, user=request.user)
    if request.method == 'POST':
        property_instance.delete()
        messages.success(request, 'Your property has been deleted!')
        return redirect('profile')

    context = {
        'property_instance': property_instance,
        'title': f"Delete {property_instance.property}"
    }
    return render(request, 'property/confirm_delete.html', context)


# @login_required
# def propertyPost(request):
#     if request.method == 'POST':
#         prop_form = PropertyPostForm(request.POST)
#         prop_img_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())
        
#         if prop_form.is_valid() and prop_img_formset.is_valid():
#             property_instance = prop_form.save(commit=False)
#             property_instance.user = request.user

#             for form in prop_img_formset.cleaned_data:
#                 if form:
#                     image = form['image']
#                     # Limit the upload size
#                     max_size = 1 * 1024 * 1024  # 1 MB
#                     if image.size > max_size:
#                         messages.warning(request, 'Image size exceeds the limit (1 MB).')
#                         return redirect('propertypost')  # Redirect to the same page
#                     property_instance.save()
#                     PropertyImage.objects.create(property=property_instance, image=image)

#             messages.success(request, 'Your property has been posted!')
#             return redirect('profile')
#     else:
#         prop_form = PropertyPostForm()
#         prop_img_formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())
    
#     context = {
#         'prop_form': prop_form,
#         'prop_img_formset': prop_img_formset,
#         'title': f"{request.user.first_name} property post",
#         'property_post': True
#     }

#     return render(request, 'property/property_post.html', context)

def load_subcities(request):
    city_id = request.GET.get('city_id')
    subcities = SubCity.objects.filter(city_id=city_id).order_by('subcity')
    return JsonResponse(list(subcities.values('id', 'subcity')), safe=False)




class PropertyList(LoginRequiredMixin, ListView):
    """Lists all available active properties"""
    model = PropertyPost
    context_object_name = 'pros'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        property_posts = PropertyPost.objects.all()
        if search_query:
            property_posts = property_posts.filter(
                Q(property__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(price__icontains=search_query) |
                Q(details__icontains=search_query) |
                Q(subcity__subcity__icontains=search_query) |
                Q(subcity__city__city__icontains=search_query) |

                Q(category__category__icontains=search_query)
            )
        return property_posts.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        # Attach the first image to each property
        for property_post in context['pros']:
            property_post.first_image = property_post.get_first_image()

        if not self.get_queryset():
            messages.warning(self.request, f'Sorry, property not found for "{search_query}"')
        else:
            context['q'] = True

        context['search_query'] = search_query
        return context
    

class PropertyDetails(LoginRequiredMixin, DetailView):
    '''Detailed view of a single property'''
    model = PropertyPost
    context_object_name = "objs"
    template_name = 'property/propertypost_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyDetails, self).get_context_data(**kwargs) 
        images = PropertyImage.objects.filter(property=context['objs'].id).all()
        curr_user = self.request.user
        context['images'] = images
        context['first_image'] = images.first()
        context['curr_user'] = curr_user #to destingush a crnt user & owner
        return context 
