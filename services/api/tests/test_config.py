from missioncloud_value_hub.config import Settings


def test_cors_origins_accept_comma_separated_values(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3001",
    )

    settings = Settings(_env_file=None)

    assert settings.cors_origins == [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
