import json

from django.core.paginator import Paginator
from django.db.models import QuerySet, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

from Homework28_Django_CRUD import settings
from ads.models import User
from users.models import Location


# ----------------------------------------------------------------
# UserListView, UserCreateView, UserUpdateView, UserDeleteView
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle GET request to show list of users
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().get(request, *args, **kwargs)
        users: QuerySet = self.object_list.annotate(
            total_ads=Count('advertisement', filter=Q(
                advertisement__is_published=True))).\
            prefetch_related('locations').order_by('username')

        paginator = Paginator(users, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users_list = [{
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all())),
            'total_ads': user.total_ads,
        } for user in page_obj]

        return JsonResponse({
            'items': users_list,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }, safe=False, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle GET request to show one user
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().get(request, *args, **kwargs)
        user = get_object_or_404(User, pk=kwargs['pk'])
        return JsonResponse({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all().values_list('name', flat=True))),
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle POST request to create new user and create new location if it doesn't exist
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().post(request, *args, **kwargs)
        try:
            user_data = json.loads(request.body)
            user = User.objects.create(
                username=user_data['username'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                age=user_data['age'],
                role=user_data['role']
            )
            for location in user_data['locations']:
                location_obj, _ = Location.objects.get_or_create(name=location, defaults={
                    'lat': 11.110, 'lng': 15.011
                })
                user.locations.add(location_obj)

            user.save()
        except Exception:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all().values_list('name', flat=True))),
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'age', 'locations']

    def put(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle PUT request to update user and create new location if it doesn't exist
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().post(request, *args, **kwargs)
        try:
            user_data = json.loads(request.body)
            self.object.username = user_data['username']
            self.object.password = user_data['password']
            self.object.first_name = user_data['first_name']
            self.object.last_name = user_data['last_name']
            self.object.age = user_data['age']

            for location in user_data['locations']:
                location_obj, _ = Location.objects.get_or_create(name=location, defaults={
                    'lat': 11.110, 'lng': 15.011
                })
                self.object.locations.add(location_obj)

            self.object.save()
        except Exception:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        return JsonResponse({
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'locations': list(map(str, self.object.locations.all().values_list('name', flat=True))),
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        """
        View to handle DELETE request to delete user
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: JsonResponse
        """
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'})
