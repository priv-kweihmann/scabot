# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

# set CRYPTOGRAPHY_OPENSSL_NO_LEGACY to avoid errors
# with newer cryptography versions
import os
import logging

os.environ['CRYPTOGRAPHY_OPENSSL_NO_LEGACY'] = '1'

from scabot.runargs import create_parser  # noqa: E402
from scabot.runargs import create_provider_instance  # noqa: E402
from scabot.runargs import create_request_instance  # noqa: E402


def main():
    _args = create_parser().parse_args()
    _prodiver = create_provider_instance(_args)
    logging.info(_prodiver)  # pragma: no cover
    _request = create_request_instance(_args, _prodiver)  # pragma: no cover
    logging.info(f'New Notes -> {_request.NewNotes}')  # noqa: G004 # pragma: no cover
    _request.Process()  # pragma: no cover


if __name__ == '__main__':
    main()  # pragma: no cover
