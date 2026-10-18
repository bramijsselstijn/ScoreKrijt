package com.example.scorekrijtapp

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.graphics.Typeface
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.SwitchCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import org.json.JSONObject

class SkBoxSettingsActivity : AppCompatActivity() {
    private data class Setting(val key: String, val label: String, val min: Int, val max: Int)
    private val definitions = listOf(
        Setting("history_rows", "Aantal getoonde beurten", 1, 10),
        Setting("player_name_size", "Spelersnamen", 20, 120),
        Setting("score_text_size", "Tekst caramboles / score", 20, 80),
        Setting("score_value_size", "Waarde caramboles / score", 120, 280),
        Setting("turn_text_size", "Tekst beurt", 50, 90), Setting("turn_value_size", "Waarde beurt", 50, 150),
        Setting("current_car_text_size", "Tekst huidige caramboles", 20, 80), Setting("current_car_value_size", "Waarde huidige caramboles", 40, 80),
        Setting("tmc_text_size", "Tekst TMC", 10, 60), Setting("tmc_value_size", "Waarde TMC", 15, 90),
        Setting("points_text_size", "Tekst punten", 10, 50), Setting("points_value_size", "Waarde punten", 20, 80),
        Setting("stats_text_size", "Tekst statistieken", 10, 50), Setting("stats_value_size", "Waarden statistieken", 20, 80),
        Setting("history_text_size", "Tekst geschiedenis", 10, 50), Setting("history_value_size", "Waarden geschiedenis", 10, 50)
    )
    private val values = mutableMapOf<String, Int>()
    private val valueLabels = mutableMapOf<String, TextView>()
    private val seekBars = mutableMapOf<String, SeekBar>()
    private lateinit var historySwitch: SwitchCompat
    private lateinit var status: TextView
    private var loading = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState); setContentView(R.layout.activity_sk_box_settings)
        val extraVerticalSpace = (8 * resources.displayMetrics.density).toInt()
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.skBoxSettingsRoot)) { view, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            view.setPadding(
                systemBars.left,
                systemBars.top + extraVerticalSpace,
                systemBars.right,
                systemBars.bottom + extraVerticalSpace
            )
            insets
        }
        findViewById<Button>(R.id.btnBack).setOnClickListener { finish() }
        status = findViewById(R.id.tvSettingsStatus); historySwitch = findViewById(R.id.switchHistory)
        buildControls(findViewById(R.id.settingsContainer))
        historySwitch.setOnCheckedChangeListener { _, _ -> if (!loading) send("preview_display_settings") }
        findViewById<Button>(R.id.btnSaveSettings).setOnClickListener { send("save_display_settings") }
        findViewById<Button>(R.id.btnResetSettings).setOnClickListener {
            AlertDialog.Builder(this).setTitle("Standaardweergave herstellen?").setMessage("Alle grootscherminstellingen worden teruggezet en opgeslagen op de SK-Box.")
                .setNegativeButton("Annuleren", null).setPositiveButton("Herstellen") { _, _ -> ScoreKrijtBluetoothBox.send(JSONObject().put("cmd", "reset_display_settings")) }.show()
        }
        findViewById<Button>(R.id.btnBluetoothDebug).setOnClickListener { showBluetoothDebug() }
    }

    override fun onResume() {
        super.onResume()
        ScoreKrijtBluetoothBox.setListeners(onStatusChanged = { runOnUiThread { status.text = it } }, onMessageReceived = { runOnUiThread { receive(it) } })
        if (ScoreKrijtBluetoothBox.isConnected()) ScoreKrijtBluetoothBox.send(JSONObject().put("cmd", "get_display_settings")) else status.text = "SK-Box niet verbonden"
    }
    override fun onPause() { super.onPause(); ScoreKrijtBluetoothBox.clearListeners() }

    private fun buildControls(container: LinearLayout) = definitions.forEach { d ->
        val label = TextView(this).apply { text = d.label; textSize = 16f; setPadding(0, 18, 0, 0) }
        val valueLabel = TextView(this).apply { text = "–"; textSize = 14f }
        val seek = SeekBar(this).apply { max = d.max - d.min }
        valueLabels[d.key] = valueLabel; seekBars[d.key] = seek
        container.addView(label); container.addView(valueLabel); container.addView(seek)
        seek.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(bar: SeekBar?, progress: Int, fromUser: Boolean) { if (fromUser) { values[d.key] = d.min + progress; valueLabel.text = (d.min + progress).toString() } }
            override fun onStartTrackingTouch(bar: SeekBar?) = Unit
            override fun onStopTrackingTouch(bar: SeekBar?) { if (!loading) send("preview_display_settings") }
        })
    }

    private fun send(command: String) {
        if (!ScoreKrijtBluetoothBox.isConnected()) { Toast.makeText(this, "SK-Box niet verbonden", Toast.LENGTH_SHORT).show(); return }
        val settings = JSONObject().put("show_history", historySwitch.isChecked); values.forEach { (key, value) -> settings.put(key, value) }
        if (ScoreKrijtBluetoothBox.send(JSONObject().put("cmd", command).put("settings", settings))) status.text = if (command == "save_display_settings") "Opslaan…" else "Live voorbeeld bijgewerkt"
    }

    private fun receive(message: JSONObject) {
        if (message.optString("event") != "display_settings") return
        val settings = message.optJSONObject("settings") ?: return; loading = true
        historySwitch.isChecked = settings.optBoolean("show_history", true)
        definitions.forEach { d -> if (settings.has(d.key)) { val number = settings.optInt(d.key).coerceIn(d.min, d.max); values[d.key] = number; valueLabels[d.key]?.text = number.toString(); seekBars[d.key]?.progress = number - d.min } }
        loading = false; status.text = if (message.optBoolean("saved")) "Opgeslagen op de SK-Box" else "Wijzigingen worden direct getoond"
    }

    private fun showBluetoothDebug() {
        val padding = (16 * resources.displayMetrics.density).toInt()
        val logView = TextView(this).apply {
            typeface = Typeface.MONOSPACE
            textSize = 11f
            setPadding(padding, padding, padding, padding)
            setTextIsSelectable(true)
        }
        val scrollView = ScrollView(this).apply { addView(logView) }
        val handler = Handler(Looper.getMainLooper())
        val refresh = object : Runnable {
            override fun run() {
                val updatedLog = ScoreKrijtBluetoothBox.debugLogText()
                if (logView.text.toString() != updatedLog) {
                    logView.text = updatedLog
                    scrollView.post { scrollView.fullScroll(ScrollView.FOCUS_DOWN) }
                }
                handler.postDelayed(this, 500)
            }
        }
        val dialog = AlertDialog.Builder(this)
            .setTitle("Bluetooth-communicatie")
            .setMessage("TX = telefoon naar SK-Box, RX = SK-Box naar telefoon")
            .setView(scrollView)
            .setNeutralButton("Log wissen", null)
            .setPositiveButton("Sluiten", null)
            .create()
        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_NEUTRAL).setOnClickListener {
                ScoreKrijtBluetoothBox.clearDebugLog()
                logView.text = ScoreKrijtBluetoothBox.debugLogText()
            }
            handler.post(refresh)
        }
        dialog.setOnDismissListener { handler.removeCallbacks(refresh) }
        dialog.show()
    }
}
