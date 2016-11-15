import boto3
import util.util as util
import chef as pychef
import datetime


class aws:
    def __init__(self, profile):
        self.profile = util.get_aws_creds(profile)
        self.client = boto3.client(
            'ec2',
            aws_access_key_id=self.profile['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.profile['AWS_SECRET_ACCESS_KEY'],
            region=self.profile['REGION']
        )

    def get_instance_ids(self):
        instances = self.client.describe_instances()
        instanceIds = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'running':
                    instanceIds.append(instance['InstanceId'])
        return instanceIds


class chef:
    def __init__(self):
        self.knife = util.get_knife_creds()
        self.chef_api = pychef.ChefAPI(
            self.knife['chef_server_url'],
            self.knife['client_key'],
            self.knife['node_name']
        )

    def get_chef_nodes(self):
        nodes = []
        for node in pychef.node.Node.list(api=self.chef_api):
            nodes.append(node)
        return nodes

    def delete_chef_node(self, nodeId):
        try:
            pychef.Node(nodeId, api=self.chef_api).delete(api=self.chef_api)
            pychef.Client(nodeId, api=self.chef_api).delete(api=self.chef_api)
            return True
        except Exception as e:
            return e

    def get_convergence_status(self, target_nodes=None, show_all=True):
        nodes = {}
        now = datetime.datetime.now()
        if target_nodes is None:
            target_nodes = self.get_chef_nodes()
        for node in target_nodes:
            try:
                last_converge = datetime.datetime.fromtimestamp(pychef.Node(
                    node, api=self.chef_api
                ).attributes['ohai_time'])
            except:
                continue
            if not show_all:
                if (now - last_converge).seconds > 720:
                    nodes[node] = last_converge
            else:
                    nodes[node] = last_converge
        return nodes
