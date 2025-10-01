#!/usr/bin/env python3
import platform
import sys
import os
import title

if platform.system() != "Windows" and os.getuid() == 0:
  print("\033[31mCritical Error: root should not be running user processes")
  sys.exit(1)

title.title()
