from django.db import models
from django.forms import ValidationError

class Voter(models.Model):
    class Meta:
        unique_together = (('cnic', 'family_no'),)
    cnic = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    family_no = models.CharField(max_length=12)
    statical_lock_code = models.CharField(max_length=50,default="null")
    series_number = models.CharField(max_length=50, default="fake")
    dob = models.DateField()
    email = models.EmailField(max_length=50, null=False, blank=False)

    def get_full_name(self):
        return f'{self.first_name}, {self.last_name}'

    def __str__(self):
        return f'{self.cnic} - {self.first_name}'


class Candidate(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.voter.get_full_name()}'


class Party(models.Model):
    name = models.CharField(max_length=10, default="test")  # short name
    full_name = models.CharField(max_length=50, default="test")  # long name
    description = models.CharField(max_length=255, default="test")  # description of party platform or ideology
    logo = models.ImageField(upload_to='party_logos/')  # file field to store party logo or symbol
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name}'


class Vote(models.Model):
    voter = models.OneToOneField(Voter, related_name='vote', on_delete=models.CASCADE)
    voted_to = models.ForeignKey(Party, related_name='votes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.voter} has voted for {self.voted_to.name}'













### older models
# class Voter(models.Model):
#     class Meta:
#         unique_together = (('cnic', 'family_no'),)
#     cnic = models.CharField(max_length=15, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     family_no = models.CharField(max_length=12)
#     statical_lock_code = models.CharField(max_length=50)
#     series_number = models.CharField(max_length=50)
#     dob = models.DateField()
#     email = models.EmailField(max_length=50, null=False, blank=False)
#     def get_full_name(self):
#         return f'{self.first_name}, {self.last_name}'

#     def __str__(self):
#         return f'{self.cnic} - {self.first_name}'

# class Candidate(models.Model):
#     voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
#     def __str__(self):
#         return f'{self.voter.get_full_name()} - {self.party.name}'


# class Party(models.Model):
#     name = models.CharField(max_length=10, default="test") # short name
#     full_name = models.CharField(max_length=50, default="test") # long name
#     description = models.CharField(max_length=255,default="test") # description of party platform or ideology
#     logo = models.ImageField(upload_to='party_logos/') # file field to store party logo or symbol
#     candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.full_name} <- {self.candidate}'



# class Vote(models.Model):
#     voter = models.OneToOneField(Voter, related_name='by', on_delete=models.CASCADE)
#     voted_to = models.ForeignKey(Party, related_name='to', on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.voter} has voted to {self.voted_to.name}'