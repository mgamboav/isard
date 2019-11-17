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
        try:
            self.tree.xpath(xpath)[index].getparent().remove(self.tree.xpath(xpath)[index])
            return True
        except:
            return False

    def clean_xml(self, item=None):
        if item == 'uuid' or item ==None: self.remove_branch('/domain/uuid') 
        if item == 'memory' or item ==None:
            self.remove_branch('/domain/memory')
            self.remove_branch('/domain/currentMemory')
            self.remove_branch('/domain/maxMemory')  
        if item == 'vcpu' or item ==None: self.remove_branch('/domain/vcpu')
        if item == 'cpu' or item ==None: self.remove_branch('/domain/cpu') 
        if item == 'disk' or item == None :
            device = self.tree.xpath('/domain/devices')[0]
            for disk in device.findall(".//disk"):
                device.remove(disk)         
        if item == 'graphics' or item ==None:
            device = self.tree.xpath('/domain/devices')[0]
            for graphic in device.findall(".//graphics"):
                device.remove(graphic)    
        if item == 'video' or item ==None:
            device = self.tree.xpath('/domain/devices')[0]
            for video in device.findall(".//video"):
                device.remove(video)   
        if item == 'interface' or item ==None:
            device = self.tree.xpath('/domain/devices')[0]
            for interface in device.findall(".//interface"):
                device.remove(interface)   
        if item == 'boot' or item == None :
            os = self.tree.xpath('/domain/os')[0]
            for boot in os.findall(".//boot") + os.findall(".//bootmenu"):
                os.remove(boot)
        if item == 'sound' or item == None :
            device = self.tree.xpath('/domain/devices')[0]
            for sound in device.findall(".//sound"):
                device.remove(sound) 
                                
    def to_xml(self):
        return etree.tostring(self.tree, encoding='unicode', pretty_print=True)

    def domain_name_update(self, name):
        self.tree.xpath('/domain/name')[0].text = name

    def domain_vcpu_update(self, vcpu, remove=False):
        if remove: self.clean_xml('vcpu')
        try:
            vcpu_xml = vcpu['xml'].format(vcpu=vcpu['vcpu'])
            vcpu_etree = etree.parse(StringIO(vcpu_xml))
            self.tree.xpath('/domain/name')[0].addnext(vcpu_etree.getroot())
        except Exception as e:
            raise
        return True

    def domain_cpu_update(self, cpu, remove=False):
        if remove: self.clean_xml('cpu')
        try:
            cpu_xml = cpu['xml'].format(match=cpu['match'],
                                        fallback=cpu['fallback'],
                                        model=cpu['model'])
            cpu_etree = etree.parse(StringIO(cpu_xml))
            self.tree.xpath('/domain/os')[0].addnext(cpu_etree.getroot())
        except Exception as e:
            raise
        return True
                
    def domain_memory_update(self, memory, remove=False):
        if remove: self.clean_xml('memory')
        try:
            memory_xml = memory['xml'].format(unit=memory['unit'],
                                         maxmemory=str(memory['maxmemory']),
                                         memory=str(memory['memory']),
                                         currentmemory=str(memory['currentmemory']))
            memory_xmls = memory_xml.splitlines()
            memory_etrees = [etree.parse(StringIO(memory_xml)) for memory_xml in memory_xmls if memory_xml is not ""]
            [self.tree.xpath('/domain/name')[0].addnext(memory_etree.getroot()) for memory_etree in memory_etrees]
        except Exception as e:
            raise
        return True

    def domain_boot_update(self,boot_devs, menu=False):
        try:
            self.clean_xml(item='boot')
            dev_xml = '''<boot dev="{dev}"/>'''
            menu_xml = '''<bootmenu enable="{menu}"/>'''
            boots_xml = [dev_xml.format(dev=bd) for bd in boot_devs]
            boots_etree = [etree.parse(StringIO(boot_xml)) for boot_xml in boots_xml]
            for be in boots_etree:
                self.tree.xpath('/domain/os')[0].insert(-1, be.getroot())
            menu_xml = menu_xml.format(menu='yes' if menu else 'no')
            menu_etree = etree.parse(StringIO(menu_xml))
            self.tree.xpath('/domain/os')[0].insert(-1, menu_etree.getroot()) 
        except Exception as e:
            raise
        return True
                                                                     
    def domain_disk_next_dev(self, bus):
        ''' device = disk, cdrom, floppy '''
        ''' bus = virtio, ide, fdc, sata, scsii, ... '''
        try:
            xpath='/domain[@type="kvm"]/devices/disk'
            disks=self.tree.xpath(xpath)
            devs=[]
            idisk = 0
            for d in disks:
                # ~ print(d.xpath('target[@dev]')[0].get("bus"))
                if d.xpath('target[@dev]')[0].get("bus") == bus:
                    # ~ print(d.xpath('target[@dev]')[0].get("dev"))
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

   
    def domain_disk_add(self, disk, remove=False):
        if remove: self.clean_xml('disk')
        try:
            dev, disk_new_xpath = self.domain_disk_next_dev(disk['bus'])
            disk_xml = disk['xml'].format(format=disk['format'],
                                         source=disk['ppath']+disk['rpath']+disk['filename'],
                                         dev=dev,
                                         bus=disk['bus'])
            disk_etree = etree.parse(StringIO(disk_xml))
            if disk_new_xpath is not None:
                self.tree.xpath(disk_new_xpath)[0].getparent().addnext(disk_etree.getroot())
            else:
                self.tree.xpath('/domain/devices')[-1].append(disk_etree.getroot())
        except Exception as e:
            raise
        return True

    def domain_interface_add(self, interface, remove=False):
        if remove: self.clean_xml('interface')
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

    def domain_graphic_add(self, graphic, remove=False):
        if remove: self.clean_xml('graphics')
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

    def domain_video_add(self, video, remove=False):
        if remove: self.clean_xml('video')
        try:
            video_xml = video['xml'].format()
            video_etree = etree.parse(StringIO(video_xml))

            video_xpath='/domain/devices/video'
            video = self.tree.xpath(video_xpath)
            if len(video) == 0:
                self.tree.xpath('/domain/devices')[-1].append(video_etree.getroot())
            else:
                video[-1].addnext(video_etree.getroot())
        except Exception as e:
            raise
        return True

    def domain_sound_add(self, sound, remove=False):
        if remove: self.clean_xml('sound')
        try:
            sound_xml = sound['xml'].format()
            sound_etree = etree.parse(StringIO(sound_xml))

            sound_xpath='/domain/devices/sound'
            sound = self.tree.xpath(sound_xpath)
            if len(sound) == 0:
                self.tree.xpath('/domain/devices')[-1].append(sound_etree.getroot())
            else:
                sound[-1].addnext(sound_etree.getroot())
        except Exception as e:
            raise
        return True
                                            
    def xml_check(self, xml):
        try:
            return etree.parse(StringIO(xml), parser)
        except Exception as e:
            # ~ log.error('Exception when parse xml: {}'.format(e))
            # ~ log.error('xml that fail: \n{}'.format(xml))
            # ~ log.error('Traceback: {}'.format(traceback.format_exc()))
            raise
            
