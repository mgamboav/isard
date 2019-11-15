from lxml import etree
from io import StringIO

class XmlParser(object):
    def __init__(self, xml):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            self.tree = etree.parse(StringIO(xml), parser)
            self.clean_xml()
        except Exception as e:
            raise

    def remove_branch(self, xpath, index=0):
        self.tree.xpath(xpath)[index].getparent().remove(self.tree.xpath(xpath)[index])


    def clean_xml(self):
        items = ['disk','graphics','video','interface']
        xpath='/domain[@type="kvm"]/devices/'
        for i in items:
            while len(self.tree.xpath(xpath+i)):
                self.remove_branch(xpath+i)         
            # ~ sub = self.tree.xpath(xpath+i)
            # ~ self.remove_branch(xpath)
            # ~ index=0
            # ~ for s in sub:
                # ~ sub[index].remove()
                # ~ index=index+1
                
    def to_xml(self):
        return etree.tostring(self.tree, encoding='unicode', pretty_print=True)

    def domain_disk_next_dev(self, bus):
        ''' device = disk, cdrom, floppy '''
        ''' bus = virtio, ide, fdc, sata, scsii, ... '''
        try:
            xpath='/domain[@type="kvm"]/devices/disk'
            disks=self.tree.xpath(xpath)
            devs=[]
            idisk = 0
            for d in disks:
                print(d.xpath('target[@dev]')[0].get("bus"))
                if d.xpath('target[@dev]')[0].get("bus") == bus:
                    print(d.xpath('target[@dev]')[0].get("dev"))
                    devs.append(d.xpath('target[@dev]')[0].get("dev"))
                idisk=idisk + 1            
            if len(devs) == 0:
                if bus == 'virtio': dev = 'vda'
                if bus == 'sata': dev = 'sda'
                if bus == 'ide': dev = 'hda'
                if bus == 'fdc': dev = 'fda'
                return dev, None
            devs.sort()                
            last = devs[-1]
            dev = last[:-1] + chr(ord(last[-1])+1)
            return dev, '/domain/devices/disk/target[@dev="'+devs[-1]+'"]'
        except Exception as e:
            raise

   
    def domain_disk_add(self, disk):
        try:
            dev, disk_new_xpath = self.domain_disk_next_dev(disk['bus'])
            disk_xml = disk['xml'].format(format=disk['format'],
                                         source=disk['ppath']+disk['rpath'],
                                         dev=disk['dev'],
                                         bus=disk['bus'])
            disk_etree = etree.parse(StringIO(disk_xml))
            if disk_new_xpath is not None:
                self.tree.xpath(disk_new_xpath)[0].getparent().addnext(disk_etree.getroot())
            else:
                self.tree.xpath('/domain/devices')[-1].append(disk_etree.getroot())
        except Exception as e:
            raise
        return True

    def domain_interface_add(self, interface):
        try:
            interface_xml = interface['xml'].format(source=interface['source'],
                                         mac=interface['mac'],
                                         model=interface['model'])
            interface_etree = etree.parse(StringIO(interface_xml))

            interface_xpath='/domain[@type="kvm"]/devices/interface'
            iface = self.tree.xpath(interface_xpath)
            if len(iface) == 0:
                self.tree.xpath('/domain/devices')[-1].append(interface_etree.getroot())
            else:
                iface[-1].addnext(interface_etree.getroot())
        except Exception as e:
            raise
        return True

    def domain_graphic_add(self, graphic):
        try:
            graphic_xml = graphic['xml'].format()
            graphic_etree = etree.parse(StringIO(graphic_xml))

            graphic_xpath='/domain[@type="kvm"]/devices/graphics'
            graphic = self.tree.xpath(graphic_xpath)
            if len(graphic) == 0:
                self.tree.xpath('/domain/devices')[-1].append(graphic_etree.getroot())
            else:
                graphic[-1].addnext(graphic_etree.getroot())
        except Exception as e:
            raise
        return True

    def domain_video_add(self, video):
        try:
            video_xml = video['xml'].format()
            video_etree = etree.parse(StringIO(video_xml))

            video_xpath='/domain[@type="kvm"]/devices/video'
            video = self.tree.xpath(video_xpath)
            if len(video) == 0:
                self.tree.xpath('/domain/devices')[-1].append(video_etree.getroot())
            else:
                video[-1].addnext(video_etree.getroot())
        except Exception as e:
            raise
        return True
                                    
    def xml_check(self, xml):
        try:
            return etree.parse(StringIO(xml), parser)
            # ~ return True
        except Exception as e:
            # ~ log.error('Exception when parse xml: {}'.format(e))
            # ~ log.error('xml that fail: \n{}'.format(xml))
            # ~ log.error('Traceback: {}'.format(traceback.format_exc()))
            self.parser = False
            raise
            return False

        # ~ self.vm_dict = self.dict_from_xml(self.tree)

        # ~ self.index_disks = {}
        # ~ self.index_disks['virtio'] = 0
        # ~ self.index_disks['ide'] = 0
        # ~ self.index_disks['sata'] = 0
