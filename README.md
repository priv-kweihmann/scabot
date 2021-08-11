<!---
SPDX-FileCopyrightText: 2021 Konrad Weihmann
SPDX-License-Identifier: GPL-3.0-only
-->

# sca bot

this bot can automatically comment on

- gitlab merge requests
- github pull requests

using fidings from [meta-sca](https://github.com/priv-kweihmann/meta-sca)

## Usage

```shell
usage: scabot [-h] [--botuser BOTUSER] [--bottoken BOTTOKEN] [--comment_only_affected_lines] [--comment_drafts] [--comment_indirect] {github,gitlab,mock} ...

gitlab/hub auto commenter

positional arguments:
  {github,gitlab,mock}

optional arguments:
  -h, --help            show this help message and exit
  --botuser BOTUSER     Username of the bot (default: )
  --bottoken BOTTOKEN   Access token of the bot (default: )
  --comment_only_affected_lines
                        Comment only on changed lines (default: False)
  --comment_drafts      Comment on draft/WIP requests (default: False)
  --comment_indirect    Comment if any of the incoorporated BBFILES was changed (default: False)
```

options for gitlab

```shell
usage: scabot gitlab [-h] [--project PROJECT] [--request REQUEST] [--server SERVER] files [files ...]

positional arguments:
  files              Files containing SCA results

optional arguments:
  -h, --help         show this help message and exit
  --project PROJECT  Project number
  --request REQUEST  Request Number
  --server SERVER    Path to mock server files
```

options for github

```shell
usage: scabot github [-h] [--project PROJECT] [--request REQUEST] [--server SERVER] files [files ...]

positional arguments:
  files              Files containing SCA results

optional arguments:
  -h, --help         show this help message and exit
  --project PROJECT  Project name
  --request REQUEST  Request Number
  --server SERVER    https://github.com/<profile-name>
```

### Use of environment variables

several options can be defined via environment variable, which is the preferred way to specify confidental information (like the access token)

| option                        | environment var               | comments                                 |
| ----------------------------- | ----------------------------- | ---------------------------------------- |
| --bottoken                    | SCABOT_BOTTOKEN               |                                          |
| --botuser                     | SCABOT_BOTUSER                |                                          |
| --comment_drafts              | SCABOT_COMMENT_DRAFT_REQUEST  | value of the env variable doesn't matter |
| --comment_indirect            | SCABOT_COMMENT_INDIRECT       | value of the env variable doesn't matter |
| --comment_only_affected_lines | SCABOT_COMMENT_AFFECTED_LINES | value of the env variable doesn't matter |
| --project                     | SCABOT_PROJECT                |                                          |
| --request                     | SCABOT_REQUEST                |                                          |
| --server                      | SCABOT_SERVER                 |                                          |

## License

This application is licensed under `GPL-3.0-only`
