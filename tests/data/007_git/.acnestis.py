from acnestis.processing import BaseProcessor
from acnestis.steps import git

PROCESSOR = BaseProcessor(
    [git("https://github.com/oduvan/acnestis-test-repo.git", branch="main")],
)
