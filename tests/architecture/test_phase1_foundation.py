import unittest
from pathlib import Path


class TestPhaseOneFoundation(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).parent.parent.parent

    def test_migration_and_local_setup_assets_exist(self):
        required = [
            "apps/api/core/database.py",
            "infrastructure/database/alembic/env.py",
            "infrastructure/database/alembic/versions/0001_initial_schema.py",
            "docs/development/local-setup.md",
            ".vscode/settings.json",
        ]
        for item in required:
            self.assertTrue((self.root / item).is_file(), item)


if __name__ == "__main__":
    unittest.main()
