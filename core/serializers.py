from rest_framework import serializers
from .models import (
    Customer,
    Profession,
    DataSheet,
    Document,
)

class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = (
            'id', 'description', 'historical_data'
        )

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description', 'status')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    #data_sheet = serializers.SerializerMethodField()
    #data_sheet = serializers.PrimaryKeyRelatedField(read_only=True)  #return the number of the datasheet
    data_sheet = DataSheetSerializer()  #nested relationships
    #professions = serializers.StringRelatedField(many=True)  #return the name of the professions
    professions = ProfessionSerializer(many=True)  #nested relationships
    document_set = serializers.StringRelatedField(many=True)  #return the numbers of the doc


    class Meta:
        model = Customer
        fields = (
            'id', 'name', 'address', 'professions', 'data_sheet', 'active',
            'status_message', 'num_professions', 'document_set'
        )

    def get_num_professions(self, obj):
        return obj.num_professions()


    # def get_data_sheet(self, obj):
    #     return obj.data_sheet.description


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id', 'dtype', 'doc_number', 'customer'
        )
