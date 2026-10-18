package com.example.scorekrijtapp

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledFuture
import java.util.concurrent.TimeUnit

object ScoreKrijtBluetoothBox {
    private var client: ScoreKrijtBluetoothClient? = null
    private var statusListener: ((String) -> Unit)? = null
    private var messageListener: ((JSONObject) -> Unit)? = null
    private var lastStatus: String = "Niet verbonden"
    private var connectedStatus: String? = null
    private val debugLog = ArrayDeque<String>()
    private val reconnectExecutor = Executors.newSingleThreadScheduledExecutor()
    private var lastDevice: BluetoothDevice? = null
    private var reconnectFuture: ScheduledFuture<*>? = null
    private var reconnectAttempt = 0
    @Volatile private var manualDisconnect = true

    fun initialize(bluetoothAdapter: BluetoothAdapter?) {
        if (client != null) return

        client = ScoreKrijtBluetoothClient(
            bluetoothAdapter,
            onStatusChanged = { status ->
                if (status.startsWith("Verbonden met ")) {
                    synchronized(this) {
                        reconnectAttempt = 0
                        reconnectFuture?.cancel(false)
                        reconnectFuture = null
                    }
                    connectedStatus = status
                }
                lastStatus = status
                statusListener?.invoke(status)
                if (status.contains("verbinding verbroken", ignoreCase = true) ||
                    status.startsWith("Bluetooth fout") ||
                    status.startsWith("Bluetooth verzenden mislukt")) {
                    scheduleReconnect()
                }
            },
            onMessageReceived = { message ->
                messageListener?.invoke(message)
            },
            onDebugLog = { line -> appendDebugLog(line) }
        )
    }

    fun setListeners(
        onStatusChanged: ((String) -> Unit)? = null,
        onMessageReceived: ((JSONObject) -> Unit)? = null
    ) {
        statusListener = onStatusChanged
        messageListener = onMessageReceived
        onStatusChanged?.invoke(lastStatus)
    }

    fun clearListeners() {
        statusListener = null
        messageListener = null
    }

    fun connect(device: BluetoothDevice) {
        synchronized(this) {
            lastDevice = device
            manualDisconnect = false
            reconnectAttempt = 0
            reconnectFuture?.cancel(false)
            reconnectFuture = null
        }
        client?.connect(device)
    }

    @Synchronized
    private fun scheduleReconnect() {
        val device = lastDevice ?: return
        if (manualDisconnect || reconnectFuture?.isDone == false || client?.isConnected() == true) return
        if (reconnectAttempt >= 3) {
            lastStatus = "Automatisch opnieuw verbinden mislukt"
            appendDebugLog("INFO automatisch opnieuw verbinden gestopt na 3 pogingen")
            statusListener?.invoke(lastStatus)
            return
        }
        val delays = longArrayOf(1, 2, 5)
        val delay = delays[reconnectAttempt]
        reconnectAttempt++
        appendDebugLog("INFO herverbindingspoging $reconnectAttempt over ${delay}s")
        reconnectFuture = reconnectExecutor.schedule({
            synchronized(this) { reconnectFuture = null }
            if (manualDisconnect || client?.isConnected() == true) return@schedule
            lastStatus = "Automatisch opnieuw verbinden ($reconnectAttempt/3)…"
            statusListener?.invoke(lastStatus)
            client?.connect(device)
        }, delay, TimeUnit.SECONDS)
    }

    fun reconnect(): Boolean {
        val device = synchronized(this) {
            val remembered = lastDevice ?: return false
            manualDisconnect = false
            reconnectAttempt = 0
            reconnectFuture?.cancel(false)
            reconnectFuture = null
            remembered
        }
        client?.connect(device)
        return true
    }

    fun canReconnect(): Boolean = lastDevice != null

    fun send(message: JSONObject): Boolean {
        return client?.send(message) == true
    }

    @Synchronized
    private fun appendDebugLog(line: String) {
        val time = SimpleDateFormat("HH:mm:ss.SSS", Locale.getDefault()).format(Date())
        debugLog.addLast("$time  $line")
        while (debugLog.size > 200) debugLog.removeFirst()
    }

    @Synchronized
    fun debugLogText(): String = if (debugLog.isEmpty()) {
        "Nog geen Bluetooth-communicatie geregistreerd."
    } else {
        debugLog.joinToString("\n")
    }

    @Synchronized
    fun clearDebugLog() {
        debugLog.clear()
    }

    fun isConnected(): Boolean {
        return client?.isConnected() == true
    }

    fun lastStatus(): String {
        return lastStatus
    }

    fun connectedStatus(): String {
        return connectedStatus ?: "Verbonden"
    }

    fun disconnect() {
        synchronized(this) {
            manualDisconnect = true
            reconnectAttempt = 0
            reconnectFuture?.cancel(false)
            reconnectFuture = null
        }
        client?.disconnect()
        lastStatus = "Niet verbonden"
        connectedStatus = null
        statusListener?.invoke(lastStatus)
    }
}

