import nox


nox.options.default_venv_backend = "uv"

TEST_DEPS = [
    "pytest<9",
    "pytest-cache<2",
    "pytest-cov<7",
    "WebTest<4",
]

MARSHMALLOW_VERSIONS = {
    "marshmallow3": "marshmallow>=3.13,<4",
    "marshmallow4": "marshmallow>=4",
}


@nox.parametrize("marshmallow", list(MARSHMALLOW_VERSIONS.keys()))
@nox.session
def tests(session: nox.Session, marshmallow: str) -> None:
    session.install(".", *TEST_DEPS, MARSHMALLOW_VERSIONS[marshmallow])
    session.run("pytest", "tests/", "-v", *session.posargs)
