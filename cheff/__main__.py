import sys
import cheff as chef
import argparse


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', dest='execute', action='store_true', default=False
    )
    args = parser.parse_args()

    profiles = [
        'prod',
        'drama9'
    ]

    ecs_instance_ids = []
    for profile in profiles:
        Chef = chef.chef(profile)
        ecs_instance_ids += Chef.get_instance_ids()

    Chef = chef.chef('prod')
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
        print 'Removing node and client object for {}'.format(node)
        if args.execute:
            # Chef.delete_chef_node(node)
            print 'forreal'


if __name__ == '__main__':
    main()
