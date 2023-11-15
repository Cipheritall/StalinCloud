# StalinCloud Instruction

# Mount the hard drive
Once the memory device is plugged, run the following command to get it's path in /dev/
```
 lsblk 
```
after identifying the path, configure the mount in /etc/fstab to allow write access to your user by adding this line
- /etc/fstab
```
[..]
/dev/sdb /media/sdcard auto user,umask=000,utf8,noauto 0 0
```
mount it using the following command
```
sudo mount /dev/sdb
```
