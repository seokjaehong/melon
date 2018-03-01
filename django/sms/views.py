from django.shortcuts import render, redirect
import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


# Create your views here.
def send_sms(request):
    api_key = "NCSGLMHSQ2FTVZUA"
    api_secret = "6SJTTSSM27RIGTG3ERVXKFLKVWVEUHFI"

    if request.method == "POST":
        to_number = request.POST['to_number']
        contents = request.POST['contents']

        params = dict()
        params['type'] = 'sms'
        params['to'] = to_number
        params['from'] = '01044321237'
        params['text'] = contents

        cool = Message(api_key, api_secret)
        cool.send(params)

    return render(request, 'sms/send.html')