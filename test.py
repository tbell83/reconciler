import cheff.cheff as cheff

profiles = [
    'prod',
    'drama9'
]

ecs_instance_ids = []
for profile in profiles:
    Chef = cheff.chef(profile)
    ecs_instance_ids += Chef.get_instance_ids()

Chef = cheff.chef('prod')
chef_node_instance_ids = sorted(Chef.get_chef_nodes())
ecs_instance_ids = sorted(ecs_instance_ids)

print 'Chef Instances: {}\nEC2 Instances: {}'.format(
    len(chef_node_instance_ids), len(ecs_instance_ids)
)

dead_chefs = []
for instance in chef_node_instance_ids:
    if instance.split('.')[-1] not in ecs_instance_ids:
        dead_chefs.append(instance)

print 'Orphaned Chef Nodes: {}'.format(len(dead_chefs))

for node in dead_chefs:
    Chef.delete_chef_node(node)
