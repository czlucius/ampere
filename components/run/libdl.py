#   A multi-purpose Discord Bot written with Python and pycord.
#   Copyright (C) 2022 czlucius (lcz5#3392)
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import urllib.request, json

from components.run.coderunner import PistonCodeRunner


class NoSuitablePackageException(Exception):
    pass


async def download_py_whl(lib_name: str):
    """
    Downloads a whl package, returning the raw contents of the file (in bytes perhaps)
    :param lib_name: Library name to find and download.
    :return: Contents of the whl file
    :raises: NoSuitablePackageFoundException: if there is no suitable package found
    """
    # TODO pip also accepts *.tar.gz files, so we can download the relevant distribution from PyPI-Simple for libs w/o wheel distributions.
    # We can use pypi simple to fetch, and check if the lib is compatible through filename.

    logging.info(f"download_py_whl: library name: {lib_name}")
    url = "https://www.wheelodex.org/json/projects/" + lib_name  # TODO please improve this!
    logging.info(f"download_py_whl: url name: {url}")

    with urllib.request.urlopen(url) as url_data:
        whl_data = json.load(url_data)
    if not whl_data:
        raise NoSuitablePackageException("Library not found/does not have a wheel distribution.")

    current_latest = (-99999, -99999, -99999)
    latest_info = []
    for version in whl_data.items():
        major, minor, patch = [int(x, 10) for x in version[0].split('.')]
        if (major > current_latest[0]) or\
                (major == current_latest[0] and minor > current_latest[1]) or\
                (major == current_latest[0] and minor == current_latest[1] and patch > current_latest[2]):
            current_latest = (major, minor, patch)
        latest_info = version[1]

    sample = PistonCodeRunner()
    arch = (await sample.run("bash", "uname -m")).output

    # Architecture can be x86_64, aarch64, etc.
    # We need to discard as many irrelevant packages, and cannot afford to query for every single one
    # Packages such as pycryptodome have many *.whl files, we should only look at the ones that interest us.
    # e.g. macOS, not x86_64
    # pp/jp/ip cannot (we only use cp, CPython or py3, independent) - look @ query step.

    # https://peps.python.org/pep-0425/#details
    processed = []
    for whl in latest_info:
        filename: str = whl["filename"].lower()
        # Operating system. We assume Windows, macOS, Linux, or platform-independent only. Other systems could cause a crash, but parsing is not very helpful.
        if "macos" in filename:
            continue
        elif "win" in filename: # may trigger if package name contains win: https://pypi.org/search/?q=win
            continue

        # We only include the specific architecture, or any.
        # for any, we may detect false positives if the package name is similar, but its ok.
        # we will filter these in the querying step.
        if arch in filename or "-any" in filename:
            processed.append(whl)
    if not processed:
        raise NoSuitablePackageException("Library exists, but no compatible version found.")

    to_run = []
    for whl in processed:
        href = "https://www.wheelodex.org/" + whl["href"]
        with urllib.request.urlopen(href) as url_data:
            href_data = json.load(url_data)
        try:
            rollout_info = href_data["data"]
            whl_archs = rollout_info["arch"]
            arch_compat = False
            if "any" in whl_archs:
                arch_compat = True
            for whl_arch in whl_archs:
                if arch in whl_arch:  # To cater to arch names such as manylinux2010_x86_64 which are not equal
                    arch_compat = True
                    break

            # The Piston compiler runs on Python 3.73 (please file an issue if this has changed)
            # So, if manylinux is used, only manylinux2010 and manylinux1 is compatible.
            # Drop packages with manylinux2014 or manylinux_x
            for whl_arch in whl_archs:
                if "manylinux" in whl_arch:
                    if "manylinux2014" in whl_arch or "manylinux_" in whl_arch:
                        # Discard even though arch is compatible.
                        arch_compat = False
                        # We cannot break in case there is a manylinux that is compatible afterwards.
                    else:
                        arch_compat = True
                        break
            if not arch_compat:
                continue

            # Check the pyver. (must either start with py3 or cp3). We are not going to run Python 2 packages.
            pyver: str = rollout_info["pyver"][0]
            if not (pyver.startswith("py3") or pyver.startswith("cp3")):
                # Discard.
                continue

            # TODO add parsing code for ABI.
        except KeyError:
            # Some libs, e.g. tensorflow do not have the data section.
            # We shall just skip this part then, and download the whl and hope it works.
            pass


        whl2 = whl.copy()
        whl2["hrefdata"] = href_data
        to_run.append(whl2)

    if not to_run:
        raise NoSuitablePackageException("Library exists, but no compatible version found.")

    # We just pick the 1st one since all the packages in to_run can be run.
    suitable_pkg = to_run[0]
    filename1 = suitable_pkg["filename"]
    whl_url_to_dl = suitable_pkg["hrefdata"]["pypi"]["url"]

    with urllib.request.urlopen(whl_url_to_dl) as pkg_raw:
        pkg_contents = pkg_raw.read()

    return [filename1, pkg_contents]
