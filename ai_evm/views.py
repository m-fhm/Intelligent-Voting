from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings 
from django.core.mail import EmailMessage 
from django.db.models import Count
from threading import Thread
from mailjet_rest import Client
from .models import Voter, Party, Vote, Candidate
from .forms import VoterForm, PartyForm, CandidateForm



'''
1. Persons detections
2. Mask detection
3. Face Recognition
4. Vote 
'''

# fetch only firstnames for face recognition phase
cnic = Voter.objects.values_list('cnic', flat=True)

def index(request):
    return render(request, 'ore.html')

def refresh(request):
    request.session.flush()
    request.method = 'GET'
    return redirect('start')


def init_session(request):
    request.session['phase_1'] = False
    request.session['phase_2'] = False
    request.session['phase_3'] = False
    request.session['phase_4'] = False


def start(request):
    # check for app state is initialized or not
    if 'phase_1' not in request.session:
        init_session(request)

    if request.method == 'POST':
        if not request.session['phase_1']:
            # get # of persons
            from detect_person.camera import PERSON_COUNT 
            request.session['persons'] = PERSON_COUNT
            print('PERSONS:', PERSON_COUNT)

            if PERSON_COUNT == 1:
                messages.success(request, 'Persons Detection Phase completed')
                request.session['phase_1'] = True
                return render(request, 'index.html', {'stream': 'detect_mask'})
            else:
                messages.error(request, 'More than one person not allowed in the Polling Booth!')
                return render(request, 'index.html', {'stream': 'detect_person'})

        elif not request.session['phase_2']:
            # get mask status
            from detect_mask.camera import HAS_MASK
            request.session['has_mask'] = HAS_MASK
            print('HAS_MASK:', HAS_MASK)

            if not HAS_MASK:
                # mark as complete & render phase-3
                messages.success(request, 'Mask Detection Phase completed')
                request.session['phase_2'] = True
                return render(request, 'index.html', {'stream': 'recognize_face'})
            else:
                # revert back to same phase
                messages.warning(request, 'Please remove your mask!')
                return render(request, 'index.html', {'stream': 'detect_mask'})
        
        elif not request.session['phase_3']:
            # get face name
            from recognize_face.camera import FACE_NAME
            request.session['face_name'] = FACE_NAME
            print('FACE_NAME:', FACE_NAME)

            if FACE_NAME in cnic:
                # mark as complete & move to phase_4 (voting)
                messages.success(request, 'Face Recognition Phase completed')
                request.session['phase_3'] = True
                # if alread voted clear session & send back to main page
                request.method = 'GET'
                return start(request)
            else:
                messages.error(request, 'Your nomination is not in this constituency!')
                return render(request, 'index.html', {'stream': 'recognize_face'})

        elif not request.session['phase_4']:
            voted_to = Party.objects.get(name=request.POST['voted_to'])
            voter = Voter.objects.get(cnic=request.session['face_name'])
            Vote(voter=voter, voted_to=voted_to).save()
            Thread(target= success, args=(voter, voted_to.full_name)).start()
            # return JsonResponse(dict(request.POST))
            messages.success(request, 'Thank for you vote! Your vote has been received!')
            request.session.flush()
            request.method = 'GET'
            return start(request)
        
        else:
            return HttpResponse('No suitable POST condition satisfied!')

    else:
        if not request.session['phase_1']:
            return render(request, 'index.html', context = {'stream': 'detect_person'})
        if not request.session['phase_2']:
            return render(request, 'index.html', context = {'stream': 'detect_mask'})
        if not request.session['phase_3']:
            return render(request, 'index.html', context = {'stream': 'recognize_face'})
        if not request.session['phase_4']:
            if len(Vote.objects.filter(voter__cnic=request.session['face_name'])) > 0:
                messages.error(request, 'Sorry, You have already voted!')
                request.session.flush()
                request.method = 'GET'
                return start(request)
            else:
                return render(request, 'index.html', {'pts': Party.objects.all()})




def dbg(request):
    return JsonResponse(dict(request.session))


def success(voter, voted_to):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "nktchhn1997@gmail.com",
            "Name": "Ankit"
        },
        "To": [
            {
            "Email": voter.email, # In future make sure to query by pk
            "Name": voter.first_name
            }
        ],
        "Subject": "Greetings AI-EVM.",
        "TextPart": "Your vote has been counted",
        "HTMLPart": f"<h3>Dear {voter.first_name}, This mail is to remind you that your vote has been taken into consideration! <br> You have voted to {voted_to} </h3><br />Thank You!",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)

    # voter CRUD Starts here
def voter_list(request):
    voters = Voter.objects.all()
    return render(request, 'voters/voter_list.html', {'voters': voters})

def voter_create(request):
    if request.method == 'POST':
        form = VoterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voter_list')
    else:
        form = VoterForm()
    return render(request, 'voters/add_voter.html', {'form': form})

def voter_detail(request, pk):
    voter = get_object_or_404(Voter, pk=pk)
    return render(request, 'voters/voter_detail.html', {'voter': voter})

def voter_update(request, pk):
    voter = get_object_or_404(Voter, pk=pk)
    if request.method == 'POST':
        form = VoterForm(request.POST, instance=voter)
        if form.is_valid():
            form.save()
            return redirect('voter_list')
    else:
        form = VoterForm(instance=voter)
    return render(request, 'voters/add_voter.html', {'form': form})

def voter_delete(request, pk):
    voter = get_object_or_404(Voter, pk=pk)
    if request.method == 'POST':
        voter.delete()
        return redirect('voter_list')
    return render(request, 'voters/delete_voter.html', {'voter': voter})


# Party section starts here

def party_list(request):
    parties = Party.objects.all()
    return render(request, 'parties/party_list.html', {'parties': parties})

def party_create(request):
    if request.method == 'POST':
        form = PartyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('party_list')
    else:
        form = PartyForm()
    return render(request, 'parties/party_add.html', {'form': form})

def party_update(request, pk):
    party = get_object_or_404(Party, pk=pk)
    if request.method == 'POST':
        form = PartyForm(request.POST, request.FILES, instance=party)
        if form.is_valid():
            form.save()
            return redirect('party_list')
    else:
        form = PartyForm(instance=party)
    return render(request, 'parties/party_add.html', {'form': form})

def party_delete(request, pk):
    party = get_object_or_404(Party, pk=pk)
    party.delete()
    return redirect('party_list')

#--------Candidate CURD
#---------------

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'candidate/candidate_list.html', {'candidates': candidates})

def candidate_create(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'candidate/candidate_form.html', {'form': form})

def candidate_update(request, cnic):
    candidate = get_object_or_404(Candidate, voter__cnic=cnic)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('candidate_list')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'candidate/candidate_form.html', {'form': form, 'candidate': candidate})

def candidate_delete(request, cnic):
    candidate = get_object_or_404(Candidate, voter__cnic=cnic)
    if request.method == 'POST':
        candidate.delete()
        return redirect('candidate_list')
    return render(request, 'candidate/candidate_confirm_delete.html', {'candidate': candidate})

# vote counter each party 
def party_votes_view(request):
    # Query to count the total votes for each party
    party_votes = Party.objects.annotate(total_votes=Count('votes'))

    context = {
        'party_votes': party_votes
    }

    return render(request, 'voters/vote_count.html', context)