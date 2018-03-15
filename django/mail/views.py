from django.core.mail import EmailMessage
from django.shortcuts import render

from django.core.mail import send_mail

from mail.forms import UploadFileForm


# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def send_email(request):
    # 1. send_mail
    if request.method == "POST":
        to_mail_address = [request.POST['mail_address']]
        title = request.POST['title']
        contents = request.POST['contents']
        from_mail_address = 'devhsj@gmail.com'

        send_mail(title, contents, from_mail_address, to_mail_address)

    # 2. EmailMessage
    # if request.method == "POST":
    #     # form = UploadFileForm(request.POST, request.FILES)
    #     # if form.is_valid():
    #     #     handle_uploaded_file(request.FILES['file'])
    #     # else:
    #     #     form = UploadFileForm()
    #
    #     to_mail_address = [request.POST['mail_address']]
    #     title = request.POST['title']
    #     contents = request.POST['contents']
    #
    #     email = EmailMessage(title, contents, to=[to_mail_address])
    #     email.attach_file('../.media/artist/suji.jpg')
    #     email.send()
    return render(request, 'mail/send.html')
