import json
import unittest
from pathlib import Path


class TestPhaseOneFoundation(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).parent.parent.parent

    def test_seed_fixtures_match_development_baseline(self):
        fixtures = self.root / "data" / "fixtures"
        organizations = json.loads((fixtures / "organizations_seed.json").read_text())
        sensors = json.loads((fixtures / "sensors_seed.json").read_text())
        self.assertEqual(len(organizations), 3)
        self.assertEqual(len(sensors), 10)
        self.assertTrue(all("location" in sensor for sensor in sensors))

    def test_migration_and_local_setup_assets_exist(self):
        required = [
            "apps/api/core/database.py",
            "infrastructure/database/alembic/env.py",
            "infrastructure/database/alembic/versions/0001_initial_schema.py",
            "scripts/seed-db.py",
            "docs/development/local-setup.md",
            ".vscode/settings.json",
        ]
        for item in required:
            self.assertTrue((self.root / item).is_file(), item)


if __name__ == "__main__":
    unittest.main()
