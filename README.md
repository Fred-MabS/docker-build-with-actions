# docker-build-with-actions

## badges

![Unit Test](https://github.com/Fred-MabS/docker-build-with-actions/actions/workflows/unittest.yml/badge.svg)

![Build](https://github.com/Fred-MabS/docker-build-with-actions/actions/workflows/docker-image.yml/badge.svg)

[![Known Vulnerabilities](https://snyk.io/test/github/Fred-MabS/docker-build-with-actions/badge.svg)](https://snyk.io/test/github/Fred-MabS/docker-build-with-actions)



[![Mega-Linter@master](https://github.com/Fred-MabS/docker-build-with-actions/workflows/Mega-Linter/badge.svg?branch=master)](https://github.com/marketplace/actions/mega-linter)

![Mega-Linter](https://github.com/Fred-MabS/docker-build-with-actions/workflows/Mega-Linter/badge.svg)](https://github.com/marketplace/actions/mega-linter)

shield.io badge

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/fred-mabs/docker-build-with-actions/Mega-Linter?label=lint)

## purge workflow runs

First `gh auth login`

`gh api repos/fred-mabs/docker-build-with-actions/actions/runs | jq -r '.workflow_runs[] | "\(.id)"' | xargs -n1 -I % gh api repos/fred-mabs/docker-build-with-actions/actions/runs/% -X DELETE`
