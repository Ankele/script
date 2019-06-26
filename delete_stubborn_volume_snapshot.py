#! -*- coding: utf-8 -*-
import commands
import threading

"""
存储池被清理后，卷和快照在数据库中的记录不能被删除
1、修改cinder/volume/drivers/rbd.py中 delete_volume和delete_snapshot
    在第一行插入return即可
2、执行本脚本
"""

source_type = "volume"

def do():
    cmd_lst = source_type=='volume' and "cinder list | awk '{print $2}'" or "cinder snapshot-list | awk '{print $2}'"
    thread_list = []
    commands.getoutput('. /root/admin-open.rc')
    ress = commands.getoutput(cmd_lst)
    item_list = ress.split('\n')[3:]
    for item in item_list:
        if not item:
            continue
        t = threading.Thread(target=delete, args=(item,))
        t.setDaemon(True)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


def delete(item):
    cmd_reset = source_type=='snapshot' and 'cinder snapshot-reset-state --state error %s' % item or "cinder reset-state --state available %s" % item
    if source_type == 'snapshot':
        commands.getoutput(cmd_reset)
    cmd_delete = source_type=='snapshot' and 'cinder snapshot-delete %s' % item or 'cinder delete %s' % item
    commands.getoutput(cmd_delete)


do()
source_type = 'snapshot'
do()
