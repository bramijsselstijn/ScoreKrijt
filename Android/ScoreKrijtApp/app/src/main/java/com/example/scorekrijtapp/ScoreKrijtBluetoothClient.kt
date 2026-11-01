package com.example.scorekrijtapp

import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.util.UUID
import java.util.concurrent.atomic.AtomicBoolean

class ScoreKrijtBluetoothClient(
    private val bluetoothAdapter: BluetoothAdapter?,
    private val onStatusChanged: (String) -> Unit,
    private val onMessageReceived: (JSONObject) -> Unit,
    private val onDebugLog: (String) -> Unit
) {
    companion object {
        private val SPP_UUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
        const val PROTOCOL_VERSION = 2
    }

    private var socket: BluetoothSocket? = null
    private var readerThread: Thread? = null
    private val connected = AtomicBoolean(false)
    private val writeLock = Any()

    fun isConnected(): Boolean = connected.get()

    @SuppressLint("MissingPermission")
    fun connect(device: BluetoothDevice) {
        disconnect()
        onStatusChanged("Verbinden met ${device.name ?: device.address}...")

        Thread {
            val targetName = device.name ?: device.address
            try {
                try {
                    bluetoothAdapter?.cancelDiscovery()
                } catch (_: SecurityException) {
                    // Connecting can continue even when Android blocks discovery cancellation.
                }
                val newSocket = connectWithFallback(device)
                socket = newSocket
                connected.set(true)
                onDebugLog("INFO socket verbonden met $targetName")
                onStatusChanged("Verbonden met $targetName")
                startReader(newSocket)
                sendHello()
            } catch (e: Exception) {
                connected.set(false)
                closeSocketQuietly()
                onStatusChanged("Bluetooth fout met $targetName: ${e.message ?: "kan niet verbinden"}")
            }
        }.start()
    }

    fun send(message: JSONObject): Boolean {
        val activeSocket = socket ?: return false
        if (!connected.get()) return false

        return try {
            synchronized(writeLock) {
                activeSocket.outputStream.write((message.toString() + "\n").toByteArray(Charsets.UTF_8))
                activeSocket.outputStream.flush()
                onDebugLog("TX ${message}")
            }
            true
        } catch (e: Exception) {
            if (socket === activeSocket) {
                connected.set(false)
                onStatusChanged("Bluetooth verzenden mislukt: ${e.message ?: "verbinding kwijt"}")
            }
            false
        }
    }

    fun disconnect() {
        connected.set(false)
        closeSocketQuietly()
        readerThread = null
    }

    @SuppressLint("MissingPermission")
    private fun connectWithFallback(device: BluetoothDevice): BluetoothSocket {
        val secureError = try {
            val secureSocket = device.createRfcommSocketToServiceRecord(SPP_UUID)
            secureSocket.connect()
            return secureSocket
        } catch (e: Exception) {
            e
        }

        try {
            val insecureSocket = device.createInsecureRfcommSocketToServiceRecord(SPP_UUID)
            insecureSocket.connect()
            return insecureSocket
        } catch (_: Exception) {
            // Try the common BlueZ SPP channel directly below.
        }

        val channelSocket = device.javaClass
            .getMethod("createRfcommSocket", Int::class.javaPrimitiveType)
            .invoke(device, 1) as BluetoothSocket
        try {
            channelSocket.connect()
            return channelSocket
        } catch (e: Exception) {
            throw Exception("SPP kanaal niet bereikbaar (${e.message ?: secureError.message ?: "geen detail"})")
        }
    }

    private fun startReader(activeSocket: BluetoothSocket) {
        readerThread = Thread {
            var helloRetriedAfterBoxReady = false
            try {
                val reader = BufferedReader(InputStreamReader(activeSocket.inputStream, Charsets.UTF_8))
                while (connected.get() && socket === activeSocket) {
                    val line = reader.readLine() ?: break
                    if (line.isBlank()) continue
                    onDebugLog("RX $line")
                    // Als rfcomm net wordt geopend kan Linux de eerste hello echoën
                    // en samenvoegen met bluetooth_connected. Die regel is dan geen
                    // geldige JSON, maar het gereed-signaal is wel betrouwbaar te zien.
                    if (!helloRetriedAfterBoxReady && line.contains("bluetooth_connected")) {
                        helloRetriedAfterBoxReady = true
                        sendHello()
                    }
                    try {
                        onMessageReceived(JSONObject(line))
                    } catch (_: Exception) {
                        onStatusChanged("Bluetooth bericht niet leesbaar")
                    }
                }
            } catch (_: Exception) {
                markDisconnectedIfCurrent(activeSocket)
            } finally {
                markDisconnectedIfCurrent(activeSocket)
                closeSocketQuietly(activeSocket)
            }
        }.also { it.start() }
    }

    private fun markDisconnectedIfCurrent(activeSocket: BluetoothSocket) {
        synchronized(writeLock) {
            if (socket !== activeSocket) return
            socket = null
            if (connected.getAndSet(false)) onStatusChanged("Bluetooth verbinding verbroken")
        }
    }

    private fun sendHello() {
        send(JSONObject()
            .put("cmd", "hello")
            .put("app", "ScoreKrijt Android")
            .put("app_version", "2.8.8")
            .put("protocol_version", PROTOCOL_VERSION))
    }

    private fun closeSocketQuietly() {
        val activeSocket = socket
        socket = null
        closeSocketQuietly(activeSocket)
    }

    private fun closeSocketQuietly(activeSocket: BluetoothSocket?) {
        try { activeSocket?.close() } catch (_: Exception) { }
    }
}



