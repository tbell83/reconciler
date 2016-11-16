from cheff import chef, aws
import argparse
import datetime
import re
import logging
logging.captureWarnings(True)


def get_chefs():
    chef_client = chef()
    return chef_client.get_chef_nodes()


def get_ecss(profiles=['drama9', 'prod']):
    ecs_instance_ids = []
    for profile in profiles:
        aws_client = aws(profile)
        ecs_instance_ids += aws_client.get_instance_ids()
    return sorted(ecs_instance_ids)


def get_dead_chefs(chefs=get_chefs(), ecss=get_ecss()):
    dead_chefs = []
    for instance in chefs:
        if instance.split('.')[-1] not in ecss:
            dead_chefs.append(instance)
    return dead_chefs


def status(show_all=False):
    chef_client = chef()
    failures = chef_client.get_convergence_status(show_all=show_all)
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


def get_dupes(chefs=get_chefs()):
    nodes = chefs
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


def prune(execute=False):
    chef_client = chef()
    dead_chefs = get_dead_chefs(chefs=get_chefs(), ecss=get_ecss())
    for node in dead_chefs:
        print 'Removing node and client object for {}'.format(node)
        if execute:
            chef_client.delete_chef_node(node)


def report(print_out=True):
    dead_chefs = get_dead_chefs()
    dupes = get_dupes()
    output = {}
    output['Chef Instances'] = get_chefs()
    output['EC2 Instances'] = get_ecss()
    output['Orphaned Chef Nodes'] = dead_chefs
    output['Duplicate Nodes'] = dupes
    if print_out:
        for item in output:
            print '{}\t{}'.format(len(output[item]), item)
    return output


def dedupe(execute=False):
    chef_client = chef()
    dupes = get_dupes(get_chefs())
    for dupeset in dupes:
        nodes = chef_client.get_convergence_status(target_nodes=dupeset)
        for node in nodes:
            if (datetime.datetime.now() - nodes[node]).total_seconds() > 900:
                print 'removing {} which last converged: {}'.format(
                    node,
                    nodes[node]
                )
                if execute:
                    chef_client.delete_chef_node(node)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', dest='execute', action='store_true', default=False
    )
    parser.add_argument(
        '-a', dest='all', action='store_true', default=False
    )
    parser.add_argument('command', nargs='?', default=None)
    args = parser.parse_args()
    if args.execute is False \
        and args.command != 'status' \
            and args.command:
        print '!!!PRE-FLIGHT, NOT REMOVING ANYTHING!!!\n' \
            'Use -e to execute changeset'
    if args.command == 'status':
        for node in status(args.all):
            print node
    elif args.command == 'prune':
        prune(execute=args.execute)
        if report(print_out=False)['Duplicate Nodes'] > 0:
            dedupe(execute=args.execute)
    elif args.command == 'dedupe':
        dedupe(execute=args.execute)
    else:
        report()

if __name__ == '__main__':
    main()
