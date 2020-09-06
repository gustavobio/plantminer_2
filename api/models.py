from django.db import models

class Names(models.Model):
    search_str = models.CharField(max_length=120, primary_key=True)
    def __str__(self):
        return self.search_str

class ShortNames(models.Model):
    short_name = models.CharField(max_length=40)
    def __str__(self):
        return self.short_name

class Details(models.Model):
    id = models.IntegerField(primary_key=True)
    scientific_name = models.CharField(max_length=120, null = True)
    family = models.CharField(max_length=20, null = True)
    genus = models.CharField(max_length=60, null=True)
    specific_epiteth = models.CharField(max_length=60, null=True)
    infra_epiteth = models.CharField(max_length=60, null=True)
    taxon_rank = models.CharField(max_length=20, null = True)
    authorship = models.CharField(max_length=120, null=True)
    taxon_status = models.CharField(max_length=60, null = True)
    name_status = models.CharField(max_length=60, null = True)
    search_str = models.ForeignKey(Names, on_delete=models.CASCADE)
    threat_status = models.CharField(max_length=70, null=True)
    establishment = models.CharField(max_length=15, null=True)
    endemism = models.CharField(max_length=15, null=True)
    life_form = models.CharField(max_length = 70, null=True)
    habitat = models.CharField(max_length = 120, null = True)
    vegetation_type = models.CharField(max_length = 500, null = True)
    occurrence = models.CharField(max_length = 170, null = True)
    domain = models.CharField(max_length = 120, null = True)
    short_name = models.ForeignKey(ShortNames, on_delete=models.CASCADE)

    def get_synonyms(self):
        rel = Relationships.objects.filter(accepted_id = self.id)
        return Details.objects.filter(id__in = rel.values_list('synonym_id', flat = True))

    def get_accepted(self):
        rel = Relationships.objects.filter(synonym_id = self.id)
        return Details.objects.filter(id__in = rel.values_list('accepted_id', flat = True))

class Relationships(models.Model):
    id = models.IntegerField(primary_key=True)
    synonym_id = models.ForeignKey(Details, related_name = 'synonym', on_delete = models.SET_NULL, null = True)
    accepted_id = models.ForeignKey(Details, related_name = 'accepted', on_delete = models.SET_NULL, null = True)
    accepted = models.BooleanField()
    relationship = models.CharField(max_length=200, null=True)

class Words(models.Model):
    word = models.CharField(max_length=30, primary_key=True)