import json

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

from Homework28_Django_CRUD import settings
from ads.models import Category, Advertisement


# ----------------------------------------------------------------
# FBV
def check_response(request) -> JsonResponse:
    """
    CALL THE FUNCTION 'fill_database(' TO FILL DATABASE

    Function to give status OK response
    :param request: request
    :return: JsonResponse
    """
    return JsonResponse({
        'status': 'OK'
    }, status=200)


# ----------------------------------------------------------------
# CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle GET request to show list of categories
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().get(request, *args, **kwargs)
        categories: QuerySet = self.object_list.order_by('name')
        return JsonResponse([{
            'id': category.id,
            'name': category.name
        } for category in categories], safe=False, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle GET request to show one category
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().get(request, *args, **kwargs)
        category = get_object_or_404(Category, pk=kwargs['pk'])
        return JsonResponse({
            'id': category.id,
            'name': category.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle PATCH request to update category
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().post(request, *args, **kwargs)
        try:
            category_data = json.loads(request.body)
            self.object.name = category_data['name']
            self.object.save()
        except Exception:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url: str = '/'

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle DELETE request to delete category
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'})


# ----------------------------------------------------------------
# AdvertisementListView, AdvertisementCreateView, AdvertisementUpdateView, AdvertisementDeleteView
class AdvertisementListView(ListView):
    model = Advertisement

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle GET request to show list of advertisements
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().get(request, *args, **kwargs)
        advertisements: QuerySet = self.object_list.select_related('author', 'category').order_by('-price')

        paginator = Paginator(advertisements, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        advertisements_list = [{
            'name': advertisement.name,
            'price': advertisement.price,
            'description': advertisement.description,
            'image': advertisement.image.url if advertisement.image else None,
            'author': advertisement.author.username,
            'category': advertisement.category.name,
        } for advertisement in page_obj]

        return JsonResponse({
            'items': advertisements_list,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }, safe=False, status=200)


class AdvertisementDetailView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        """
        View to handle GET request to show one advertisement
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().get(request, *args, **kwargs)
        advertisement = get_object_or_404(Advertisement, pk=kwargs['pk'])
        return JsonResponse({
            'name': advertisement.name,
            'price': advertisement.price,
            'description': advertisement.description,
            'image': advertisement.image.url if advertisement.image else None,
            'author': advertisement.author.username,
            'category': advertisement.category.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementCreateView(CreateView):
    model = Advertisement
    fields = ['name', 'price', 'description', 'image', 'author_id', 'category_id']

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle POST request to create new advertisement
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        try:
            advertisement_data = json.loads(request.body)
            advertisement = Advertisement.objects.create(**advertisement_data)
        except Exception:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        return JsonResponse({
            'name': advertisement.name,
            'price': advertisement.price,
            'description': advertisement.description,
            'image': advertisement.image.url if advertisement.image else None,
            'author': advertisement.author.username,
            'author_id': advertisement.author_id,
            'category': advertisement.category.name,
            'category_id': advertisement.category_id,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementUpdateView(UpdateView):
    model = Advertisement
    fields = ['name', 'price', 'description', 'author', 'category']

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle PATCH request to update advertisement
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().post(request, *args, **kwargs)
        try:
            advertisement_data = json.loads(request.body)
            self.object.name = advertisement_data['name']
            self.object.price = advertisement_data['price']
            self.object.description = advertisement_data['description']
            self.object.author_id = advertisement_data['author_id']
            self.object.category_id = advertisement_data['category_id']
        except Exception:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'description': self.object.description,
            'author': self.object.author.username,
            'is_published': self.object.is_published,
            'category': self.object.category.name,
            'image': self.object.image.url if self.object.image else None
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url: str = '/'

    def delete(self, request, *args, **kwargs):
        """
        View to handle DELETE request to delete advertisement
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().delete(self, request, *args, **kwargs)
        return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementUploadImage(UpdateView):
    model = Advertisement
    fields = ['name', 'price', 'description', 'author', 'category']

    def post(self, request, *args, **kwargs):
        """
        View to handle POST request to upload image
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        self.object = self.get_object()
        try:
            self.object.image = request.FILES['image']
            self.object.save()
        except Exception:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'description': self.object.description,
            'author_id': self.object.author_id,
            'author': self.object.author.username,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'category': self.object.category.name,
            'image': self.object.image.url if self.object.image else None
        }, status=200)
