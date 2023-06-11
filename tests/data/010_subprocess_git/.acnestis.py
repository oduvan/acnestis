from acnestis.processing import BaseProcessor
from acnestis.steps import git

PROCESSOR = BaseProcessor(
    processors=[
        BaseProcessor(
            [git("https://github.com/oduvan/acnestis-test-repo.git", branch="main")],
            folder="sub/main",
        ),
    ]
)
