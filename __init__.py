# -*- coding:utf-8 -*-  
from version import VERSION

_version_ = VERSION

from Remotelibrary  import import_remote_key


class AutomatedLib(import_remote_key):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'