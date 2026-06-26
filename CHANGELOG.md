# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.1] - 2026-06-26

### Fixed

- Crash on group and gym contest URLs (`/group/...`): scraper now uses the original URL instead of rewriting to `/problemset/problem/...`
- Clear error message when problem statement is not found (e.g. page requires login)
- Blog post link now correctly reflects the original URL rather than always pointing to `/problemset/`

## [0.1.0] - 2026-06-25

### Added

- `cpscribe post` command: scrapes Codeforces problem page, generates a structured blog post
- `cpscribe init` command: interactive config setup
- Config file at `~/.config/cpscribe/config` with `CPSCRIBE_BLOG_ROOT` / `CPSCRIBE_AUTHOR` env overrides
- URL extraction from `.cpp` file comments
