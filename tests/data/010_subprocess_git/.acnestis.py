from acnestis.processing import Processor
from acnestis.steps import git

PROCESSOR = Processor(
    [
        Processor(
            [git("https://github.com/oduvan/acnestis-test-repo.git", branch="main")],
            folder="sub/main",
        ),
    ]
)
