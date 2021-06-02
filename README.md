# docker-build-with-actions

## badges

![QA](https://github.com/Fred-MabS/docker-build-with-actions/actions/workflows/qa.yml/badge.svg)

![Build](https://github.com/Fred-MabS/docker-build-with-actions/actions/workflows/docker-image.yml/badge.svg)

[![Known Vulnerabilities](https://snyk.io/test/github/Fred-MabS/docker-build-with-actions/badge.svg)](https://snyk.io/test/github/Fred-MabS/docker-build-with-actions)


[![GitHub Super-Linter](https://github.com/Fred-MabS/docker-build-with-actions/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)



## purge workflow runs

First `gh auth login`

`gh api repos/fred-mabs/docker-build-with-actions/actions/runs | jq -r '.workflow_runs[] | "\(.id)"' | xargs -n1 -I % gh api repos/fred-mabs/docker-build-with-actions/actions/runs/% -X DELETE`