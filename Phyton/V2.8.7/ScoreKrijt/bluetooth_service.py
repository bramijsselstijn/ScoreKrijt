# -*- coding: utf-8 -*-
"""
Bluetooth Classic SPP service voor ScoreKrijt.

Leest JSON-regels vanaf /dev/rfcomm0 en geeft geldige berichten
door aan een callback.
"""

import sys
import threading
import time

try:
    import serial
except ImportError:
    serial = None

from .bluetooth_protocol import BluetoothProtocol, ProtocolError


class BluetoothService:
    def __init__(
        self,
        message_callback,
        port="/dev/rfcomm0",
        baudrate=9600,
        timeout=1,
        auto_reconnect=True,
    ):
        self.message_callback = message_callback
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.auto_reconnect = auto_reconnect

        self.serial_connection = None
        self.running = False
        self.thread = None
        self.write_lock = threading.Lock()
        self._last_error = None

    def _log(self, text):
        # Komt in scorekrijt-autostart.log terecht (de launcher stuurt stderr daarheen).
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{stamp} [bluetooth] {text}", file=sys.stderr, flush=True)

    def _log_error(self, error):
        # Alleen loggen als de melding verandert, anders komt er elke 2 seconden
        # een regel bij zolang er geen telefoon verbonden is.
        text = f"{type(error).__name__}: {error}"
        if text != self._last_error:
            self._last_error = text
            self._log(f"poort gesloten of niet beschikbaar: {text}")

    def start(self):
        if serial is None:
            raise RuntimeError(
                "pyserial is niet geïnstalleerd. Installeer met: pip install pyserial"
            )

        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )
        self.thread.start()

    def stop(self):
        self.running = False

        if self.serial_connection:
            try:
                self.serial_connection.close()
            except Exception:
                pass

        self.serial_connection = None

    def send(self, data: dict):
        if not self.serial_connection:
            return False

        try:
            with self.write_lock:
                self.serial_connection.write(
                    BluetoothProtocol.encode(data)
                )
            return True
        except Exception:
            return False

    def _connect(self):
        self.serial_connection = serial.Serial(
            self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

    def _run(self):
        while self.running:
            try:
                if self.serial_connection is None:
                    self._connect()
                    self._last_error = None
                    self._log(f"{self.port} geopend")
                    self.send(BluetoothProtocol.ok("bluetooth_connected"))

                line = self.serial_connection.readline()

                if not line:
                    continue

                try:
                    msg = BluetoothProtocol.decode(line)
                except ProtocolError as e:
                    self.send(BluetoothProtocol.error(str(e)))
                    continue

                try:
                    self.message_callback(msg)
                    self.send(BluetoothProtocol.ok("command_received"))
                except Exception as e:
                    self.send(BluetoothProtocol.error(f"Fout bij verwerken: {e}"))

            except Exception as error:
                self._log_error(error)
                if self.serial_connection:
                    try:
                        self.serial_connection.close()
                    except Exception:
                        pass

                self.serial_connection = None

                if not self.auto_reconnect:
                    self.running = False
                    break

                time.sleep(2)
