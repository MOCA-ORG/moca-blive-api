#!/bin/sh

# Ω*
#               ■          ■■■■■  
#               ■         ■■   ■■ 
#               ■        ■■     ■ 
#               ■        ■■       
#     ■■■■■     ■        ■■■      
#    ■■   ■■    ■         ■■■     
#   ■■     ■■   ■          ■■■■   
#   ■■     ■■   ■            ■■■■ 
#   ■■■■■■■■■   ■              ■■■
#   ■■          ■               ■■
#   ■■          ■               ■■
#   ■■     ■    ■        ■■     ■■
#    ■■   ■■    ■   ■■■  ■■■   ■■ 
#     ■■■■■     ■   ■■■    ■■■■■

# """
# Copyright (c) 2020.5.28 [el.ideal-ideas]
# This software is released under the MIT License.
# see LICENSE.txt or following URL.
# https://www.el-ideal-ideas.com/MocaSystem/LICENSE/
# """

export LC_ALL=C
linux_info=$(cat /etc/redhat-release)
echo "Linux Version: $linux_info"
if [ "${linux_info:0:22}" = "CentOS Linux release 8" ]; then
   # ------- Check MariaDB -------
  if [ "$(command -v mysql)" != "" ]; then
    echo "Mysql is already installed in $(command -v mysql)"
    exit;
  fi
  # ------- Install MariaDB -------
  echo "Starting install MariaDB."
  dnf update -y;
  dnf install -y mariadb-server mariadb mariadb-devel;
  systemctl start mariadb;
  systemctl enable mariadb;
  mysql_secure_installation;
else
  echo "Error: Only supports CentOS8."
fi