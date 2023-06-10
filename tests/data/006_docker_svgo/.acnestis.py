from acnestis.processing import BaseProcessor
from acnestis.steps import docker

PROCESSOR = BaseProcessor(
    [docker("acnestis_svgo", skip_pull=True)],
)
