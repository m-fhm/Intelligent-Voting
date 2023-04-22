from django.db import models
from django.forms import ValidationError


class Voter(models.Model):
    class Meta:
        unique_together = (('epic', 'aadhar'),)

    epic = models.CharField(max_length=10, primary_key=True)
    aadhar = models.CharField(max_length=12)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField(max_length=50, null=False, blank=False)

    def get_full_name(self):
        return f'{self.first_name}, {self.last_name}'

    def __str__(self):
        return f'{self.epic} - {self.first_name}'


# class Party(models.Model):
#     name = models.CharField(max_length=10) # short name
#     full_name = models.CharField(max_length=50) # long name
#     candidate = models.OneToOneField(Voter, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f'{self.full_name} <- {self.candidate}'

class Party(models.Model):
    name = models.CharField(max_length=10, default="test") # short name
    full_name = models.CharField(max_length=50, default="test") # long name
    description = models.CharField(max_length=255,default="test") # description of party platform or ideology
    logo = models.ImageField(upload_to='party_logos/',default="test") # file field to store party logo or symbol
    candidate = models.OneToOneField(Voter, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name} <- {self.candidate}'



class Vote(models.Model):
    voter = models.OneToOneField(Voter, related_name='by', on_delete=models.CASCADE)
    voted_to = models.ForeignKey(Party, related_name='to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.voter} has voted to {self.voted_to.name}'