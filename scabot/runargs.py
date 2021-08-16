# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import os

from scabot.provider import Provider
from scabot.provider.github import GitHubProvider
from scabot.provider.gitlab import GitLabProvider
from scabot.provider.mock import MockProvider
from scabot.request import Request


def __create_github_parser(subparser):
    _parser = subparser.add_parser('github')
    _parser.add_argument(
        '--project', default=os.environ.get('SCABOT_PROJECT', ''), help='Project name')
    _parser.add_argument(
        '--request', default=os.environ.get('SCABOT_REQUEST', ''), help='Request Number')
    _parser.add_argument(
        '--server', default=os.environ.get('SCABOT_SERVER', ''), help='https://github.com/<profile-name>')
    _parser.add_argument('files', nargs='+',
                         help='Files containing SCA results')


def __create_gitlab_parser(subparser):
    _parser = subparser.add_parser('gitlab')
    _parser.add_argument(
        '--project', default=os.environ.get('SCABOT_PROJECT', ''), help='Project number')
    _parser.add_argument(
        '--request', default=os.environ.get('SCABOT_REQUEST', ''), help='Request Number')
    _parser.add_argument(
        '--server', default=os.environ.get('SCABOT_SERVER', ''), help='Url to your gitlab server')
    _parser.add_argument('files', nargs='+',
                         help='Files containing SCA results')


def __create_mock_parser(subparser):
    _parser = subparser.add_parser('mock')
    _parser.add_argument(
        '--project', default=os.environ.get('SCABOT_PROJECT', ''), help='Project number')
    _parser.add_argument(
        '--request', default=os.environ.get('SCABOT_REQUEST', ''), help='Request Number')
    _parser.add_argument(
        '--server', default=os.environ.get('SCABOT_SERVER', ''), help='Path to mock server files')
    _parser.add_argument('files', nargs='+',
                         help='Files containing SCA results')


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='scabot', description='gitlab/hub auto commenter')
    parser.add_argument(
        '--botuser', default=os.environ.get('SCABOT_BOTUSER', ''), help='Username of the bot')
    parser.add_argument('--bottoken', default=os.environ.get(
        'SCABOT_BOTTOKEN', ''), help='Access token of the bot')
    parser.add_argument('--comment_only_affected_lines',
                        default='SCABOT_COMMENT_AFFECTED_LINES' in os.environ,
                        action='store_true',
                        help='Comment only on changed lines')
    parser.add_argument('--comment_drafts',
                        default=any(os.environ.get('SCABOT_COMMENT_DRAFT_REQUEST', '')),
                        action='store_true',
                        help='Comment on draft/WIP requests')
    parser.add_argument('--comment_indirect',
                        default=any(os.environ.get('SCABOT_COMMENT_INDIRECT', '')),
                        action='store_true',
                        help='Comment if any of the incoorporated BBFILES was changed')
    parser.add_argument('--incomplete',
                        default=False,
                        action='store_true',
                        help='Build was incomplete - no issues will be resolved, just new added')

    subparser = parser.add_subparsers(dest='mode')
    __create_github_parser(subparser)
    __create_gitlab_parser(subparser)
    __create_mock_parser(subparser)

    return parser


def create_provider_instance(args) -> Provider:
    if args.mode == 'mock': # pragma: no cover
        return MockProvider(args, args.botuser, args.bottoken,
                            args.server, args.project, args.request)  # pragma: no cover
    elif args.mode == 'github': # pragma: no cover
        return GitHubProvider(args, args.botuser, args.bottoken,
                              args.server, args.project, args.request) # pragma: no cover
    elif args.mode == 'gitlab': # pragma: no cover
        return GitLabProvider(args, args.botuser, args.bottoken,
                              args.server, args.project, args.request) # pragma: no cover
    raise NotImplementedError(
        'Unknown provider -> {prov}'.format(prov=args.mode))


def create_request_instance(args, provider) -> Request:
    return Request(args, provider) # pragma: no cover
