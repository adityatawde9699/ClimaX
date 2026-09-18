import unittest
from pathlib import Path


class TestArchitectureScaffolding(unittest.TestCase):
    def test_core_directories_exist(self):
        root = Path(__file__).parent.parent.parent
        expected_dirs = [
            "apps/web",
            "apps/api",
            "packages/types",
            "packages/ui",
            "packages/config",
            "packages/utils",
            "services/ai",
            "services/prediction",
            "services/geospatial",
            "services/environmental-data",
            "services/alerts",
            "services/analytics",
            "data/schemas",
            "infrastructure/docker",
            "infrastructure/gcp",
            "infrastructure/database",
            "docs/architecture",
            "docs/product",
            "docs/ai",
            "docs/data",
            "docs/decisions",
        ]
        for directory in expected_dirs:
            dir_path = root / directory
            self.assertTrue(dir_path.exists(), f"Required directory {directory} is missing")
            self.assertTrue(dir_path.is_dir(), f"Expected {directory} to be a directory")

    def test_no_hardcoded_secrets_in_env_example(self):
        root = Path(__file__).parent.parent.parent
        env_example = root / ".env.example"
        self.assertTrue(env_example.exists())
        content = env_example.read_text()

        # Verify no real credentials
        forbidden_tokens = ["AIza" + "Sy", "gh" + "p_", "s" + "k-", "xox" + "b-"]
        for token in forbidden_tokens:
            self.assertNotIn(token, content, "Potentially live credential detected in .env.example")


if __name__ == "__main__":
    unittest.main()
