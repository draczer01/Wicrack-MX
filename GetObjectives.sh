#!/bin/bash
objectives=$(nmcli d wifi list)

for line in $objectives
do
    echo "${line} Ekisde"
done