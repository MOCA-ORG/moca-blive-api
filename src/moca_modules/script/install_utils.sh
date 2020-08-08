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
  # ------- Install Utils -------
  echo "Starting install Utilities."
  dnf update -y;
  dnf install emacs htop unzip git wget;
  echo "Utilities installed."
else
  echo "Error: Only supports CentOS8."
fi