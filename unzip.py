import zipfile
file = zipfile.ZipFile("archive.zip", "w", zipfile.ZIP_DEFLATED)
file.write("мой.py")
file.close()

# unzip file.
with zipfile.ZipFile("archive.zip", "r") as zfile:
    for filename in zfile.namelist():
        with open(filename, "w+b") as file:
            file.write(zfile.read(filename))


def ann(name: str) -> str:
    pass

ann(1)


