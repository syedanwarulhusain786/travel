from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
def EmailMessage_api(subject,content,reciever):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = subject
    sender = {"name":"Support","email":"support@niranaya.com"}
    html_content = content
    to = reciever
    params = {"parameter":"My param value","subject":"New Subject"}
    
    # attachment=[
    #         {
    #             "content": attachment,
    #             "name": "file.xlsx"
    #         }
    #     ]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to,html_content=html_content, sender=sender, subject=subject)
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        return False

def EmailMessage_api_attach(subject,content,reciever,attach):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = subject
    sender = {"name":"Support","email":"support@niranaya.com"}
    html_content = content
    to = reciever
    params = {"parameter":"My param value","subject":"New Subject"}
    
    attachment=[
            {
                "content": attach,
                "name": "offer.pdf"
            }
        ]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to,html_content=html_content, sender=sender, subject=subject,attachment=attachment)
    # api_instance.send_transac_email(send_smtp_email)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        return False




# import base64

# with open('pdf.xlsx', 'rb') as file:
#     encoded_file = base64.b64encode(file.read()).decode('utf-8')
# tr=EmailMessage_api_attach('email_subject','email_body',[{"email":'syedanwarulhusain68@gmail.com',"name":"shabi husain"}],encoded_file)

# print(tr)