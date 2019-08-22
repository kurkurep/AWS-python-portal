# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:02:49 2019

@author: kurkurep
"""



from flask import Flask, request, render_template
import boto3
import sys
import os
import time
import botocore
import cgi
global ec2_con_re

iam = boto3.client('iam')

form = cgi.FieldStorage()

app = Flask(__name__)
ec2client = boto3.client('ec2')
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template("Trial.html", msg="AWS with Python and Html")


@app.route('/get_ec2_con_for_give_region', methods=["GET", "POST"])
def get_ec2_con_for_give_region():
    region = request.form.get("Region")
    global ec2_con_re
    ec2_con_re=boto3.resource('ec2',region)
    print(ec2_con_re)
    print(type(ec2_con_re))
    x=[("User: {0}\nUserId: {1}\nARN: {2}\nCreatedOn: {3}\n".format(user['UserName'],user['UserId'],user['Arn'],user['CreateDate']))for user in iam.list_users()['Users']]
    return render_template("Trial2.html",msg=x)

@app.route('/list_roles', methods=["GET", "POST"])
def list_roles():
    y=[("Role: {0}\nRoleId: {1}\nARN: {2}\nCreatedOn: {3}\n".format(user['RoleName'],user['RoleId'],user['Arn'],user['CreateDate']))for user in iam.list_roles()['Roles']]
    return render_template("Trial3.html",msg=y)

@app.route('/list_instances', methods=["GET", "POST"])
def list_instances():
    z=[("Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\nTags: {6}\n".format(instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state, instance.tags)) for instance in ec2_con_re.instances.all()]
    return render_template("Trial4.html",msg=z)


def get_instant_state(ec2_con_re,in_id): 
    state=[]
    for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
            state = each.state['Name']
    return state

@app.route('/start_instance', methods=["GET", "POST"])
def start_instance():
    pr_st=get_instant_state(ec2_con_re,request.form.get("instance_id"))
    if request.form['start/stop']=="start": 
                        
        if pr_st=="running":
            return render_template("Trial5.html",msg1=("Already running instance"))
        else:
            for instance in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[request.form['instance_id']]}]):
                instance.start()     
                #return render_template("trial3.html",msg1=("Starting instance"))
                instance.wait_until_running()
                return render_template("Trial5.html",msg1=("Instance started"))
    else:
        x = stop_instance(pr_st,ec2_con_re,request.form['instance_id'])
        return render_template("Trial5.html",msg1=(x))
                    
def stop_instance(pr_st,ec2_con_re,in_id):
    pr_st=get_instant_state(ec2_con_re,in_id)
    print (pr_st)
    if pr_st=="stopped":
           return "Already stopped instance"
    else:
           for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
                   each.stop()
                   each.wait_until_stopped()
                   return "Instance stopped"

if __name__ == '__main__':
  os.system('cls')
  in_id=""
  region=""
  app.run()
