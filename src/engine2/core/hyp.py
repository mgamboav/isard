# Copyright 2019 the Isard-vdi project authors:
#      Alberto Larraz Dalmases
#      Josep Maria Viñolas Auquer
# License: AGPLv3

import libvirt

from engine2.common.exceptions import UnAcceptedValueConnectionHypParameters



class Hyp(object):
    """Operates with libvirt hypervisor

    Try connect with ssh with detailed error, create connexions, register stats.

    Args:
        hostname (str): valid hostname to connect via ssh.
        username (Optional[str]): Defaults to 'root'.
        port (Optional[int]): Defaults to 22.

    Attributes:
        conn: Libvirt connection if established

    """
    def __init__(self, hostname: str, username: str = 'root', port: int = 22):
        """Try to connect to hypervisor
        Raises:
            UnAcceptedValueConnectionHypParameters: if port or hostname are invalid"""

        self.verify_parameters_ssh(port,hostname,username)
        self.port = port
        self.hostname = hostname
        self.username = username


    def verify_parameters_ssh(self,port,hostname,username):
        if type(port) is not int:
            raise UnAcceptedValueConnectionHypParameters("Port for ssh connection must be integer")
        if type(address) is not str:
            raise UnAcceptedValueConnectionHypParameters("Hostname for ssh connection must be string")
        if type(username) is not str:
            raise UnAcceptedValueConnectionHypParameters("Username for ssh connection must be string")

        #port between 1 and 2^16
        if 1 < port < pow(2, 16):
            port = int(port)
        else:
            log.error("port to connect hypervisor {} is not valid: {port}")
            raise UnAcceptedValueConnectionHypParameters("Port innvalid, must be between 1 and 2^16: {port}")

        #test if hostame is valid
        if hostname[-1] == ".":
            hostname = hostname[:-1]  # strip exactly one dot from the right, if present
        #allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        #if all(allowed.match(x) for x in hostname.split(".")) is False:
        if all(x.find(' ')<0 for x in hostname.split('.')):
            raise UnAcceptedValueConnectionHypParameters(f"Hostname as space characters: {hostname}")

        if all(x.find(' ')<0 for x in username.split('.')):
            raise UnAcceptedValueConnectionHypParameters(f"Username as space characters: {username}")


