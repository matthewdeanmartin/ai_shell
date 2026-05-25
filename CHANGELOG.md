# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2024-01-21
### Changed
- Integrate metametameta and documentation updates

## [1.0.3] - 2024-01-01
### Added
- Add todo bot with instructions and mission files for AI-assisted task management
- Add backup and restore utility module
- Reorganize AI logging into dedicated ai_logs subpackage with separate JSON, Markdown, and bash log handlers

## [1.0.2] - 2023-12-29
### Fixed
- Demo bot fixes

## [1.0.1] - 2023-12-29
### Changed
- Improve demo bots (docs writer, pylint, test writer, tool tester) with expanded setup and configuration
- Add zip-builder script and reduce fish_tank bundle size
- Expand rewrite tool and read_fs utility tests

## [1.0.0] - 2023-12-29
### Added
- Add ai_shell.toml configuration file support
- Add demo bots infrastructure with dedicated demo_setup module
- Add externals package exposing black, pygount, pylint, and pytest integrations
### Changed
- Expand CLI entry point with richer argument handling
- Update code generation to produce toolkit and schema artifacts

## [0.1.3] - 2023-12-25
### Added
- Add black formatting tool integration via externals module
- Add pygount code metrics integration via externals module
- Expose public API additions in package __init__
### Changed
- Improve cut, ed, edlin, and patch tool implementations

## [0.1.2] - 2023-12-25
### Fixed
- Monkey patch issues

## [0.1.1] - 2023-12-24
### Changed
- Update README and documentation files
- Update pre-commit configuration and add markdownlint config
- Update pyproject.toml dependencies and bot glue module

## [0.1.0] - 2023-12-24
### Added
- Initial release

[1.0.4]: https://github.com/matthewdeanmartin/ai_shell/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/matthewdeanmartin/ai_shell/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/matthewdeanmartin/ai_shell/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/matthewdeanmartin/ai_shell/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/matthewdeanmartin/ai_shell/compare/v0.1.3...v1.0.0
[0.1.3]: https://github.com/matthewdeanmartin/ai_shell/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/matthewdeanmartin/ai_shell/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/matthewdeanmartin/ai_shell/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/matthewdeanmartin/ai_shell/releases/tag/v0.1.0
