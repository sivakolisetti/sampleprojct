#============================================================================================================
#      FILE NAME: create-tfvars.py
#      USAGE: python create-tfvars.py ticket_id 
#      ENVIRONMENT VARIABLES: GH_PAT,JIRA_BASIC_AUTH,CLIENT_ID,CLIENT_SECRET,TENANT_GUID
#      VERSION: 1.0
#      AUTHOR: Sahana Gajanana Acharya
#      DEPARTMENT: Platform Team
#============================================================================================================

import requests
import sys,os
import git
import json
import shutil

#============================================================================================================
#Functions:
#Function to execute git push
#============================================================================================================
def git_push():
      repo.git.add('--all')
      repo.git.commit("-m","Create tfvars file")
      repo.git.push('origin',branch)

#============================================================================================================
#Function to create pull request
#============================================================================================================
def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }

    r = requests.post(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))
    resp=r.json()
    print("Pull Request No"+str(resp["number"]))
    pr_no=resp["number"]
    print(pr_no)
    merge_pull_request("aeco-bim-dces","aeco-bim-dces-iac-ecad-storageaccount",branch, "Create PR",branch,"main",pat,pr_no)

#============================================================================================================================================
#Function to merge pull request
#============================================================================================================================================
def merge_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token,pr_no):
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls/{2}/merge".format(
        project_name,
        repo_name, pr_no)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}
    payload = {
        "commit_message": "Merge PR",
    }
    r = requests.put(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))
    if not r.ok:
        print("Request Failed: {0}".format(r.text))

#============================================================================================================================================
#Start:
#============================================================================================================================================
ticket_id=sys.argv[1]
pat=os.environ.get("GH_PAT")
jira_sd=os.environ.get("JIRA_BASIC_AUTH")

#============================================================================================================================================
#Creating unique identifier(from Jira ticket Id) for all the resources getting created.
#============================================================================================================================================
identifier=ticket_id[4:]
if(len(identifier)==1):
    identifier="000{0}".format(identifier)
elif(len(identifier)==2):
    identifier="00{0}".format(identifier)
elif(len(identifier)==3):
    identifier="0{0}".format(identifier)
print(identifier)

#=======================================================================================================================================================
#Get user inputs from Jira:
#=======================================================================================================================================================
issue = requests.get('https://schneider-electric-se.atlassian.net/rest/servicedeskapi/request/'+ticket_id,headers={"accept": 'application/json',
         "Authorization": "Basic "+jira_sd}).json()
print(issue['requestFieldValues'])

#=======================================================================================================================================================
#Extract the required field values into variables:
#=======================================================================================================================================================
for i in issue['requestFieldValues']:
    if i['label']=="Subscription Name":
       subscriptionName=i['value']['value']
    if i['label']=="ECAD Cost Center":
       cost_center=i['value']['value']
    if i['label']=="Application Family":
       app=i['value']['value']
    if i['label']=="Enter Alpicloud Email ID":
       userPrincipalName=i['value']

#=======================================================================================================================================================
#get subscription identifier to use in storage account name and environment to use in tags
#=======================================================================================================================================================
sub_name_split=subscriptionName.split("-")
subscriptionIdentifier=sub_name_split[len(sub_name_split)-1]
env=sub_name_split[len(sub_name_split)-2]
print("subscriptionIdentifier: "+subscriptionIdentifier)
print("env: "+env)

#=======================================================================================================================================================
#To get Subscription Id from Subscription Name
#=======================================================================================================================================================
client_id=os.environ.get("CLIENT_ID")
client_secret=os.environ.get("CLIENT_SECRET")
tenant_id=os.environ.get("TENANT_GUID")
secrets = {
    "client_id": client_id,
    "grant_type": "client_credentials",
    "scope": "https://management.core.windows.net/.default",
    "client_secret": client_secret
}
res=requests.post("https://login.microsoftonline.com/{0}/oauth2/v2.0/token".format(tenant_id),headers={"Content-Type": "application/x-www-form-urlencoded"},data=secrets).json()
headers_subDetails= {
    "Authorization":"Bearer {0}".format(res["access_token"]),
    "Content-Type": "application/json"
}
#==========================================================================================================================================================================================
#list all subscriptions and get sub Id
#==========================================================================================================================================================================================
res=requests.get("https://management.azure.com/subscriptions?api-version=2020-01-01",headers=headers_subDetails).json()
flag=0
for x in res['value']:
    if(subscriptionName==x['displayName']):
        subscriptionId=x['subscriptionId']
        flag=1
        break
#==========================================================================================================================================================================================
#If subscription doesnt exist,stop execution, else continue 
#==========================================================================================================================================================================================
if(flag!=1):
    print("Subscription does not exists!")
else:
    #======================================================================================================================================================================================
    #Update user-input.txt file with the required variables(exported as GH variables) to be used in different tasks in next Github ACtion
    #======================================================================================================================================================================================
    with open("user-input.txt", "w") as f:
        f.write('subscriptionId={0}\n'.format(subscriptionId))
        f.write('ticket_id={0}\n'.format(ticket_id))
        f.write('subscriptionName={0}\n'.format(subscriptionName))
        f.write('app={0}\n'.format(app.lower()))
        f.write('userPrincipalName={0}\n'.format(userPrincipalName))
        f.close()
    #=======================================================================================================================================================================================
    #Update the required variables in user-input.tfvars(this variable file will be used by terraform)
    #=======================================================================================================================================================================================
    with open("user-input.tfvars",'a+') as fn:
        fn.write('storage_account_name="st{0}{1}we{2}"\n'.format(subscriptionIdentifier,env,identifier))  #Name must be between 3 and 24 characters.
        fn.write('resource_name="st{0}{1}we{2}"\n'.format(subscriptionIdentifier,env,identifier))
        fn.write('resource_type="Microsoft.Storage/storageAccounts"\n')    
        fn.write('resource_group_name="rg-{0}-we"\n'.format(subscriptionName))
        fn.write('spoke_vnet="vnet-{0}-we"\n'.format(subscriptionName))
        fn.write('vm_subnet="vmsubnet-{0}-we"\n'.format(subscriptionName))
        fn.write('blob_private_endpoint="sa{0}-wePrivateEndpoint{1}"\n'.format(subscriptionName,identifier))
        fn.write('tags = {createdWith ="terraform",finid="'+cost_center+'",app="'+app+'",env="'+env+'"}\n')
        fn.close()
    #========================================================================================================================================================================================
    #Github:If repo exists-delete it,Clone repo,Create Branch,Copy Files,Git Push,Create PR and Merge PR.
    #========================================================================================================================================================================================
    if os.path.exists('aeco-bim-dces-iac-ecad-storageaccount'):
       shutil.rmtree('aeco-bim-dces-iac-ecad-storageaccount')
    repo=git.Repo.clone_from('https://srvgh-aecobimdces_ecad:'+pat+'@github.com/aeco-bim-dces/aeco-bim-dces-iac-ecad-storageaccount', 'aeco-bim-dces-iac-ecad-storageaccount')
    branch=ticket_id
    repo.git.checkout('-b',branch)
    shutil.copy("user-input.tfvars","aeco-bim-dces-iac-ecad-storageaccount/input/user-input.tfvars")
    shutil.copy("user-input.txt","aeco-bim-dces-iac-ecad-storageaccount/input/user-input.txt")
    git_push()
    create_pull_request("aeco-bim-dces","aeco-bim-dces-iac-ecad-storageaccount",branch, "Create PR",branch,"main",pat)
