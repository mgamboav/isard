osinfo-query os > osinfo.txt
for os in $(osinfo-query --fields=short-id os | tail -n +3); do \
virt-install --import --name $os  --os-variant $os --network=bridge=br \
--dry-run --print-xml --disk none --memory=2048 \
--disk /home/tmp/disk.qcow2,device=disk \
--disk /home/tmp/cdrom.iso,device=cdrom \
--disk /home/tmp/floppy.img,device=floppy \
--boot network,cdrom,fd,hd,menu=on\
> $os.xml; done
