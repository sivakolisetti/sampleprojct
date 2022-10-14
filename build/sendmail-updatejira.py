#==============================================================================================================================================
#      FILE NAME: sendmail-updatejira.py
#      USAGE: python sendmail-updatejira.py ticket_id userPrincipalName
#      ENVIRONMENT VARIABLES: JIRA_BASIC_AUTH,SENDGRID_API_KEY,SENDGRID_TEMPLATE_ID,ARM_CLIENT_ID,ARM_CLIENT_SECRET,ARM_TENANT_ID
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#==============================================================================================================================================

import requests
import json
import os,sys
import hcl2
import sendgrid
from sendgrid.helpers.mail import *

#==============================================================================================================================================
#Functions:
#Function to update jira ticket status to "closed"
#==============================================================================================================================================
def update_jiraticket_status(comment):
    jira_status_api='https://schneider-electric-se.atlassian.net/rest/api/2/issue/{0}/transitions'.format(ticket_id)
    headers={
         "Authorization": "Basic {0}".format(jiraapiToken),
         "Content-Type": "application/json"
        }
    data_jira = {"update": {"comment": [{"add": {"body": comment}}]},"transition": {"id": 61 }}
    issue=requests.post(jira_status_api,headers=headers,data=json.dumps(data_jira))
    if(issue.status_code==204):
        print("Jira Ticket :{0} updated".format(ticket_id))
    else:
        print("Error in Jira Ticket Update")
        print(issue.json())

#==============================================================================================================================================
#Function to send mail
#==============================================================================================================================================
def send_mail(user_mailId,user_name,storage_account_name):
    sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
    from_email = Email("ecad-support@ecad.app")
    to_email = To(user_mailId)
    cc_email = Email("Ecad.devops@se.com")
    p = Personalization()
    p.add_to(to_email)
    p.add_cc(cc_email)
    mail = Mail(from_email,to_email)
    mail.add_personalization(p)
    mail.dynamic_template_data = {   
        "user_name":user_name,  
        "sa_name":storage_account_name
    }
    template_id=sendgrid_template_id
    mail.template_id = template_id
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    if(response.status_code==202):
        print("Mail sent")
        return 1
    else:
        print("Error-Email not sent")
        print(response.status_code)
        print(response.body)
        return 0
#==============================================================================================================================================
#Start
#==============================================================================================================================================
jiraapiToken=os.environ.get("JIRA_BASIC_AUTH")
sendgrid_api_key=os.environ.get("SENDGRID_API_KEY")
sendgrid_template_id=os.environ.get("SENDGRID_TEMPLATE_ID")
ticket_id=sys.argv[1]

#==============================================================================================================================================
#get user details(mail id and name)
#==============================================================================================================================================
client_id=os.environ.get("ARM_CLIENT_ID")
client_secret=os.environ.get("ARM_CLIENT_SECRET")
tenant_id=os.environ.get("ARM_TENANT_ID")
userPrincipalName=sys.argv[2]
headers_token={"Content-Type": "application/x-www-form-urlencoded"}
secrets = {
    "client_id": client_id,
    "grant_type": "client_credentials",
    "scope": "https://graph.microsoft.com/.default",
    "client_secret": client_secret
}
res1=requests.post("https://login.microsoftonline.com/{0}/oauth2/v2.0/token".format(tenant_id),headers=headers_token,data=secrets)
res1_json=res1.json()
headers_userDetails= {
    "Authorization":"Bearer {0}".format(res1_json["access_token"]),
    "Content-Type": "application/json"
}
res_user=requests.get("https://graph.microsoft.com/v1.0/users/{0}".format(userPrincipalName), headers=headers_userDetails)
res_user_json=res_user.json()
user_mailId=res_user_json["mail"]
user_name=res_user_json["displayName"]

#==============================================================================================================================================
#Using tfvars file,get the required details to be sent in email
#==============================================================================================================================================
with open('input/user-input.tfvars', 'r') as file:
        data = hcl2.load(file)
        #required fields
        storage_account_name=data["storage_account_name"]
        file.close()

#==============================================================================================================================================
#Sendmail and Close jira ticket
#==============================================================================================================================================
if(send_mail(user_mailId,user_name,storage_account_name)):
    update_jiraticket_status("Storage Account created successfully!Details sent to {0}.".format(user_name))
