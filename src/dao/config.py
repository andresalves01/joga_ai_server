from configparser import ConfigParser


def config(filename="src/dao/database.ini", section="postgresql") -> dict:
    parser = ConfigParser()
    parser.read(filenames=filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file".format(section, filename)
        )
    return db
