from __future__ import absolute_import

import logging

import minemeld.comm

LOG = logging.getLogger(__name__)


class Fabric(object):
    def __init__(self, chassis, config, comm_class):
        self.chassis = chassis

        self.comm_config = config
        self.comm_class = comm_class

        self.comm = minemeld.comm.factory(self.comm_class, self.comm_config)

    def request_rpc_channel(self, ftname, ft, allowed_methods):
        self.comm.request_rpc_server_channel(ftname, ft, allowed_methods)

    def request_pub_channel(self, ftname):
        return self.comm.request_pub_channel(ftname)

    def request_sub_channel(self, ftname, ft, subname, allowed_methods):
        self.comm.request_sub_channel(subname, ft, allowed_methods)

    def send_rpc(self, sftname, dftname, method, params,
                 block=True, timeout=None):
        params['source'] = sftname
        self.comm.send_rpc(
            dftname,
            method,
            params,
            block=block,
            timeout=timeout
        )

    def _comm_failure(self):
        self.chassis.fabric_failed()

    def start(self):
        LOG.debug("fabric start called")
        self.comm.add_failure_listener(self._comm_failure)
        self.comm.start()

    def stop(self):
        LOG.debug("fabric stop called")
        self.comm.stop()


def factory(classname, chassis, config):
    return Fabric(
        chassis=chassis,
        config=config,
        comm_class=classname
    )