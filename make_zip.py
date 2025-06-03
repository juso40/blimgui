import zipfile
from argparse import ArgumentParser
from pathlib import Path

FILE_EXTENSION = ".zip"


def get_mod_dirs() -> list[Path]:
    mod_dirs = []
    for path in Path().iterdir():
        if not path.is_dir():
            continue
        if path.name.startswith(("__", ".")):
            continue
        mod_dirs.append(path)
    return mod_dirs


def create_mod_zip(mod_dir: Path) -> None:
    with zipfile.ZipFile(
        mod_dir.with_suffix(FILE_EXTENSION),
        "w",
        zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zf:
        for child in mod_dir.rglob("*"):
            if child.is_dir() or "__pycache__" in str(child.absolute()) or child.suffix == FILE_EXTENSION:
                continue
            zf.write(child, mod_dir.name / child.relative_to(mod_dir))


def main() -> None:
    for mod_dir in get_mod_dirs():
        create_mod_zip(mod_dir)


if __name__ == "__main__":
    argparser = ArgumentParser(description="Bundle mod folders into .zip files")
    argparser.add_argument("-d", "--directory", type=Path, default=None, help="Single mod folder to bundle")
    args = argparser.parse_args()
    if args.directory:
        if not args.directory.is_dir():
            raise ValueError(f"{args.directory} is not a valid directory")
        create_mod_zip(args.directory)
    else:
        print("Bundling all mod folders in the current directory...")
        main()
