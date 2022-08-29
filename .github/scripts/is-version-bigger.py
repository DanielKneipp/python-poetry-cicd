import sys

VERSION_CURRENT = sys.argv[1]
VERSION_REFERENCE = sys.argv[2]

vcurr_major, vcurr_minor, vcurr_patch = VERSION_CURRENT.split(".")
vref_major, vref_minor, vref_patch = VERSION_REFERENCE.split(".")

if vref_major > vcurr_major:
    print(
        f"Reference version {VERSION_REFERENCE} cannot be bigger than the current version {VERSION_CURRENT}",
        file=sys.stderr,
    )
    exit(1)

if vref_major < vcurr_major:
    exit(0)

if vref_minor > vcurr_minor:
    print(
        f"Reference version {VERSION_REFERENCE} cannot be bigger than the current version {VERSION_CURRENT}",
        file=sys.stderr,
    )
    exit(1)

if vref_minor < vcurr_minor:
    exit(0)

if vref_patch > vcurr_patch:
    print(
        f"Reference version {VERSION_REFERENCE} cannot be bigger than the current version {VERSION_CURRENT}",
        file=sys.stderr,
    )
    exit(1)
