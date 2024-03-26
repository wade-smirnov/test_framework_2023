co_auth_login = {
    "type": "object",
    "properties": {
        "success": {
            "nonEmptyString": {
                "type": "string",
                "minLength": 1,
                "not": {"enum": ["null"]},
            }
        },
        "token": {
            "nonEmptyString": {
                "type": "string",
                "minLength": 10,
                "not": {"enum": ["null"]},
            }
        },
    },
    "required": ["success", "token"],
}
