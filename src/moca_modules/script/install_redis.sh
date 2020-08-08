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
   # ------- Check Redis -------
  if [ "$(command -v redis-cli)" != "" ]; then
    echo "Redis is already installed in $(command -v redis-cli)"
    exit;
  fi
  # ------- Install Redis -------
  echo "Starting install Redis."
  dnf update -y;
  dnf install -y redis;
  systemctl start redis;
  systemctl enable redis;
else
  echo "Error: Only supports CentOS8."
fi