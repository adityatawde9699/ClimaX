from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


def test_alembic_revision_chain_has_one_resolvable_head():
    repository_root = Path(__file__).parents[2]
    config = Config(repository_root / "infrastructure/database/alembic.ini")
    config.set_main_option("script_location", str(repository_root / "infrastructure/database/alembic"))
    script = ScriptDirectory.from_config(config)

    assert script.get_current_head() == "0007_google_identity"
    assert [revision.revision for revision in script.walk_revisions()] == [
        "0007_google_identity",
        "0006_query_indexes",
        "0005_ai_analysis_audit_fields",
        "0004_observation_quality_flag",
        "0003",
        "0002",
        "0001",
    ]
