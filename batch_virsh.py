#!/usr/bin/env python
import sys
import time
import commands


def start_domains(start, end):
    for i in range(start, end+1):
        cmd = 'virsh start node%s' % i
        commands.getoutput(cmd)
        time.sleep(1)


def destroy(start, end):
    for i in range(start, end+1):
        cmd1 = 'virsh destroy node' + str(i)
        commands.getoutput(cmd1)


def snap(start, end, snap_name):
    for i in range(start, end+1):
        cmd2 = 'virsh snapshot-create-as --name %s node%s' % (snap_name, str(i))
        commands.getoutput(cmd2)


def undef(start, end):
    for i in range(start, end+1):
        cmd3 = 'virsh undefine node' + str(i)
        commands.getoutput(cmd3)


def revert(start, end, snap_name):
    for i in range(start, end+1):
        cmd4 = 'virsh snapshot-revert --snapshotname %s node%s' % (snap_name, str(i))
        commands.getoutput(cmd4)


def _help():
    help_str = """
Usage: batch_virsh <subcommands> [parameters]

Batch undefine or/and destroy or/and snapshot domains use libvirt command lines.

Subcommands:
    help        show this help message and exit
    start       start domains limited by parameters
                    like: batch_virsh start start end
    snap        power off and snapshot domains limited by parameters
                    like: batch_virsh snap start end snapshot_name
    revert      revert domains to snapshot limited by parameters
                    like: batch_virsh revert start end snapshot_name
    destroy     power off domains limited by parameters
                    like: batch_virsh destroy start end
    undefine    undefine domains limited by parameters
                    like: batch_virsh undefine start end

Parameters:
    start       integer number suffix of the first domains' name
                    if node23, the start is 23
    end         integer number suffix of the last domains' name
                    if node23, the end is 23
    name        name of snapshot
"""
    print help_str


def _handle_error_params():
    _help()
    print 'ERROR! No argument passed to command module'
    sys.exit(1)


def main():
    try:
        param1 = sys.argv[1]
    except IndexError, ie:
        _handle_error_params()
    try:
        start = int(sys.argv[2])
        end = int(sys.argv[3])
    except IndexError, ie:
        if param1 != 'help':
            _handle_error_params()
    except ValueError, ve:
        _handle_error_params()
    if param1 == 'start':
        if len(sys.argv) < 4:
            _handle_error_params()
        jixu = raw_input('will start all nodes you select, continue? [yes/no]: ')
        if jixu == 'yes':
            start_domains(start, end)
    elif param1 == 'snap':
        if len(sys.argv) < 5:
            _handle_error_params()
        snap_name = sys.argv[4]
        jixu = raw_input('will destroy all nodes you select, continue? [yes/no]: ')
        if jixu == 'yes':
            destroy(start, end)
            time.sleep(1)
            snap(start, end, snap_name)
    elif param1 == 'revert':
        if len(sys.argv) < 5:
            _handle_error_params()
        snap_name = sys.argv[4]
        jixu = raw_input('will revert all nodes you select, continue? [yes/no]: ')
        if jixu == 'yes':
            revert(start, end, snap_name)
    elif param1 == 'destroy':
        jixu = raw_input('will destroy all nodes you select, continue? [yes/no]: ')
        if jixu == 'yes':
            destroy(start, end)
    elif param1 == 'undefine':
        jixu = raw_input('will define all nodes you select, continue? [yes/no]: ')
        if jixu == 'yes':
            destroy(start, end)
            time.sleep(1)
            undef(start, end)
    elif param1 == 'help':
        _help()
    else:
        _handle_error_params()


if __name__ == '__main__':
    main()
