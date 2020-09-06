from rest_framework import serializers
from api.models import Names, Details, Relationships, ShortNames, Words

class NamesSerializer(serializers.ModelSerializer):
     class Meta:
         model = Names
         fields = '__all__'

class DetailsSerializer(serializers.ModelSerializer):
    short_name = serializers.StringRelatedField()
    class Meta:
        model = Details
        fields = '__all__'

class ShortenNameSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'shortened_name': instance,
        }

class IdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['id']

class ShortNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = "__all__"

class SynonymsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = "__all__"

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = "__all__"

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["family"]

class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["genus"]

class SpecificEpitethSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["specific_epiteth"]

class ScientificNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["scientific_name"]

class InfraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["infra_epiteth"]

class TaxonRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["taxon_rank"]

class AuthorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ["authorship"]

class TaxonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['taxon_status']

class NameStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['name_status']

class ThreatStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['threat_status']

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['establishment']

class EndemismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['endemism']

class LifeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['life_form']

class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['habitat']

class VegetationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['vegetation_type']

class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['occurrence']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['domain']