import shutil
import subprocess
import sys
from pathlib import Path

THIS_FOLDER = Path(__file__).parent

IMGUI_FOLDER = THIS_FOLDER / ".tmp_imgui_bundle"
VENV32_FOLDER = THIS_FOLDER / ".tmp_venv32"
VENV64_FOLDER = THIS_FOLDER / ".tmp_venv32"
DIST32_FOLDER = THIS_FOLDER / "blimgui" / "dist32"
DIST64_FOLDER = THIS_FOLDER / "blimgui" / "dist64"


def clone_imgui_bundle() -> None:
    subprocess.run(
        [
            "git",
            "clone",
            "--depth=1",
            # This version is known to work, newer ones have caused crashes.
            "--branch=v1.6.2",
            "git@github.com:pthom/imgui_bundle.git",
            IMGUI_FOLDER,
        ],
        check=True,
    )

    # Nanobind 3 made some breaking changes, which this old imgui_bundle version won't compile with
    # Since it's part of the build system, we can't simply add 'nanobind<3.0' during a pip install
    # Instead, edit its pyproject to add the limit there
    pyproject = IMGUI_FOLDER / "pyproject.toml"
    pyproject.write_text(
        pyproject.read_text().replace(
            'requires = ["scikit-build-core>=0.9.1", "nanobind"]',
            'requires = ["scikit-build-core>=0.9.1", "nanobind<3.0"]',
        ),
    )


def install_dist(py_version: str, venv_folder: Path, output_folder: Path) -> None:
    subprocess.run(
        [
            "py",
            f"-{py_version}",
            "-m",
            "venv",
            venv_folder,
        ],
        check=True,
    )
    subprocess.run(
        [
            venv_folder / "Scripts" / "python.exe",
            "-m",
            "pip",
            "install",
            ".",
        ],
        cwd=IMGUI_FOLDER,
        check=True,
    )
    shutil.move(venv_folder / "Lib" / "site-packages", output_folder)

    for path in output_folder.glob("pip*"):
        shutil.rmtree(path)


if __name__ == "__main__":
    import argparse
    import platform

    if platform.system() != "Windows":
        sys.stderr.write(
            "ERROR: This script only works on Windows!\n"
            "\n"
            "It assumes access to the 'py' launcher, to access different versions, and relies on"
            " the windows venv layout.\n",
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Tool to download all required dependencies and populate the dist directories",
    )
    parser.add_argument(
        "--py-version",
        default="3.14",
        help="Which Python version to install the dependencies under. Defaults to %(default)s.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If a folder used by this script already exists, delete it.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--only-32", action="store_true", help="Only populate the dist32 folder.")
    group.add_argument("--only-64", action="store_true", help="Only populate the dist64 folder.")

    args = parser.parse_args()

    used_folders = [IMGUI_FOLDER, VENV32_FOLDER, VENV64_FOLDER]
    if not args.only_64:
        used_folders.append(DIST32_FOLDER)
    if not args.only_32:
        used_folders.append(DIST64_FOLDER)

    for folder in used_folders:
        if not folder.exists():
            continue
        if args.force:
            shutil.rmtree(folder)
        else:
            sys.stderr.write(f"ERROR: folder {folder} already exists! Stopping!\n")
            sys.exit(1)

    clone_imgui_bundle()
    if not args.only_64:
        install_dist(args.py_version + "-32", VENV32_FOLDER, DIST32_FOLDER)
    if not args.only_32:
        install_dist(args.py_version, VENV64_FOLDER, DIST64_FOLDER)

    sys.stdout.write("\n\nDone!\nCleaning up temporary folders...\n")

    # I've gotten errors trying to delete these before, so do them last
    for folder in (IMGUI_FOLDER, VENV32_FOLDER, VENV64_FOLDER):
        shutil.rmtree(folder)
