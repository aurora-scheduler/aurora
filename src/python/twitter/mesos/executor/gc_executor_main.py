import os

from twitter.common import app, log
from twitter.common.log.options import LogOptions
from twitter.common_internal.app.modules import chickadee_handler
from twitter.thermos.base.path import TaskPath

from .gc_executor import ThermosGCExecutor

import mesos


LogOptions.set_log_dir('executor_logs')
LogOptions.set_disk_log_level('DEBUG')
app.configure(module='twitter.common_internal.app.modules.chickadee_handler',
    service_name='thermos_gc_executor')
app.configure(debug=True)


if 'META_THERMOS_ROOT' in os.environ:
  CHECKPOINT_ROOT = os.path.join(os.environ['META_THERMOS_ROOT'], 'checkpoints')
else:
  CHECKPOINT_ROOT = TaskPath.DEFAULT_CHECKPOINT_ROOT


def main():
  thermos_gc_executor = ThermosGCExecutor(checkpoint_root=CHECKPOINT_ROOT)
  drv = mesos.MesosExecutorDriver(thermos_gc_executor)
  drv.run()
  log.info('MesosExecutorDriver.run() has finished.')


app.main()
