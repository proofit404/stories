module.exports = {
  repositoryUrl: "https://github.com/proofit404/stories",
  tagFormat: "${version}",
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/changelog",
      {
        changelogFile: "docs/changelog.md",
      },
    ],
    [
      "@semantic-release/exec",
      {
        prepareCmd: "poetry version ${nextRelease.version} && poetry build",
        publishCmd: "poetry publish",
      },
    ],
    [
      "@semantic-release/git",
      {
        assets: ["docs/changelog.md", "pyproject.toml"],
      },
    ],
    [
      "@semantic-release/github",
      {
        assets: [{ path: "dist/*.whl" }, { path: "dist/*.tar.gz" }],
      },
    ],
  ],
};
