"""Initial creation

Revision ID: cb71a0e5b507
Revises: 
Create Date: 2019-11-07 19:20:01.517946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
# ~ from models.base_mixin import BaseMixin
from models.domain import Domain
from models.template import Template
from models.vm import *
from models.hypervisor import *

from models.snippets import XMLHelper

# ~ Base, vm, Boot, Interface, Graphic, Video, Disk, DiskBus, DiskFormat
# Iso, Floppy

Session = sessionmaker()


# revision identifiers, used by Alembic.
revision = 'cb71a0e5b507'
down_revision = None
branch_labels = None
depends_on = None

xml = XMLHelper()


    
def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    
    session = Session(bind=bind)
    
   
    ## Add virtio-install xmls 
    session.bulk_save_objects([VmXML(name=x['name'], xml=x['xml']) for x in xml.get_virtinstalls()])
    
    ## Add snippet xmls
    session.bulk_save_objects([DiskXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('disk')])
    session.bulk_save_objects([MediaXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('media')])
    session.bulk_save_objects([InterfaceXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('interface')])
    session.bulk_save_objects([GraphicXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('graphic')])
    session.bulk_save_objects([VideoXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('video')])
    session.bulk_save_objects([MemoryXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('memory')])
    session.bulk_save_objects([VcpuXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('vcpu')])
    session.bulk_save_objects([CpuXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('cpu')])
    session.bulk_save_objects([SoundXML(name=i['name'], xml=i['xml']) for i in xml.get_snippets('sound')])
    ################################3
    # New vm.
    ## Get xml for new vm
    d_xml = session.query(VmXML).filter(VmXML.name == 'altlinux1.0').one()
    
    ## Create the vm
    d = Domain(name="_t_e_s_t_", vm_xml=d_xml) #, vcpu = 1, memory = 768)

    mem_xml = session.query(MemoryXML).filter(MemoryXML.name == 'balloon').one()
    mem = Vm_Memory(vm_id=d, memory_id=mem_xml.id, mem=1500)
    d.memory.append(mem) 
    
    vcpu_xml = session.query(VcpuXML).filter(VcpuXML.name == 'vcpu').one()
    vcpu = Vm_Vcpu(vm_id=d, vcpu_id=vcpu_xml.id, vcpus=2)
    d.vcpu.append(vcpu) 

    cpu_xml = session.query(CpuXML).filter(CpuXML.name == 'host-model').one()
    cpu = Vm_Cpu(vm_id=d, cpu_id=cpu_xml.id)
    d.cpu.append(cpu)
          
    # ~ sound_xml = session.query(SoundXML).filter(SoundXML.name == 'ich6').one()
    # ~ sound = Vm_Sound(vm_id=vm, sound_id = sound_xml.id)
    # ~ vm.sound.append(sound)
          
    ### Boot
    db = Boot(vm_id=d.id, name='BOOT_NETWORK') #, order=1)
    d.boot.append(db)
    db = Boot(vm_id=d.id, name='BOOT_HD') #, order=1)
    d.boot.append(db)
    db = Boot(vm_id=d.id, name='BOOT_CD') #, order=1)
    d.boot.append(db)
    

    # ~ print(Boot.filter_by(name='disk').first())
    ### Hard disk
    dd_xml = session.query(DiskXML).filter(DiskXML.name == 'disk').one()
    dd = Disk(vm_id=d.id, xml=dd_xml, name='____', filename="____.qcow2", bus='virtio', size=10, format='qcow2')
    d.disk.append(dd)

    ### Medias
    # ~ dm_xml = session.query(MediaXML).filter(MediaXML.name == 'iso').one()
    # ~ dm = Vm_Media(vm_id=vm.id, media_id=dm_xml.id, filename="____.iso", order=1)
    # ~ vm.medias.append(dm)
    
    ### Interfaces
    di_xml = session.query(InterfaceXML).filter(InterfaceXML.name == 'network').one()
    di = Vm_Interface(vm_id=d, interface_id=di_xml.id, model='virtio', source='default', order=1)
    # ~ , mac='11:22:33:44:55:66', order=1)
    d.interfaces.append(di)        
    session.add(d) 
    
    ### Graphics
    # ~ dg_xml = session.query(GraphicXML).filter(GraphicXML.name == 'spice').one()
    # ~ dg = Vm_Graphic(vm_id=vm, graphic_id=dg_xml.id, order=1)
    # ~ vm.graphic.append(dg)
    
    ### Videos
    # ~ dv_xml = session.query(VideoXML).filter(VideoXML.name == 'qxl').one()
    # ~ dv = Vm_Video(vm_id=vm, video_id=dv_xml.id, order=1)
    # ~ vm.videos.append(dv)
    
    
    
    ##########################################
    ### Hypervisor
    ##########################################
    hv = ViewerCertificate(name='default', 
                        default_mode='secure',
                        certificate='certificate ac po984wyt',
                        server_cert='server cert afjñw49iwp948f',
                        host_subject='',
                        domain='isardvdi.com')
    session.add(hv)
    session.flush()
    cpu_xml = session.query(CpuXML).filter(CpuXML.name == 'host-passthrough').one()
    hp = HypervisorPool(name='default',
                        viewer_certificate_id=hv.id,
                        cpu_id=cpu_xml.id)
    session.add(hp)
    session.flush()
    h = Hypervisor(hostname='isard-hypervisor',
                    passwd='pass',
                    hypervisor_pool_id=hp.id)
    session.add(h)
    session.flush()
    acl = Acl(hypervisor_pool_id=hp.id,
                order=1,
                src='',
                dst='',
                weight=100,
                hypervisor_id=h.id)
    # ~ h.hypervisor_pool_id.append(hp) 
    session.add(acl)
    session.flush()
    # ~ vm.boot.append(db)
    # ~ vm.boot.reorder()        
    session.commit()

def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
