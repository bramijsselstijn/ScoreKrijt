# -*- coding: utf-8 -*-
"""
Bluetooth protocol voor ScoreKrijt.
JSON-per-regel protocol.
"""

import json


class ProtocolError(Exception):
    pass


class BluetoothProtocol:
    PROTOCOL_VERSION = 2
    VALID_COMMANDS = {
        "hello",
        "ping",
        "status",
        "start_new_match",
        "update_match",
        "score_plus",
        "score_minus",
        "next_turn",
        "undo",
        "match_finished",
        "get_display_settings",
        "preview_display_settings",
        "save_display_settings",
        "reset_display_settings",
    }

    @staticmethod
    def encode(data: dict) -> bytes:
        if not isinstance(data, dict):
            raise ProtocolError("Bericht moet een dict zijn")

        return (json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8")

    @staticmethod
    def decode(line: bytes | str) -> dict:
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="replace")

        line = line.strip()

        if not line:
            raise ProtocolError("Leeg bericht")

        try:
            msg = json.loads(line)
        except json.JSONDecodeError as e:
            raise ProtocolError(f"Ongeldige JSON: {e}")

        if not isinstance(msg, dict):
            raise ProtocolError("JSON moet een object zijn")

        cmd = msg.get("cmd")

        if not cmd:
            raise ProtocolError("Bericht mist 'cmd'")

        if cmd not in BluetoothProtocol.VALID_COMMANDS:
            raise ProtocolError(f"Onbekend commando: {cmd}")

        return msg

    @staticmethod
    def ok(message="ok") -> dict:
        return {
            "status": "ok",
            "message": message
        }

    @staticmethod
    def error(message: str) -> dict:
        return {
            "status": "error",
            "message": message
        }

