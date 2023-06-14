from acnestis.processing import Processor
from acnestis.steps import docker

PROCESSOR = Processor(
    [docker("acnestis_svgo", skip_pull=True)],
)
