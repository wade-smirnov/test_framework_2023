import random


class SignatureHelper:
    signature_file_extensions = [".xods", ".xodt", ".xlsx", ".docx", ".ods", ".odt"]
    extension_convertions = {
        "xods": "xods",
        "xodt": "xodt",
        "xlsx": "xods",
        "docx": "xodt",
        "ods": "xods",
        "odt": "xodt",
    }

    @staticmethod
    def get_random_signature_file_extension() -> str:
        return random.choice(SignatureHelper.signature_file_extensions)

    @staticmethod
    def get_filename_after_import(filename: str) -> str:
        name = filename.split(".")[0]
        extension = filename.split(".")[1]
        if extension in ["xodt", "xods"]:
            return name + " (2)" + "." + extension
        else:
            extension = SignatureHelper.extension_convertions.get(extension)
            return name + "." + extension
