#!/bin/bash
now="$(date +'%d_%m_%Y_%H_%M_%S')"
filename="db_backup.sql"
backupfolder="/carparker/db_dump"
fullpathbackupfile="$backupfolder/$now/$filename"
mkdir -p "$backupfolder/$now"
mysqldump -hparker-db --user=root --password=root --default-character-set=utf8 parker > "$fullpathbackupfile"
rm "$backupfolder/latest"
ln -s "$backupfolder/$now" "$backupfolder/latest"



