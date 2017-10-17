# nodePipeline

This is the deployment pipeline to deploy nodejs application to AWS instance.

 1. EC2 instance creation is automated using python and its supported library Boto3.
    Security policy has been applied as part of this automation to enable incoming request on various ports. All configuration information 
    about instance can be found in data.yml file under aws folder.
    Note: certain steps needs to be perofrmed to set up run time environment for boto3 to run. After performing basic environment set up
           we are ready to run this automation to spin up new vm's in AWS.
  
 2. After spinning up the VM we are all set for deployments.
    Deployments are done using Ansible, this is a 2 step process.
    
    1. Configure dynamic inventory for ansible to run on AWS instances.
    2. Run the main.yml as it will install all required packages and do the deployment based on the environment passed to it.
    
    Example: ansible-playbook main.yml --extra-vars "ENVR=DEV"
            
            'Here ENVR is the environment and we need to change this based on where we want to deploy.'
          
  Deployment details:
  
  1. One AWS instance was created and all deployments were done on same VM.
  2. Deployments were done for 4 environments with different environment varibales.
      1. DEV : ENV= DEV, PORT=8002
      2. TEST: ENV=TEST, PORT=8001
      3. DR: ENV=DR, PORT=8003
      4. PROD ENV=PROD, PORT=8004
      
  3. Localtion of each deployment
      1. DEV: /opt/ENV/DEV
      2. TEST: /opt/ENV/TEST
      3. DR: /opt/ENV/DR
      4. PROD: /opt/ENV/PROD
      
      
  Login to VM can be done using the access key that is also saved along with code ( prajjwalkey.pem )
  
  chmod 400 prajjwalkey.pem
  ssh -i "prajjwalkey.pem" ubuntu@ec2-35-166-148-130.us-west-2.compute.amazonaws.com
  
 Application Can be accessed on these ports:
  
 DEV: http://ec2-35-166-148-130.us-west-2.compute.amazonaws.com:8002/
 TEST: http://ec2-35-166-148-130.us-west-2.compute.amazonaws.com:8001/
 DR: http://ec2-35-166-148-130.us-west-2.compute.amazonaws.com:8003/
 PROD:  http://ec2-35-166-148-130.us-west-2.compute.amazonaws.com:8004/
  
  
  
