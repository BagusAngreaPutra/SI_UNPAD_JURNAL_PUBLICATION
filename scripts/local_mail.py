"""Local SMTP inbox for OJS development. Saves messages; never relays email."""
from aiosmtpd.controller import Controller
from pathlib import Path
from threading import Event
from uuid import uuid4
from datetime import datetime, timezone

class Inbox:
    async def handle_DATA(self, server, session, envelope):
        directory = Path(__file__).resolve().parents[2] / 'UNPAD-runtime' / 'mail'
        directory.mkdir(parents=True, exist_ok=True)
        name = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-') + uuid4().hex + '.eml'
        (directory / name).write_bytes(envelope.original_content)
        return '250 Stored in local development inbox'

if __name__ == '__main__':
    controller = Controller(Inbox(), hostname='127.0.0.1', port=1025)
    controller.start()
    try:
        Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
