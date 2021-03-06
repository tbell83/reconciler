# Reconciler
Reconciles ECS and Chef nodes, pruning when necessary

## Setup
reconciler expects aws creds to be in `~/.aws/config` and knife creds to be in
`~/.chef/knife.rb`

To install clone this repo and run `make` .

For ease of use you can add an alias to `~/.virtualenv/reconciler/bin/reconciler`

## Usage
`reconciler`

Returns current reconcilliation between chef and ec2

```
174	Chef Instances
5	Orphaned Chef Nodes
1	Duplicate Nodes
187	EC2 Instances
```

### Status
`reconciler status`

Returns convergence status of chef registered nodes, default only shows nodes
that have not converged in the past 10 minutes, `-a` to show status of all nodes.

```
2 hours ago:	i-0c528c6417edea7c0
2 hours ago:	i-0d9b52305a18eb70c
53 minutes ago:	i-0b54bcbdb2543e587
51 minutes ago:	i-0daf831cb47516a8b
17 minutes ago:	i-0639404ab46f0f5d5
3 minutes ago:	i-0243c84e41946704f
```

### Prune

`reconciler prune`

Runs a prune of chef nodes that are no longer present in ec2.
It will also do a check for nodes registered with chef that have duplicate ec2 instance IDs.

By default this runs without actually making any changes to the chef server,
to execute the changeset use the `-e` flag.

```
Removing node and client object for i-0a84c58ba016bc130
Removing node and client object for i-0abc434b062bdd006
Removing node and client object for i-0beb519eddc7c87d7
Removing node and client object for i-0d9b52305a18eb70c
Removing node and client object for i-092a2154a58f0c36b
```

### Dedupe

`reconciler dedupe`

Removes chef nodes that are failing to converge and have duplicate EC2 instance
IDs.

By default this runs without actually making any changes to the chef server,
to execute the changeset use the `-e` flag.

```
removing i-06c6ed728b769a626 which last converged: 2016-11-15 12:02:22.230306
removing i-0c528c6417edea7c0 which last converged: 2016-11-15 09:10:06.686192
```
