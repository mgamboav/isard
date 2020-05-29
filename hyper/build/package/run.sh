echo "Generating selfsigned certs for spice client..."
sh auto-generate-certs.sh
echo "Starting libvirt daemon..."
/usr/sbin/virtlogd &
/usr/sbin/libvirtd &
sleep 2
/usr/bin/virsh net-start default
echo "Checking hypervisor..."
echo "[1/1] basic domain start..."
virsh create checks/domain.xml
virsh destroy domain

/hyper