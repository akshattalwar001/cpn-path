import re
import uuid

from pathlib import Path

from telethon.tl import patched  # type: ignore


def parse_entity(entity: str) -> int | str:
    return int(entity) if entity.lstrip("-").isdigit() else entity


def get_unique_filename(message: patched.Message) -> str:

    unique_prefix = str(uuid.uuid4())

    original_filename = None
    original_suffix = ""

    if message.file and isinstance(message.file.name, str):
        original_filename = Path(message.file.name).stem
        original_suffix = Path(message.file.name).suffix

    if original_filename:
        filename = f"{original_filename}_{unique_prefix}{original_suffix}"
    else:
        # Fallback if no original name (use message_id and media type if possible)
        fallback_name = f"download_{message.id}_{unique_prefix}"
        if message.file and isinstance(message.file.mime_type, str):
            # Try to get extension from mime type (basic implementation)
            parts = message.file.mime_type.split("/")
            if len(parts) == 2 and parts[1]:
                filename = f"{fallback_name}.{parts[1]}"
            else:
                filename = fallback_name
        else:
            filename = fallback_name

    return filename


def parse_telegram_url(url: str) -> tuple[str | int, int] | None:
    """https://t.me/somechannel/123 to (entity, message_id)
    """
    pattern = r"^(?:https?://)?t(?:elegram)?\.me/(?:(?P<username>[A-Za-z0-9_]+)/(?P<message_id>\d+)|c/(?P<chat_id>\d+)/(?P<chat_message_id>\d+))/?$"

    match = re.match(pattern, url)

    if match:
        captured = match.groupdict()
        entity = captured.get("username") or captured.get("chat_id")
        message_id = captured.get("message_id") or captured.get("chat_message_id")

        if entity and message_id:
            return parse_entity(entity), int(message_id)

    return None
