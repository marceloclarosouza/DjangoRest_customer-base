from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http.response import HttpResponseNotAllowed
from .models import Customer, Profession, DataSheet, Document
from .serializers import (
    CustomerSerializer,
    ProfessionSerializer,
    DataSheetSerializer,
    DocumentSerializer,
)
from rest_framework import viewsets


class CustomerViewSet(viewsets.ModelViewSet):
    #queryset = Customer.objects.all()  #standard method
    serializer_class = CustomerSerializer

    def get_queryset(self):  ##replacing the GET method
        active_customers = Customer.objects.filter(active=True)
        return active_customers

    # def list(self, request, *args, **kwargs):
    #     customers = Customer.objects.filter(id=3)
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        customer = self.get_object()
        serializer = CustomerSerializer(customer)
        return Response(serializer)

    def create(self, request, *args, **kwargs):  ##Post method
        data = request.data
        customer = Customer.objects.create(
            name=data['name'],
            address=data['address'],
            data_sheet_id=data['data_sheet']
        )
        profession = Profession.objects.get(id=data['profession'])

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):  #replace de PUT FUNCTION full update
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    def partial_update(self, request, *args, **kwargs): #replacing PATH partial update
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)

        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):  #replacing de DELETE function
        customer = self.get_object()
        customer.delete()

        return Response('Object deleted')


    @action(detail=True)  ##decorator action
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        status = True if request.data['active'] == 'True' else False

        customers = Customer.objects.all()
        customers.update(active=status)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
