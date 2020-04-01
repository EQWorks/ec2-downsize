import boto3


def main():
    ec2 = boto3.client('ec2')
    ins = boto3.resource('ec2').instances.filter(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running'],
        },
    ])
    # stop instances
    ec2.stop_instances(InstanceIds=ins)
    waiter=ec2.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=ins)
    # modify/downsize instance type
    for i in ins:
        try:
            ec2.modify_instance_attribute(
                InstanceId=i,
                Attribute='instanceType',
                Value='t3.nano',
            )
        except Exception as e:
            try:
                ec2.modify_instance_attribute(
                    InstanceId=i,
                    Attribute='instanceType',
                    Value='t2.nano',
                )
            except Exception as e:
                print(e)
                print(i)
    # restart instancs async
    ec2.start_instances(InstanceIds=ins)


if __name__ == "__main__":
    main()
