from configparser import ConfigParser, NoSectionError


def config(filename="src/dao/database.ini", section="postgresql") -> dict[str, str]:
    parser = ConfigParser()
    parser.read(filenames=filename)

    if not parser.has_section(section):
        raise NoSectionError(f"Section {section} is not found in the {filename} file")

    db = {key: value for key, value in parser.items(section)}

    return db
