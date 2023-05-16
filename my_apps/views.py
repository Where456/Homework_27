import csv
import json
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from my_apps.models import Categories, Ads


def first_step(request):
    data = {
        'status': 'ok'
    }
    return JsonResponse(data, status=200)


def second_step(request):
    with open('datasets/ads.csv', 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        data = list(data)

    response = HttpResponse(content_type='text/plain; charset=utf-8')
    for row in data:
        row = [smart_str(cell) for cell in row]
        response.write('\t'.join(row) + '\n')

    return response

    # with open('datasets/ads.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         obj1 = Ads(name=row['name'], author=row['author'], price=row['price'], description=row['description'],
    #                address=row['address'])
    #         obj1.save()



def csv_to_json(request):
    data = []
    with open('datasets/categories.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

            # obj1 = Categories(name=row['name'])
            # obj1.save()

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    return JsonResponse(json_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):
    def get(self, request):
        categories = Categories.objects.all()

        search_text = request.GET.get("name", None)
        if search_text:
            categories = categories.filter(text=search_text)

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Categories.objects.create(**category_data)

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Categories.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()

        search_text = request.GET.get("name", None)
        if search_text:
            ads = ads.filter(text=search_text)

        response = []
        for i in ads:
            response.append({
                "id": i.pk,
                "name": i.name,
                "author": i.author,
                "price": i.price,
                "description": i.description,
                "address": i.address,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        ads_data = json.loads(request.body)

        ads = Ads.objects.create(**ads_data)

        return JsonResponse({
            "id": ads.pk,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
        })


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ads = self.get_object()
        except Ads.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": ads.pk,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
        })
