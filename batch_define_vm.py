#!/bin/env python
import commands
import time

#src_qcow = "/zl/backup/ins_cephrpms_vimwget_20200702.qcow2"
src_qcow = "/zl/big_nodes/template.qcow2"
xml_path = "/zl/big_nodes/xml"
qcow_path = "/zl/big_nodes/qcow"

num = raw_input('Please input num of nodes: ')

for i in range(61, int(num)+61):
    name = 'node'+str(i)
    port = 5910 + int(i)
    cmd1 = 'cp {} {}/{}'.format(src_qcow, qcow_path, name+'.qcow2')
    commands.getoutput(cmd1)
    cmd2 = 'qemu-img create -f qcow2 /zl/big_nodes/data/%(name)s_1.qcow2 30G' % ({'name': name})
    commands.getoutput(cmd2)
    xml_str = """
<domain type='kvm'>
  <name>%(name)s</name>
  <memory unit='Gib'>12</memory>
  <currentMemory unit='Gib'>12</currentMemory>
  <vcpu>8</vcpu>
  <os>
    <type arch='x86_64' machine='pc'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='localtime'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/zl/big_nodes/qcow/%(name)s.qcow2'/>
      <target dev='hda' bus='virtio'/>
    </disk>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/zl/big_nodes/data/%(name)s_1.qcow2'/>
      <target dev='hdb' bus='virtio'/>
    </disk>
    <channel type='unix'>
      <target type='virtio' name='org.qemu.guest_agent.0'/>
    </channel>
    <controller type='virtio-serial' index='0'>
    </controller>
    <interface type='bridge'>
      <source bridge='br-ex'/>
      <model type='virtio'/>
    </interface>
    <interface type='bridge'>
      <source bridge='br-ex'/>
      <model type='virtio'/>
    </interface>
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='%(port)s' autoport='no' listen = '0.0.0.0' keymap='en-us'/>
  </devices>
</domain>
    """
    xml_str = xml_str % {'name': name, 'port': port}
    new_xml = xml_path + "/node" + str(i) + '.xml'
    with open(new_xml, 'w') as f:
        f.write(xml_str)
    # define
    cmd3 = 'virsh define {}/{}.xml'.format(xml_path, name)
    commands.getoutput(cmd3)
    # start
    cmd4 = 'virsh start ' + name
    commands.getoutput(cmd4)
    time.sleep(10)
