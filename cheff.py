import boto3
import util
import chef as pychef


class chef:
    def __init__(self, profile):
        self.knife = util.get_knife_creds()
        self.chef_api = pychef.ChefAPI(
            self.knife['chef_server_url'],
            self.knife['client_key'],
            self.knife['node_name']
        )
        self.profile = util.get_aws_creds(profile)
        self.client = boto3.client(
            'ec2',
            aws_access_key_id=self.profile['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.profile['AWS_SECRET_ACCESS_KEY']
        )

    def get_instance_ids(self):
        instances = self.client.describe_instances()
        instanceIds = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instanceIds.append(instance['InstanceId'])
        return instanceIds

    def get_chef_nodes(self):
        instanceIds = []
        for node in sorted(
            pychef.Search('node', 'roles:*', api=self.chef_api),
            key=lambda node: node['name']
        ):
            instanceIds.append(node['name'])
        return instanceIds

    def delete_chef_node(self, nodeId):
        try:
            node = pychef.Node(nodeId, api=self.chef_api)
            node.delete(api=self.chef_api)
            client = pychef.Client(nodeId, api=self.chef_api)
            client.delete(api=self.chef_api)
            return True
        except Exception as e:
            return e
