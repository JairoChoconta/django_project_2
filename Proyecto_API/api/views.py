from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Company
import json


# Create your views here.

class CompanyView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0): #Se deja predeterm. en 0 para que las entregue todas en dado caso de que no se especifique un id (y se va al else), pero si le decimos un id específico, entonces entra al if y nos lo filtra.
        if (id>0):
            companies = list(Company.objects.filter(id=id).values())
            if len(companies) > 0: #...si existe ese id que buscamos entonces:
                company = companies[0] # porque aquí ya sabemos del if externo que obtendremos solo una compañía, y esa única estará filtrada en la list en la posición cero.
                datos = {'message': 'Success', 'company': company}
            else:
                datos = {'message': 'Company not found...'}
            return JsonResponse(datos)
        else:
            companies = list(Company.objects.values()) #Aquí serializamos a JSON el tipo QuerySet
            if len(companies) > 0:
                datos = {'message':'Success', 'companies': companies}
            else:
                datos = {'message': 'Companies not found...'}
            return JsonResponse(datos)
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        Company.objects.create(name=jd['name'], website=jd['website'], foundation=jd['foundation'])
        datos={'message':'Success'}
        return JsonResponse(datos)
    def put(self, request, id): #porque necesitaremos el id de la compañía a modificar
        jd = json.loads(request.body)
        companies = list(Company.objects.filter(id=id).values())
        if len(companies) > 0:
            company = Company.objects.get(id=id) #esta vez si tengo la certeza de encontrarlo get devuelve un error si no lo encuentra, filter no devuelve errores.
            company.name=jd['name']
            company.website=jd['website']
            company.foundation=jd['foundation']
            company.save()
            datos={'message':'Success'}
        else:
            datos = {'message': 'Companies not found...'}
        return JsonResponse(datos)
    def delete(self, request, id):
        companies = list(Company.objects.filter(id=id).values())
        if len(companies) > 0:
            Company.objects.filter(id=id).delete()
            datos = {'message': 'Success'}
        else:
            datos = {'message': 'Company not found...'}
        return JsonResponse(datos)