package com.example.scorekrijtapp

import android.Manifest
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import org.json.JSONArray
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    private lateinit var btnSkBoxConnect: Button
    private lateinit var btnSkBoxSettings: Button
    private lateinit var btnSkBoxReconnect: Button
    private lateinit var tvSkBoxStatus: TextView
    private var skBoxResumePromptShown = false
    private var protocolWarningShown = false
    private var protocolHandshakePending = false

    private val bluetoothPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions.values.all { it }) {
            showBluetoothDeviceDialog()
        } else {
            Toast.makeText(this, "Bluetooth toestemming is nodig", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        btnSkBoxConnect = findViewById(R.id.btnSkBoxConnect)
        btnSkBoxSettings = findViewById(R.id.btnSkBoxSettings)
        btnSkBoxReconnect = findViewById(R.id.btnSkBoxReconnect)
        tvSkBoxStatus = findViewById(R.id.tvSkBoxStatus)
        btnSkBoxConnect.setOnClickListener { requestBluetoothDeviceSelection() }
        btnSkBoxSettings.setOnClickListener {
            startActivity(Intent(this, SkBoxSettingsActivity::class.java))
        }
        btnSkBoxReconnect.setOnClickListener {
            if (!ScoreKrijtBluetoothBox.reconnect()) {
                Toast.makeText(this, "Geen eerder gebruikte SK-Box bekend", Toast.LENGTH_SHORT).show()
            }
        }
        initializeSkBoxBluetooth()
    }

    override fun onResume() {
        super.onResume()
        attachSkBoxListeners()
        checkResumeButton()
        updateSkBoxButton()
    }

    override fun onPause() {
        super.onPause()
        ScoreKrijtBluetoothBox.clearListeners()
    }

    private fun initializeSkBoxBluetooth() {
        val adapter = getSystemService(BluetoothManager::class.java)?.adapter
        ScoreKrijtBluetoothBox.initialize(adapter)
    }

    private fun attachSkBoxListeners() {
        ScoreKrijtBluetoothBox.setListeners(
            onStatusChanged = { status ->
                runOnUiThread {
                    updateSkBoxButton()
                    if (status.startsWith("Verbonden met ")) protocolHandshakePending = true
                    if (status.contains("fout", ignoreCase = true) || status.contains("verbroken", ignoreCase = true)) {
                        Toast.makeText(this, status, Toast.LENGTH_SHORT).show()
                    }
                }
            },
            onMessageReceived = { message -> runOnUiThread { handleSkBoxMessage(message) } }
        )
    }

    private fun handleSkBoxMessage(message: JSONObject) {
        if (message.optString("event") == "protocol_incompatible") {
            protocolHandshakePending = false
            showProtocolWarning(
                message.optInt("phone_protocol_version", ScoreKrijtBluetoothClient.PROTOCOL_VERSION),
                message.optInt("box_protocol_version", 0),
                message.optString("update_component")
            )
            return
        }
        if (protocolHandshakePending && message.optString("event") == "game_state") {
            protocolHandshakePending = false
            showProtocolWarning(ScoreKrijtBluetoothClient.PROTOCOL_VERSION, 1, "sk_box")
            return
        }
        if (message.optString("event") != "connection_match_status" || skBoxResumePromptShown) return
        protocolHandshakePending = false
        val boxProtocol = message.optInt("protocol_version", 0)
        if (boxProtocol != ScoreKrijtBluetoothClient.PROTOCOL_VERSION) {
            showProtocolWarning(
                ScoreKrijtBluetoothClient.PROTOCOL_VERSION,
                boxProtocol,
                if (boxProtocol < ScoreKrijtBluetoothClient.PROTOCOL_VERSION) "sk_box" else "phone_app"
            )
            return
        }
        val game = message.optJSONObject("game") ?: return
        val turn = game.optInt("turn", 0)
        if (turn == 0) return

        skBoxResumePromptShown = true
        val player1 = game.optString("player1", getString(R.string.player1_default))
        val player2 = game.optString("player2", getString(R.string.player2_default))
        AlertDialog.Builder(this)
            .setTitle("Wedstrijd bezig op SK-Box")
            .setMessage("Op de SK-Box loopt $player1 tegen $player2 (beurt $turn). Wilt u deze wedstrijd hervatten op de telefoon?")
            .setNegativeButton("Nee", null)
            .setPositiveButton("Hervatten") { _, _ -> importSkBoxMatch(game) }
            .show()
    }

    private fun showProtocolWarning(phoneVersion: Int, boxVersion: Int, updateComponent: String) {
        if (protocolWarningShown) return
        protocolWarningShown = true
        val action = when (updateComponent) {
            "phone_app" -> "Werk de telefoonapp bij."
            "sk_box" -> "Werk de software op de SK-Box bij."
            else -> "Werk de telefoonapp en SK-Box bij naar bij elkaar passende versies."
        }
        AlertDialog.Builder(this)
            .setTitle("SK-Box-versie niet compatibel")
            .setMessage("De communicatieversies komen niet overeen.\n\nTelefoon: $phoneVersion\nSK-Box: ${if (boxVersion == 0) "onbekend" else boxVersion}\n\n$action")
            .setPositiveButton("Sluiten", null)
            .show()
    }

    private fun importSkBoxMatch(game: JSONObject) {
        val history = JSONArray()
        val sourceHistory = game.optJSONArray("turn_history") ?: JSONArray()
        for (index in 0 until sourceHistory.length()) {
            val source = sourceHistory.optJSONObject(index) ?: continue
            history.put(JSONObject()
                .put("turn", source.optInt("turn", index + 1))
                .put("p1Score", if (source.isNull("p1_score")) JSONObject.NULL else source.optInt("p1_score"))
                .put("p1Total", if (source.isNull("p1_total")) JSONObject.NULL else source.optInt("p1_total"))
                .put("p2Score", if (source.isNull("p2_score")) JSONObject.NULL else source.optInt("p2_score"))
                .put("p2Total", if (source.isNull("p2_total")) JSONObject.NULL else source.optInt("p2_total")))
        }

        val totalPlayTimeSeconds = game.optLong("player1_play_time", 0) + game.optLong("player2_play_time", 0)
        getSharedPreferences("ScoreKrijtState", MODE_PRIVATE).edit()
            .putBoolean("GAME_IN_PROGRESS", true)
            .putBoolean("GAME_FINISHED", false)
            .putString("P1_NAME", game.optString("player1", getString(R.string.player1_default)))
            .putString("P2_NAME", game.optString("player2", getString(R.string.player2_default)))
            .putFloat("P1_TMC", game.optDouble("player1_tmc", 20.0).toFloat())
            .putFloat("P2_TMC", game.optDouble("player2_tmc", 15.0).toFloat())
            .putBoolean("FIXED_TURNS", game.optString("game_type") == "Vaste beurten")
            .putInt("MAX_TURNS", game.optInt("game_turns", 30))
            .putBoolean("COLOR_YELLOW", game.optString("start_color") == "Geel")
            .putBoolean("DRAW_ALLOWED", false)
            .putInt("P1_TOTAL", game.optInt("player1_car", 0))
            .putInt("P2_TOTAL", game.optInt("player2_car", 0))
            .putInt("CURRENT_TURN_CAR", game.optInt("current_car", 0))
            .putInt("TURN_NUMBER", game.optInt("turn", 1))
            .putBoolean("IS_P1_TURN", game.optInt("active_player", 1) == 1)
            .putInt("P1_HIGH", game.optInt("player1_highest_serie", 0))
            .putInt("P2_HIGH", game.optInt("player2_highest_serie", 0))
            .putLong("P1_TIME", game.optLong("player1_play_time", 0))
            .putLong("P2_TIME", game.optLong("player2_play_time", 0))
            .putLong("MATCH_START", System.currentTimeMillis() - totalPlayTimeSeconds * 1000)
            .putString("TURN_HISTORY", history.toString())
            .apply()

        startActivity(Intent(this, BiljardGame::class.java).putExtra("RESUME_GAME", true))
    }

    private fun updateSkBoxButton() {
        val connected = ScoreKrijtBluetoothBox.isConnected()
        val status = ScoreKrijtBluetoothBox.lastStatus()

        tvSkBoxStatus.text = when {
            connected -> ScoreKrijtBluetoothBox.connectedStatus()
            status.startsWith("Verbinden") -> status
            status.startsWith("Automatisch opnieuw verbinden") -> status
            else -> getString(R.string.sk_box_not_connected)
        }
        btnSkBoxConnect.text = if (connected) {
            getString(R.string.sk_box_change_connection)
        } else {
            getString(R.string.sk_box_connect)
        }
        btnSkBoxSettings.visibility = if (connected) View.VISIBLE else View.GONE
        btnSkBoxSettings.isEnabled = connected
        btnSkBoxReconnect.visibility = if (!connected &&
            status.startsWith("Automatisch opnieuw verbinden mislukt") &&
            ScoreKrijtBluetoothBox.canReconnect()) View.VISIBLE else View.GONE
    }

    private fun requestBluetoothDeviceSelection() {
        val missingPermissions = requiredBluetoothPermissions().filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }

        if (missingPermissions.isNotEmpty()) {
            bluetoothPermissionLauncher.launch(missingPermissions.toTypedArray())
        } else {
            showBluetoothDeviceDialog()
        }
    }

    private fun requiredBluetoothPermissions(): Array<String> {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(Manifest.permission.BLUETOOTH_CONNECT, Manifest.permission.BLUETOOTH_SCAN)
        } else {
            emptyArray()
        }
    }

    @Suppress("MissingPermission")
    private fun showBluetoothDeviceDialog() {
        val adapter = getSystemService(BluetoothManager::class.java)?.adapter
        if (adapter == null) {
            Toast.makeText(this, "Bluetooth wordt niet ondersteund", Toast.LENGTH_LONG).show()
            return
        }
        if (!adapter.isEnabled) {
            Toast.makeText(this, "Zet Bluetooth eerst aan", Toast.LENGTH_LONG).show()
            return
        }

        val devices = adapter.bondedDevices.sortedWith(compareBy<BluetoothDevice> { it.name ?: "" }.thenBy { it.address })
        if (devices.isEmpty()) {
            Toast.makeText(this, "Koppel de SK-Box eerst in Android Bluetooth-instellingen", Toast.LENGTH_LONG).show()
            return
        }

        val dialog = AlertDialog.Builder(this)
            .setTitle("Selecteer SK-Box")
            .setAdapter(SkBoxDeviceAdapter(devices)) { _, which ->
                val device = devices[which]
                getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
                    .edit()
                    .putString("BLUETOOTH_DEVICE_ADDRESS", device.address)
                    .apply()
                skBoxResumePromptShown = false
                protocolWarningShown = false
                ScoreKrijtBluetoothBox.connect(device)
            }
            .setNegativeButton("Verbreken") { _, _ ->
                ScoreKrijtBluetoothBox.disconnect()
                skBoxResumePromptShown = false
                protocolWarningShown = false
                updateSkBoxButton()
            }
            .show()

        dialog.listView.apply {
            isVerticalScrollBarEnabled = true
            scrollBarStyle = View.SCROLLBARS_INSIDE_INSET
            divider = null
            dividerHeight = 0
            setPadding(16, 4, 16, 4)
            clipToPadding = false
        }
    }

    private inner class SkBoxDeviceAdapter(
        devices: List<BluetoothDevice>
    ) : ArrayAdapter<BluetoothDevice>(this, R.layout.item_sk_box_device, devices) {
        override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
            val view = convertView ?: layoutInflater.inflate(R.layout.item_sk_box_device, parent, false)
            val device = getItem(position)
            view.findViewById<TextView>(R.id.tv_device_name).text = device?.name ?: "Onbekend apparaat"
            view.findViewById<TextView>(R.id.tv_device_address).text = device?.address ?: "Geen adres"
            return view
        }
    }
    private fun checkResumeButton() {
        val prefs = getSharedPreferences("ScoreKrijtState", MODE_PRIVATE)
        val saved = prefs.getBoolean("GAME_IN_PROGRESS", false)
        val finished = prefs.getBoolean("GAME_FINISHED", false)
        val btnResume = findViewById<Button>(R.id.btnResumeMatch)
        btnResume.text = getString(if (finished) R.string.ReopenLastGameKnop else R.string.ResumeGameKnop)
        btnResume.visibility = if (saved) View.VISIBLE else View.GONE
    }

    private fun checkLastMatchSummaryButton() {
        val prefs = getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
        val hasSummary = !prefs.getString("LAST_MATCH_SUMMARY_TEXT", null).isNullOrBlank()
        findViewById<Button>(R.id.btnLastMatchSummary).visibility = if (hasSummary) View.VISIBLE else View.GONE
    }

    fun onButtonClickLastMatchSummary(view: View) {
        val prefs = getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
        val summary = prefs.getString("LAST_MATCH_SUMMARY_TEXT", null)
        val title = prefs.getString("LAST_MATCH_SUMMARY_TITLE", "Laatste wedstrijd overzicht") ?: "Laatste wedstrijd overzicht"

        if (summary.isNullOrBlank()) {
            Toast.makeText(this, "Er is nog geen wedstrijd overzicht opgeslagen", Toast.LENGTH_SHORT).show()
            return
        }

        val dialogView = layoutInflater.inflate(R.layout.dialog_match_summary, null)
        dialogView.findViewById<TextView>(R.id.tv_summary_text).text = summary

        AlertDialog.Builder(this)
            .setTitle(title)
            .setView(dialogView)
            .setPositiveButton("Verzenden") { _, _ -> shareSummaryText(title, summary) }
            .setNegativeButton("Sluiten", null)
            .show()
    }

    private fun shareSummaryText(title: String, summary: String) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, title)
            putExtra(Intent.EXTRA_TEXT, summary)
        }
        startActivity(Intent.createChooser(intent, "Deel wedstrijd overzicht"))
    }

    fun onButtonClickSingleMatch(view: View) {
        val intent = Intent(this, SetupSingleMatch::class.java)
        startActivity(intent)
    }

    fun onButtonClickResumeMatch(view: View) {
        val intent = Intent(this, BiljardGame::class.java).apply {
            putExtra("RESUME_GAME", true)
        }
        startActivity(intent)
    }
}








