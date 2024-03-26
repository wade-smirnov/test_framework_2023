from framework.clients.co_client import Client


class SignatureVerificator:
    @staticmethod
    def check_detached_signature_property_setup(file_id: str, sig_file_id: str):
        file_data = Client.get_file_by_id(file_id).json().get("file")

        assert file_data.get("signatureInfo").get(
            "hasDetached"
        ), "Detached signature property was not setup"

        received_sig_id = file_data.get("signatureInfo").get("detached").get("id")
        assert received_sig_id == sig_file_id, (
            f"Received Id of signature {received_sig_id},"
            f" is not matching expected one {sig_file_id}"
        )

        sig_file_data = Client.get_file_by_id(sig_file_id).json().get("file")
        received_file_id = (
            sig_file_data.get("signatureInfo").get("signedFile").get("id")
        )
        assert received_file_id == file_id, (
            f"Received Id of signature {received_file_id},"
            f" is not matching expected one {file_id}"
        )
        return file_data, sig_file_data

    @staticmethod
    def check_detached_signature_property_is_not_setup(file_id: str, sig_file_id: str):
        file_data = Client.get_file_by_id(file_id=file_id).json()
        assert not file_data.get("file").get(
            "signatureInfo"
        ), "Detached signature property exists, we expect otherwise"

        sig_file_data = Client.get_file_by_id(file_id=sig_file_id).json()
        assert not sig_file_data.get(
            "signatureInfo"
        ), "Signature info was not removed from sig file"

    @staticmethod
    def check_user_has_specific_role_for_file(file_id: str, id: str, role: str):
        permission_data = Client.get_user_file_permission(file_id=file_id)
        user_permission = None
        for data in permission_data:
            if data.get("permission").get("id") == id:
                user_permission = data.get("permission")
                break
        assert user_permission, f"<Reserve_user> is missing {role} permission for file"

        received_role = user_permission.get("role")
        assert (
            received_role == role
        ), f"Received role {received_role} is not matching expected one {role}"

        return user_permission

    @staticmethod
    def check_all_embedded_signature_endpoints(
        file_id: str, filename: str, dir_id: str
    ):
        response = Client.get_file_by_id(file_id)
        assert (
            response.json().get("file").get("signatureInfo").get("hasEmbedded") is True
        ), "File's embedded signature is missing"

        files = Client.get_files()
        for file in files:
            if file.get("id") == Client.created_file_id:
                assert (
                    file.get("id").get("signatureInfo").get("hasEmbedded") is True
                ), "File signature is missing in v1/files"

        search_files = Client.get_files_search(dir_id, filename)
        for file in search_files:
            if file.get("id") == Client.created_file_id:
                assert (
                    file.get("id").get("signatureInfo").get("hasEmbedded") is True
                ), "File signature is missing in v1/files/search"
