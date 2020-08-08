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
  # ------- Check Python3.8 -------
  if [ "$(command -v python3.8)" != "" ]; then
    echo "python3.8 is already installed in $(command -v python3.8)"
    exit;
  fi
  # ------- Install Python3.8 -------
  echo "Starting install python3.8."
  cd "$HOME" || exit;
  dnf update -y;
  dnf -y groupinstall "Development Tools";
  dnf -y install openssl-devel bzip2-devel libffi-devel wget;
  mkdir python-code-tmp;
  cd python-code-tmp || exit;
  wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz;
  tar xvf Python-3.8.3.tgz;
  cd Python-3.8*/ || exit;
  ./configure --enable-optimizations;
  make altinstall;
  cd .. || exit;
  rm -rf "$HOME/python-code-tmp";
  python_path=$(command -v python3.8);
  echo "Your path of python3.8 is $python_path"
  # ----------------------------------
else
  echo "Error: Only supports CentOS8."
fi