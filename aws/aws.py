import boto3
import yaml
import sys
from botocore.exceptions import ClientError
import re

class AWSEC2:

    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')
        self.elb= boto3.client('elb')
        f=open('data.yml')
        self.yml=yaml.load(f)

    def checkExistance(self, securitygroup):
        print "-------------Checking to see if Security Group exists------------------"
        groupInfo = []
        for securityGroup in securitygroup:
            securityGroupName= securitygroup.get(securityGroup).get('name')
            #print self.VpcId
            try:
                a = self.ec2.describe_security_groups(
                    GroupNames=[
                        securityGroupName
                    ]
                )
                print a
                if (a is not None):
                    print "---------------- Group with name %s exists, ----------------" % (securityGroup)
                    continue
            except ClientError as e:
                print "This Group Does not exist %s"%(securityGroupName)
                GroupId = self.createSecurityGroup(securityGroupName)
                print GroupId
                groupData=[securityGroupName,GroupId]
                groupInfo.append(groupData)
                pass
        return groupInfo

    def createSecurityGroup(self,securityGroupName):
        print "-------This method is used to create Security Group---------------------"
        response = self.ec2.create_security_group(GroupName=securityGroupName,
                                  Description="This is a security group for %s"%(securityGroupName))
                                  #VpcId=self.VpcId)
        security_group_id = response['GroupId']
        return security_group_id

    def getSecurityGroupId(self,groupName):
        r = self.ec2.describe_security_groups(
            GroupNames=[
                groupName
            ]
        )
        t = r.get('SecurityGroups')[0]
        return t.get('GroupId')


    def attachRules(self, groupInfo):
        for group in groupInfo:
            securityGroupName=group[0]
            securityGroupId=group[1]
            securitygroup = self.yml.get('SecurityGroups')
            for sgroups in securitygroup:
                if (securitygroup.get(sgroups).get('name') == securityGroupName):
                    mappings=securitygroup.get(sgroups).get('mappings')
                    print "this method is used to attach the rules for seurity group"
                    for mapping in mappings:
                        if (mapping == "inBound_mapping"):
                            for mapdata in mappings[mapping]:
                                print mapdata
                                p = re.compile("([\d]+\.){3}\d*\/\d+")
                                print p.match(str(mappings[mapping][mapdata].get('IpRanges')))
                                if ((p.match(str(mappings[mapping][mapdata].get('IpRanges')))) is None):
                                    range='UserIdGroupPairs'
                                    ipType ='GroupId'
                                    ipRange = self.getSecurityGroupId(mappings[mapping][mapdata].get('IpRanges'))
                                else:
                                    range = 'IpRanges'
                                    ipType = 'CidrIp'
                                    ipRange = mappings[mapping][mapdata].get('IpRanges')
                                try:
                                    print ipRange
                                    data = (self.ec2).authorize_security_group_ingress(
                                        GroupId=securityGroupId,
                                        IpPermissions=[
                                            {'IpProtocol': mappings[mapping][mapdata].get('IpProtocol'),
                                             'FromPort': mappings[mapping][mapdata].get('FromPort'),
                                             'ToPort': mappings[mapping][mapdata].get('ToPort'),
                                             range: [{ipType: ipRange}]}

                                            ])
                                    print data
                                except ClientError as e:
                                    print (e)
                                    pass
                        elif (mapping == 'outBound_mapping'):
                            print "this is a set up for outbound mapping"
                            for mapdata in mappings[mapping]:
                                t=str(mappings[mapping][mapdata].get('IpRanges'))
                                p = re.compile("([\d]+\.){3}\d*\/\d+")
                                print mappings[mapping][mapdata].get('IprRanges')
                                print (p.match(str(mappings[mapping][mapdata].get('IpRanges'))))
                                a=mappings[mapping][mapdata]
                                print a
                                if ((p.match(str(mappings[mapping][mapdata].get('IpRanges')))) is None):
                                    range = 'UserIdGroupPairs'
                                    ipType = 'GroupId'
                                    ipRange = self.getSecurityGroupId(mappings[mapping][mapdata].get('IpRanges'))
                                else:
                                    range = 'IpRanges'
                                    ipType = 'CidrIp'
                                    ipRange = mappings[mapping][mapdata].get('IpRanges')
                                try:
                                    data = (self.ec2).authorize_security_group_egress(
                                        GroupId=securityGroupId,
                                        IpPermissions=[
                                            {'IpProtocol': mappings[mapping][mapdata].get('IpProtocol'),
                                             'FromPort': mappings[mapping][mapdata].get('FromPort'),
                                             'ToPort': mappings[mapping][mapdata].get('ToPort'),
                                             range: [{ipType: ipRange}]}

                                        ])
                                    print data
                                except ClientError as e:
                                    print (e)
                                    pass


    def createInstance(self):
        print "======= This method is used to create instances======================="
        print self.ec2
        Instances = self.yml.get('EC2-Instance')
        InstanceId=[]
        for instance in self.yml.get('EC2-Instance'):
            if (Instances.get(instance).get('re-create')):
                try:
                    data = self.ec2_resource.create_instances(
                    BlockDeviceMappings=[
                            {
                                'DeviceName': Instances.get(instance).get('DeviceName'),
                                'VirtualName': Instances.get(instance).get('VirtualName'),
                                'Ebs': {
                                    'SnapshotId': Instances.get(instance).get('SnapshotId'),
                                    'DeleteOnTermination': Instances.get(instance).get('DeleteOnTermination'),
                                    'VolumeSize': Instances.get(instance).get('VolumeSize'),
                                    'VolumeType': Instances.get(instance).get('VolumeType')
                                },

                            },
                        ],
                        Placement={
                            'AvailabilityZone': Instances.get(instance).get('AvailabilityZone')
                        },

                        ImageId=Instances.get(instance).get('ami-id'),
                        MinCount=Instances.get(instance).get('min-count'),
                        MaxCount=Instances.get(instance).get('max-count'),
                        InstanceType=Instances.get(instance).get('instanceType'),
                        SecurityGroups=Instances.get(instance).get('SecurityGroups'),
                        KeyName= Instances.get(instance).get('KeyName')
                    )
                    pt=data[0]
                    print pt.id
                    #pt.split("=")[1][1:-3]
                   # print pt
                    instance=[Instances.get(instance).get('Instance-Name'),pt.id]
                    InstanceId.append(instance)
                except ClientError as e:
                    print (e)
            else:
                print "--------- VM recreation is not needed at this point, checking the permission for other vm -----------"
        return InstanceId



    def parseSecrity(self):
        securityGroupInstance = self.yml.get('SecurityGroups')
        groupInfo=self.checkExistance(securityGroupInstance)
        self.attachRules(groupInfo)
        instanceId=self.createInstance()
        print instanceId


if __name__ == '__main__':
    aws = AWSEC2()
    aws.parseSecrity()
