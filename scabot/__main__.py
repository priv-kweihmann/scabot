# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import logging

from scabot.runargs import create_parser
from scabot.runargs import create_provider_instance
from scabot.runargs import create_request_instance


def main():
    _args = create_parser().parse_args()
    _prodiver = create_provider_instance(_args)
    logging.info(_prodiver)  # pragma: no cover
    _request = create_request_instance(_args, _prodiver)  # pragma: no cover
    logging.info(f'New Notes -> {_request.NewNotes}') # noqa: G004 # pragma: no cover
    _request.Process()  # pragma: no cover


if __name__ == '__main__':
    main()  # pragma: no cover
