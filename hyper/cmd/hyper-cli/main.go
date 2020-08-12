package main

import (
	"context"
	"fmt"

	"github.com/isard-vdi/isard/hyper/pkg/proto"

	"google.golang.org/grpc"
)

func main() {
	conn, err := grpc.Dial(":1312", grpc.WithInsecure())
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	cli := proto.NewHyperClient(conn)

	// Returns started xml
	//_, err = cli.DesktopStartValidate(context.Background(), &proto.DesktopStartRequest{
	//_, err = cli.DesktopStartPaused(context.Background(), &proto.DesktopStartRequest{
	_, err = cli.DesktopStart(context.Background(), &proto.DesktopStartRequest{
		Xml: `<domain type="kvm">
		<name>domain</name>
		<memory unit="G">2</memory>
		<vcpu placement="static">2</vcpu>
		<os>
		  <type arch="x86_64" machine="q35">hvm</type>
		</os>
		<devices>
		  <input type="keyboard" bus="ps2"></input>
		  <graphics type="spice" listen="0.0.0.0"></graphics>
		  <video>
			<model type="qxl"></model>
		  </video>
		  <controller type='pci' index='0' model='pcie-root'>
			<alias name='pci.0'/>
		  </controller>
		</devices>
	  </domain>`,
	})
	if err != nil {
		panic(err)
	}

	xml, err := cli.DesktopXMLGet(context.Background(), &proto.DesktopXMLGetRequest{
		Id: "domain",
	})
	if err != nil {
		panic(err)
	}
	fmt.Println(xml)

	_, err = cli.DesktopSuspend(context.Background(), &proto.DesktopSuspendRequest{
		Id: "domain",
	})
	if err != nil {
		panic(err)
	}

	list, err := cli.DesktopList(context.Background(), &proto.DesktopListRequest{})
	fmt.Println(list.Ids)

	_, err = cli.DesktopResume(context.Background(), &proto.DesktopResumeRequest{
		Id: "domain",
	})
	if err != nil {
		panic(err)
	}

	_, err = cli.DesktopSave(context.Background(), &proto.DesktopSaveRequest{
		Id:   "domain",
		Path: "domain.dump",
	})
	if err != nil {
		panic(err)
	}

	list, err = cli.DesktopList(context.Background(), &proto.DesktopListRequest{})
	fmt.Println(list.Ids)

	_, err = cli.DesktopRestore(context.Background(), &proto.DesktopRestoreRequest{
		Path: "domain.dump",
	})
	if err != nil {
		panic(err)
	}

	_, err = cli.DesktopStop(context.Background(), &proto.DesktopStopRequest{
		Id: "domain",
	})
	if err != nil {
		panic(err)
	}

	/* _, err = cli.DesktopMigrateLive(context.Background(), &proto.DesktopMigrateLiveRequest{
		Name:         "domain",
		Hypervisor: "192.168.200.206",
		Bandwidth:  9999,
	})
	if err != nil {
		panic(err)
	} */
}
