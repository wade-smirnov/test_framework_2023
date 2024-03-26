d_auth_login = {
    "type": "object",
    "properties": {
        "success": {
            "nonemptyString": {
                "type": "string",
                "minLength": 1,
                "not": {"enum": ["null"]},
            }
        },
        "token": {
            "nonemptyString": {
                "type": "string",
                "minLength": 10,
                "not": {"enum": ["null"]},
            }
        },
    },
    "required": ["success", "token"],
}
