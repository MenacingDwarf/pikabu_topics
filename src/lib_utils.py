from pathlib import Path


class PathLoader():

    def __init__(self, path=None):
        if not path:
            self.main_dir = Path(__file__).resolve().parent.parent
        else:
            self.main_dir = Path(path)

        self.configs = self.main_dir / "configs"
        self.models = self.main_dir / "models"
        self.reports = self.main_dir / "reports"
        self.data = self.main_dir / "data"
