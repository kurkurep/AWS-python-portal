import boto3
import sys
import os
import time
import botocore
iam = boto3.client('iam')


#def get_ec2_cred(my_access_key,my_secret_key):
 # ec2_cred=boto3.resources('ec2',access_key=my_access_key,secret_key=my_secret_key)
  #  return ec2_cred
#
def get_ec2_con_for_give_region(my_region):
                ec2_con_re=boto3.resource('ec2',region_name=my_region)
                return ec2_con_re
            
def get_ec2_users(ec2_con_re):
    for user in iam.list_users()['Users']:
        print("User: {0}\nUserId {1}\nARN: {2}\nCreatedOn: {3}\n".format(user['UserName'],user['UserId'],user['Arn'],user['CreateDate']))
                
def get_ec2_roles(ec2_con_re):
    for user in iam.list_roles()['Roles']:
        print("Role: {0}\nRoleId {1}\nARN: {2}\nCreatedOn: {3}\n".format(user['RoleName'],user['RoleId'],user['Arn'],user['CreateDate']))  
    
def list_instances_on_my_region(ec2_con_re):
    for each in ec2_con_re.instances.all():
        print(each.id)
        
def get_instant_state(ec2_con_re,in_id):
        for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
                pr_st=each.state['Name']
        return pr_st    
    
def start_instance(ec2_con_re,in_id):
         pr_st=get_instant_state(ec2_con_re,in_id)
         if pr_st=="running":
                print("Already running instance")
         else:
                for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
                        each.start()
                        print("Starting instance")
                        each.wait_until_running()
                        print("Instance started")
         return 
           
def stop_instance(ec2_con_re,in_id):
         pr_st=get_instant_state(ec2_con_re,in_id)
         if pr_st=="stopped":
                print("Already stopped instance")
         else:
                for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
                        each.stop()
                        print("Stopping instance")
                        each.wait_until_stopped()
                        print("Instance stopped")
                        
def main():
        my_region=input("Enter your region:")
        ec2_con_re=get_ec2_con_for_give_region(my_region)
        print("Getting all users {}".format(my_region))
        get_ec2_users(ec2_con_re)
        print("Getting all roles to assume {}".format(my_region))
        get_ec2_roles(ec2_con_re)
        print("Getting all instance id {}".format(my_region))
        list_instances_on_my_region(ec2_con_re)
        user_id=input("Choose the user id:")
        role_id=input("Choose the role id:")
        in_id=input("Choose the instance id:")
        start_sotp=input("Enter start or stop:")
        while True:
                if start_sotp not in ["start","stop"]:
                         start_sotp=input("Enter only start or stop command:")
                         continue
                         
                else:
                         break
        if start_sotp=="start":
                start_instance(ec2_con_re,in_id)
        else:
                stop_instance(ec2_con_re,in_id)
        
        
        
if __name__ == '__main__':
      os.system('cls')
      main()
