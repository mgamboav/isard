from lxml import etree
from io import StringIO

class XmlParser(object):
    def __init__(self, xml):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            self.tree = etree.parse(StringIO(xml), parser)
        except Exception as e:
            raise

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
            # ~ print(bus)
            for d in disks:
                print(d.xpath('target[@dev]')[0].get("bus"))
                # ~ if d.get("device") == device and d.xpath('target[@dev]')[0].get("bus") == bus:
                if d.xpath('target[@dev]')[0].get("bus") == bus:
                    print(d.xpath('target[@dev]')[0].get("dev"))
                    devs.append(d.xpath('target[@dev]')[0].get("dev"))
                idisk=idisk + 1            
            if len(devs) == 0:
                if bus == 'virtio': dev = 'vda'
                if bus == 'sata': dev = 'sda'
                if bus == 'ide': dev = 'hda'
                if bus == 'fdc': dev = 'fda'
                # ~ return dev, '/devices/disk['+str(idisk)+']'
                return dev, None
                # ~ '/domain/devices/disk'
                # ~ /target[@dev="'+devs[-1]+'"]'
                # ~ return dev, '/domain/devices/disk[@device="disk"]'
                # ~ return dev, '/devices/disk['+str(idisk)+']/target[@dev="'+dev+'"]'  
            devs.sort()                
            last = devs[-1]
            dev = last[:-1] + chr(ord(last[-1])+1)
            # ~ return dev, '/domain/devices/disk[@device="disk"]'
            return dev, '/domain/devices/disk/target[@dev="'+devs[-1]+'"]'
            # ~ [3]/target[@dev="'+devs[-1]+'"]'                              
            # ~ return dev, '/devices/disk['+str(idisk)+']/target[@dev="'+devs[-1]+'"]'  
        except Exception as e:
            raise

   
    def domain_disk_add(self, disk): #disk_xml, path, format="qcow2xxx", bus="virtio"):
        try:
            dev, disk_new_xpath = self.domain_disk_next_dev(disk['bus'])
            disk_xml = disk['xml'].format(format=disk['format'],
                                         source=disk['ppath']+disk['rpath'],
                                         dev=disk['dev'],
                                         bus=disk['bus'])
            disk_etree = etree.parse(StringIO(disk_xml))
            print(disk_etree)
            print(disk_new_xpath)
            # ~ print(self.tree.xpath(disk_new_xpath))
            if disk_new_xpath is not None:
                self.tree.xpath(disk_new_xpath)[0].getparent().addnext(disk_etree.getroot())
            else:
                self.tree.xpath('/domain/devices/disk')[-1].addnext(disk_etree.getroot())
        except Exception as e:
            raise
        return True
        # ~ xpath_same = '/devices/disk[1]/target[@dev="'+dev+'"]'
        # ~ '/domain/devices/disk[@device="disk"]'
        
        
        # ~ new_tree_xpath.addnext(disk_etree)

        # ~ if self.tree.xpath(xpath_parent):
            # ~ if self.tree.xpath(xpath_same):
                # ~ self.tree.xpath(xpath_same)[-1].addnext(element_tree)

            # ~ elif xpath_next and self.tree.xpath(xpath_next):
                # ~ self.tree.xpath(xpath_next)[0].addprevious(element_tree)

            # ~ elif xpath_previous and self.tree.xpath(xpath_previous):
                # ~ self.tree.xpath(xpath_previous)[-1].addnext(element_tree)

            # ~ else:
                # ~ self.tree.xpath(xpath_parent)[0].insert(1, element_tree)




        # ~ (self,index=0,path_disk='/path/to/disk.qcow',type_disk='qcow2',bus='virtio'):
        # ~ global index_to_char_suffix_disks

        # ~ prefix = BUS_LETTER[bus]
        # ~ index_bus = self.index_disks[bus]
        # ~ xml_snippet = XML_SNIPPET_DISK_CUSTOM.format(type_disk=type_disk,
                                                     # ~ path_disk=path_disk,
                                                     # ~ preffix_descriptor=prefix,
                                                     # ~ suffix_descriptor=index_to_char_suffix_disks[index_bus],
                                                     # ~ bus=bus)
        # ~ disk_etree = etree.parse(StringIO(xml_snippet))
        # ~ new_disk = disk_etree.xpath('/disk')[0]
        # ~ xpath_same = '/domain/devices/disk[@device="disk"]'
        # ~ xpath_next = '/domain/devices/disk[@device="cdrom"]'
        # ~ xpath_previous = '/domain/devices/emulator'
        # ~ self.add_device(xpath_same, new_disk, xpath_next=xpath_next, xpath_previous=xpath_previous)
        # ~ self.index_disks[bus] += 1











                    
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
