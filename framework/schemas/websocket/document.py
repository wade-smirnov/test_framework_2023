websocket_document = {
    "type": "object",
    "properties": {
        "$1": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "kwargs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"key": {"type": "string"}, "value": {}},
                        "required": ["key", "value"],
                    },
                },
            },
            "required": ["name", "kwargs"],
        }
    },
    "required": ["$1"],
}
