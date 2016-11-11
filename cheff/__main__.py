from cheff import chef, aws
import argparse
import datetime
import re


def status(chef_client):
    failures = chef_client.get_convergence_status()
    status = []
    for failure in sorted(failures, key=lambda failure: failures[failure]):
        seconds_since_fail = int((
            datetime.datetime.now() - failures[failure]
        ).total_seconds())
        if seconds_since_fail < 60:
            msg = '{} seconds ago'.format(seconds_since_fail)
        elif seconds_since_fail < 3600:
            msg = '{} minutes ago'.format(seconds_since_fail/60)
        elif seconds_since_fail < 86400:
            msg = '{} hours ago'.format(seconds_since_fail/3600)
        else:
            msg = '{} days ago'.format(seconds_since_fail/86400)
        status.append('{}:\t{}'.format(msg, failure))
    return status


def dedupe(chef_client):
    nodes = chef_client.get_chef_nodes()
    dupes = []
    for node in nodes:
        id = node.split('.')[-1]
        matches = []
        for i in nodes:
            if re.search(id, i):
                matches.append(i)
        if len(matches) > 1:
            dupes.append(sorted(matches))
    deduped = []
    for dupeset in sorted(dupes):
        if dupeset not in deduped:
            deduped.append(dupeset)
    return deduped


def prune(chef_client, execute=False, profiles=['drama9', 'prod']):
    ecs_instance_ids = []
    for profile in profiles:
        aws_client = aws(profile)
        ecs_instance_ids += aws_client.get_instance_ids()

    chef_node_instance_ids = chef_client.get_chef_nodes()
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
        if execute:
            chef_client.delete_chef_node(node)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', dest='execute', action='store_true', default=False
    )
    parser.add_argument('command')
    args = parser.parse_args()
    chef_client = chef()
    if args.execute is False and args.command != 'status':
        print '!!!PRE-FLIGHT, NOT REMOVING ANYTHING!!!\n' \
            'Use -e to execute changeset'
    if args.command == 'status':
        for node in status(chef_client):
            print node
    elif args.command == 'prune':
        prune(chef_client, execute=args.execute)
    elif args.command == 'dedupe':
        dupes = dedupe(chef_client)
        for dupeset in dupes:
            nodes = chef_client.get_convergence_status(nodes=dupeset)
            for node in nodes:
                print 'removing {} which last converged:\t\t{}'.format(
                    node,
                    nodes[node]
                )
                if args.execute:
                    chef_client.delete_chef_node(node)


if __name__ == '__main__':
    main()
