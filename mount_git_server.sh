#!/bin/bash

#git directionay
git_server='/home/cjling/006_git_server'

#server password
password='916sa((('

#cjling
proj_name='k-vim'
#proj_name='leetcode'
#proj_name='linux_package'
#proj_name='linux_setting'
#proj_name='oh-my-zsh'

#proj
#proj_name='ZXCCP-VPlat_CVM-trunk-source.repo-src-openstack-nova'
#proj_name='ZXCCP-VPlat_CVM-trunk-source.repo-src-python-novaclient'
#proj_name='ZXCCP-VPlat_CVM-trunk-source.repo-src-openstack-cinder'
#proj_name='ZXCCP-VPlat_CVM-trunk-source.repo-src-openstack-neutron'

pc_ip='10.74.30.154'
path='clone_from_git'
#path='clone_from_svn'

mkdir $git_server/$proj_name
mount -t cifs -o username=10132915,domain=zte.intra,password=$password //$pc_ip/proj/001_git/$path/$proj_name $git_server/$proj_name