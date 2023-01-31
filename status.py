import os
import sys
import traceback

from gi.repository import GLib

import dbus
import dbus.mainloop.glib

import requests

USER_TOKEN = os.environ.get("SLACK_USER_TOKEN")
if USER_TOKEN is None:
    print("SLACK_USER_TOKEN is required")
    exit(1)
ACTIVE_STATUS_TEXT = os.environ.get("ACTIVE_STATUS_TEXT", "")
ACTIVE_STATUS_EMOJI = os.environ.get("ACTIVE_STATUS_EMOJI", "")
INACTIVE_STATUS_TEXT = os.environ.get("INACTIVE_STATUS_TEXT", "")
INACTIVE_STATUS_EMOJI = os.environ.get("INACTIVE_STATUS_EMOJI", "")


def set_slack_status(text: str = None, emoji: str = None, expiration: int = 0) -> bool:
    res: requests.Response = requests.post(
        "https://slack.com/api/users.profile.set",
        headers={
            "Authorization": "Bearer " + USER_TOKEN,
        },
        json={
            "profile": {
                "status_text": text,
                "status_emoji": emoji,
                "status_expiration": expiration,
            }
        },
    )
    return res.status_code == 200


def handler(islocked: bool):
    if islocked:
        set_slack_status(INACTIVE_STATUS_TEXT, INACTIVE_STATUS_EMOJI)
        print(f"set status as inactive", flush=True)
    else:
        set_slack_status(ACTIVE_STATUS_TEXT, ACTIVE_STATUS_EMOJI)
        print(f"set status as active", flush=True)


if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object = bus.get_object("org.gnome.ScreenSaver", "/org/gnome/ScreenSaver")

        islocked = object.GetActive(dbus_interface="org.gnome.ScreenSaver")
        handler(islocked)

        object.connect_to_signal(
            "ActiveChanged",
            handler,
            dbus_interface="org.gnome.ScreenSaver",
        )
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    loop = GLib.MainLoop()
    loop.run()
