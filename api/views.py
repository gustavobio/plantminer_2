from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework import status
from api.models import Names, ShortNames, Relationships, Details, Words
from django.contrib.postgres.search import TrigramDistance
from api.serializers import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import pickle
from fast_autocomplete import AutoComplete
import json
from .forms import ListForm
from django.forms.models import model_to_dict

def add_cors_headers(res):
    res["Access-Control-Allow-Origin"] = "*"
    res["Access-Control-Allow-Headers"] = "*"
    res["Access-Control-Allow-Credentials"] = "true"
    return res

def suggest_name(**kwargs):
    spp = kwargs.get('search_str').capitalize()
    suggested_name = (Names.objects.filter(search_str__startswith = spp[0])
                      .annotate(distance=TrigramDistance('search_str', spp),)
                      .filter(distance__lte=0.7)
                      .order_by('distance', 'search_str'))
    if suggested_name:
        matches = suggested_name.values_list('search_str', flat = True)
        dist = [fuzz.ratio(x, spp) for x in matches]
    if not suggested_name or max(dist) < 80:
        return None
    return suggested_name[dist.index(max(dist))]
        
@api_view(['GET', 'OPTIONS'])
#@permission_classes([IsAuthenticated])
def suggestion(request, *args, **kwargs):
    suggested_name = suggest_name(**kwargs)
    if suggested_name == None:
        content = {'details': 'not found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    serializer = NamesSerializer(suggested_name)
    return Response(serializer.data)
    
#@permission_classes([IsAuthenticated])
@api_view(['GET', 'OPTIONS'])
def details(request, *args, **kwargs):
    suggest = kwargs.get('suggest')
    try:        
        spp = kwargs.get('search_str').capitalize()
        spp_name = Names.objects.get(search_str = spp)
    except ObjectDoesNotExist:
        if suggest:
            spp_name = suggest_name(**kwargs)
            if spp_name == None:
                raise Http404
            else:
                spp_name = Names.objects.get(search_str = spp_name)
        else:
            content = {'details': 'not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if kwargs.get('family'):
        serializer = FamilySerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('genus'):
        serializer = GenusSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('specific_epiteth'):
        serializer = SpecificEpitethSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('scientific_name'):
        serializer = ScientificNameSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('infra_epiteth'):
        serializer = InfraSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('taxon_rank'):
        serializer = TaxonRankSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('authorship'):
        serializer = AuthorshipSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('taxon_status'):
        serializer = TaxonStatusSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('name_status'):
        serializer = NameStatusSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('threat_status'):
        serializer = ThreatStatusSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('establishment'):
        serializer = EstablishmentSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('endemism'):
        serializer = EndemismSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('life_form'):
        serializer = LifeFormSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('habitat'):
        serializer = HabitatSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('vegetation_type'):
        serializer = VegetationTypeSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('occurrence'):
        serializer = OccurrenceSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('domain'):
        serializer = DomainSerializer(spp_name.details_set.all(), many = True)
    elif kwargs.get('id'):
        serializer = IdSerializer(spp_name.details_set.all(), many = True)
    else:
        serializer = DetailsSerializer(spp_name.details_set.all(), many = True)
    res = Response(serializer.data)
    return add_cors_headers(res)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def expand_name(request, *args, **kwargs):
    try:
        short_name = ShortNames.objects.get(short_name = kwargs.get('short_name').capitalize())
    except ObjectDoesNotExist:
        raise Http404
    short_name = short_name.details_set.all()
    serializer = ShortNamesSerializer(short_name, many = True)
    return Response(serializer.data)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def shorten(request, *args, **kwargs):
    spp = Details.objects.filter(search_str = kwargs.get('search_str').capitalize()).first()
    if spp == None:
        content = {'details': 'not found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    if kwargs.get('author'):
        spp_split = spp.scientific_name.split()
    else:
        spp_split = spp.search_str.search_str.split()
    if len(spp_split) == 1:
        spp_split = spp_split[0]
    else:
        spp_split[0] = spp_split[0][0] + "."
        spp_split = ' '.join(spp_split)
    serializer = ShortenNameSerializer(spp_split)
    return Response(serializer.data)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def remove_authors(request, *args, **kwargs):
    spp = kwargs.get('taxon').split(" ")
    not_words = []
    for i,j in enumerate(spp, start = 0):
        word = Words.objects.filter(word = spp[i])
        if not word:
            not_words.append(spp[i])
    spp = [x for x in spp if x not in not_words]
    return Response({'taxon': ' '.join(spp)}, status=status.HTTP_200_OK)

with open('data.pickle', 'rb') as f:  
    names = pickle.load(f)

autocomplete_names = AutoComplete(words=names)

def autocomplete(request):
    if request.GET.get('term'):
        q = request.GET['term']
        data = autocomplete_names.search(word = q, max_cost = 3, size = 3)
        data = [s[0] for s in data if len(s[0]) >= len(q)]
        return HttpResponse(json.dumps([x.capitalize() for x in data]), 'application/json')
    else:
        return render(request, 'api/autocomplete.html')

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def synonyms(request, *args, **kwargs):
    spp = Details.objects.filter(search_str = kwargs.get('search_str').capitalize()).first()
    if spp == None:
        content = {'details': 'not found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    serializer = SynonymsSerializer(spp.get_synonyms(), many = True)
    return Response(serializer.data)

@api_view(['GET'])
def plantminer(request):
        form = ListForm()
        return render(request, 'api/plantminer.html', {'form': form})

@api_view(['GET','POST'])
def user_list(request):
    if request.method ==  'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            user_list = form.cleaned_data['list']
            suggest = form.cleaned_data['suggest']
            replace_synonyms = form.cleaned_data['replace_synonyms']
            user_list = user_list.split("\r\n")
            user_list = list(filter(None, user_list))
            user_list = [taxa.strip() for taxa in user_list]
            queryset = Details.objects.filter(search_str__in = user_list)
            def get_taxon(taxa):
                suggested_name = None
                taxa_processed = queryset.filter(search_str = taxa)
                if taxa_processed:
                    taxon_dict = taxa_processed.values()[0]
                    taxon_dict['search_str'] = taxa_processed.first().search_str.search_str
                else:
                    if suggest:
                        suggested_name = suggest_name_pm(taxa)
                    if suggested_name:
                        taxon_dict = model_to_dict(suggested_name.details_set.first())
                    else:
                        taxon_dict = model_to_dict(Details.objects.get(id = 31594))
                        taxon_dict = {x: None for x in taxon_dict}
                taxon_dict['search_str'] = taxa
                return taxon_dict
            processed_list = [get_taxon(item) for item in user_list]
            processed_list = json.dumps({"data": processed_list})
            data = {'test_data': processed_list}
            return render(request, 'api/user-list.html', data)
    else:
        form = ListForm()
        return render(request, 'api/plantminer.html', {'form': form})

def suggest_name_pm(taxon):
    if taxon == "":
        return None
    spp = taxon.capitalize()
    suggested_name = Names.objects.filter(search_str__startswith = spp[0]).annotate(distance=TrigramDistance('search_str', spp),).filter(distance__lte=0.7).order_by('distance', 'search_str')
    if suggested_name:
        matches = suggested_name.values_list('search_str', flat = True)
        dist = [fuzz.ratio(x, spp) for x in matches]
    if not suggested_name or max(dist) < 80:
        return None
    return suggested_name[dist.index(max(dist))]
