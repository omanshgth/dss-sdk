"""

   BSD LICENSE

   Copyright (c) 2021 Samsung Electronics Co., Ltd.
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:

     * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
     * Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in
       the documentation and/or other materials provided with the
       distribution.
     * Neither the name of Samsung Electronics Co., Ltd. nor the names of
       its contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from ufm_thread import UfmThread
from systems.switch import switch_constants
from systems.switch.switch_mellanox.switch_mellanox_client import SwitchMellanoxClient


class SwitchPoller(UfmThread):
    def __init__(self, swArg):
        self.swArg = swArg
        self.log = self.swArg.log
        self.repeat_interval_secs = switch_constants.SWITCH_POLLER_INTERVAL_SECS

        self._running = False
        self.client = None

        super(SwitchPoller, self).__init__()
        self.log.info("Init {}".format(self.__class__.__name__))

    def __del__(self):
        if self._running:
            self.stop()
        self.log.info("Del {}".format(self.__class__.__name__))

    def start(self):
        self.log.info("Start {}".format(self.__class__.__name__))

        if self.swArg.sw_type.lower() == 'mellanox':
            self.client = SwitchMellanoxClient(self.swArg)
        else:
            raise Exception('Invalid switch type, {} is not valid'.format(self.swArg.sw_type))

        self._running = True
        super(SwitchPoller, self).start(
                    threadName='SwitchPoller',
                    cb=self._poller,
                    cbArgs=self.swArg,
                    repeatIntervalSecs=self.repeat_interval_secs)

    def stop(self):
        super(SwitchPoller, self).stop()
        self._running = False
        self.log.info("Stop {}".format(self.__class__.__name__))

    def is_running(self):
        return self._running

    def _poller(self, ufmArg):
        # print("_SP_", flush=True, end='')
        self.client.poll_to_db()
