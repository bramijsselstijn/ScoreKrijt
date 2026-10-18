package com.example.scorekrijtapp

import android.graphics.Color
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.Menu
import android.view.MenuItem
import android.widget.Button
import android.widget.EditText
import android.widget.RadioGroup
import android.widget.RadioButton
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.math.ceil

class BiljardGame : AppCompatActivity() {

    // Spelinstellingen
    private var p1Name = ""
    private var p2Name = ""
    private var p1TMC = 20.0
    private var p2TMC = 15.0
    private var isFixedTurns = true
    private var maxTurns = 10
    private var startColorYellow = false
    private var drawAllowed = false

    // Spelstatus
    private var player1TotalCar = 0
    private var player2TotalCar = 0
    private var currentTurnCar = 0
    private var turnNumber = 1
    private var isPlayer1Turn = true

    // Statistieken
    private var p1HighestSerie = 0
    private var p2HighestSerie = 0
    private var p1PlayTime = 0L
    private var p2PlayTime = 0L
    private var matchStartTime = 0L

    // Timer logica
    private var lastTickTime = 0L
    private val handler = Handler(Looper.getMainLooper())
    private val timerRunnable = object : Runnable {
        override fun run() {
            val now = System.currentTimeMillis()
            if (lastTickTime != 0L) {
                val elapsed = (now - lastTickTime) / 1000
                if (isPlayer1Turn) p1PlayTime += elapsed else p2PlayTime += elapsed
            }
            lastTickTime = now
            handler.postDelayed(this, 1000)
        }
    }

    // UI Elementen
    private lateinit var tvStartTime: TextView
    private lateinit var tvP1Name: TextView
    private lateinit var tvP2Name: TextView
    private lateinit var tvActivePlayerName: TextView
    private lateinit var tvP1Caramboles: TextView
    private lateinit var tvP2Caramboles: TextView
    private lateinit var tvCurrentTurn: TextView
    private lateinit var tvP1TMC: TextView
    private lateinit var tvP2TMC: TextView
    private lateinit var tvP1Points: TextView
    private lateinit var tvP2Points: TextView
    private lateinit var tvInningScore: TextView
    private lateinit var tvRemaining: TextView
    private lateinit var btnHelpTop: TextView
    private val turnHistory = mutableListOf<TurnRecord>()
    private var returnToMainAfterShare = false
    private var matchFinished = false
    private var syncFromSkBoxPending = false
    private val shareCsvLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) {
        if (returnToMainAfterShare) {
            returnToMainAfterShare = false
            returnToMainMenu()
        }
    }


    data class TurnRecord(
        val turn: Int,
        var p1Score: Int? = null,
        var p1TotalAtEnd: Int? = null,
        var p2Score: Int? = null,
        var p2TotalAtEnd: Int? = null
    ) {
        // Een score telt pas mee (en staat in het totaal) zodra het totaal is vastgelegd.
        // Zonder totaal is het een onthouden tussenstand na Undo.
        fun p1Noted(): Int? = if (p1TotalAtEnd != null) p1Score else null
        fun p2Noted(): Int? = if (p2TotalAtEnd != null) p2Score else null
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_biljard_game)

        // Haal gegevens op uit Intent
        val rawP1Name = intent.getStringExtra("P1_NAME") ?: getString(R.string.player1_default)
        val rawP2Name = intent.getStringExtra("P2_NAME") ?: getString(R.string.player2_default)
        val rawP1TMC = intent.getDoubleExtra("P1_TMC", 20.0)
        val rawP2TMC = intent.getDoubleExtra("P2_TMC", 15.0)
        val startWithP1 = intent.getBooleanExtra("START_WITH_P1", true)

        isFixedTurns = intent.getBooleanExtra("FIXED_TURNS", true)
        maxTurns = intent.getIntExtra("NUM_TURNS", 10)
        startColorYellow = intent.getBooleanExtra("START_COLOR_YELLOW", false)
        drawAllowed = intent.getBooleanExtra("DRAW_ALLOWED", false)

        if (startWithP1) {
            p1Name = rawP1Name; p1TMC = rawP1TMC
            p2Name = rawP2Name; p2TMC = rawP2TMC
        } else {
            p1Name = rawP2Name; p1TMC = rawP2TMC
            p2Name = rawP1Name; p2TMC = rawP1TMC
        }

        isPlayer1Turn = true
        matchStartTime = System.currentTimeMillis()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        initializeViews()
        setupClickListeners()
        
        val isResumeGame = intent.getBooleanExtra("RESUME_GAME", false)
        if (isResumeGame) {
            loadGameState()
        } else {
            // Nieuwe wedstrijd initialisatie
            val rawP1Name = intent.getStringExtra("P1_NAME") ?: getString(R.string.player1_default)
            val rawP2Name = intent.getStringExtra("P2_NAME") ?: getString(R.string.player2_default)
            val rawP1TMC = intent.getDoubleExtra("P1_TMC", 20.0)
            val rawP2TMC = intent.getDoubleExtra("P2_TMC", 15.0)
            val startWithP1 = intent.getBooleanExtra("START_WITH_P1", true)

            isFixedTurns = intent.getBooleanExtra("FIXED_TURNS", true)
            maxTurns = intent.getIntExtra("NUM_TURNS", 10)
            startColorYellow = intent.getBooleanExtra("START_COLOR_YELLOW", false)
            drawAllowed = intent.getBooleanExtra("DRAW_ALLOWED", false)

            if (startWithP1) {
                p1Name = rawP1Name; p1TMC = rawP1TMC
                p2Name = rawP2Name; p2TMC = rawP2TMC
            } else {
                p1Name = rawP2Name; p1TMC = rawP2TMC
                p2Name = rawP1Name; p2TMC = rawP1TMC
            }

            isPlayer1Turn = true
            matchStartTime = System.currentTimeMillis()
        }

        updateUI()
        sendBluetoothMatchMessage(if (isResumeGame) "update_match" else "start_new_match")

        lastTickTime = System.currentTimeMillis()
        handler.post(timerRunnable)

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                showExitConfirmationDialog()
            }
        })
    }

    private fun showExitConfirmationDialog() {
        AlertDialog.Builder(this)
            .setTitle("Wedstrijd verlaten?")
            .setMessage("De huidige stand is opgeslagen. Je kunt de wedstrijd later hervatten vanuit het hoofdmenu.")
            .setPositiveButton("Verlaten") { _, _ ->
                saveGameState()
                finish()
            }
            .setNegativeButton("Blijven", null)
            .show()
    }

    private fun saveGameState() {
        if (matchFinished) return
        val prefs = getSharedPreferences("ScoreKrijtState", MODE_PRIVATE)
        val editor = prefs.edit()
        editor.putBoolean("GAME_IN_PROGRESS", true)
        editor.putString("P1_NAME", p1Name)
        editor.putString("P2_NAME", p2Name)
        editor.putFloat("P1_TMC", p1TMC.toFloat())
        editor.putFloat("P2_TMC", p2TMC.toFloat())
        editor.putBoolean("FIXED_TURNS", isFixedTurns)
        editor.putInt("MAX_TURNS", maxTurns)
        editor.putBoolean("COLOR_YELLOW", startColorYellow)
        editor.putBoolean("DRAW_ALLOWED", drawAllowed)
        
        editor.putInt("P1_TOTAL", player1TotalCar)
        editor.putInt("P2_TOTAL", player2TotalCar)
        editor.putInt("CURRENT_TURN_CAR", currentTurnCar)
        editor.putInt("TURN_NUMBER", turnNumber)
        editor.putBoolean("IS_P1_TURN", isPlayer1Turn)
        
        editor.putInt("P1_HIGH", p1HighestSerie)
        editor.putInt("P2_HIGH", p2HighestSerie)
        editor.putLong("P1_TIME", p1PlayTime)
        editor.putLong("P2_TIME", p2PlayTime)
        editor.putLong("MATCH_START", matchStartTime)

        val historyArray = JSONArray()
        turnHistory.forEach { record ->
            val obj = JSONObject()
            obj.put("turn", record.turn)
            obj.put("p1Score", record.p1Score ?: JSONObject.NULL)
            obj.put("p1Total", record.p1TotalAtEnd ?: JSONObject.NULL)
            obj.put("p2Score", record.p2Score ?: JSONObject.NULL)
            obj.put("p2Total", record.p2TotalAtEnd ?: JSONObject.NULL)
            historyArray.put(obj)
        }
        editor.putString("TURN_HISTORY", historyArray.toString())
        editor.apply()
    }

    private fun loadGameState() {
        val prefs = getSharedPreferences("ScoreKrijtState", MODE_PRIVATE)
        p1Name = prefs.getString("P1_NAME", "") ?: ""
        p2Name = prefs.getString("P2_NAME", "") ?: ""
        p1TMC = prefs.getFloat("P1_TMC", 20f).toDouble()
        p2TMC = prefs.getFloat("P2_TMC", 15f).toDouble()
        isFixedTurns = prefs.getBoolean("FIXED_TURNS", true)
        maxTurns = prefs.getInt("MAX_TURNS", 10)
        startColorYellow = prefs.getBoolean("COLOR_YELLOW", false)
        drawAllowed = prefs.getBoolean("DRAW_ALLOWED", false)
        
        player1TotalCar = prefs.getInt("P1_TOTAL", 0)
        player2TotalCar = prefs.getInt("P2_TOTAL", 0)
        currentTurnCar = prefs.getInt("CURRENT_TURN_CAR", 0)
        turnNumber = prefs.getInt("TURN_NUMBER", 1)
        isPlayer1Turn = prefs.getBoolean("IS_P1_TURN", true)
        
        p1HighestSerie = prefs.getInt("P1_HIGH", 0)
        p2HighestSerie = prefs.getInt("P2_HIGH", 0)
        p1PlayTime = prefs.getLong("P1_TIME", 0)
        p2PlayTime = prefs.getLong("P2_TIME", 0)
        matchStartTime = prefs.getLong("MATCH_START", System.currentTimeMillis())

        turnHistory.clear()
        val historyStr = prefs.getString("TURN_HISTORY", null)
        if (historyStr != null) {
            val array = JSONArray(historyStr)
            for (i in 0 until array.length()) {
                val obj = array.getJSONObject(i)
                val p1Score = if (obj.isNull("p1Score")) null else obj.getInt("p1Score")
                val p1Total = if (obj.isNull("p1Total")) null else obj.getInt("p1Total")
                val p2Score = if (obj.isNull("p2Score")) null else obj.getInt("p2Score")
                val p2Total = if (obj.isNull("p2Total")) null else obj.getInt("p2Total")
                turnHistory.add(TurnRecord(obj.getInt("turn"), p1Score, p1Total, p2Score, p2Total))
            }
        }
        refreshPlayerLabels()
    }

    private fun clearSavedState() {
        val prefs = getSharedPreferences("ScoreKrijtState", MODE_PRIVATE)
        prefs.edit().putBoolean("GAME_IN_PROGRESS", false).apply()
    }

    private fun initializeViews() {
        tvStartTime = findViewById(R.id.tv_start_time)
        tvP1Name = findViewById(R.id.tv_player1_name)
        tvP2Name = findViewById(R.id.tv_player2_name)
        tvActivePlayerName = findViewById(R.id.tv_active_player_name)
        tvP1Caramboles = findViewById(R.id.tv_p1_caramboles)
        tvP2Caramboles = findViewById(R.id.tv_p2_caramboles)
        tvCurrentTurn = findViewById(R.id.tv_current_turn)
        tvP1TMC = findViewById(R.id.tv_p1_tmc)
        tvP2TMC = findViewById(R.id.tv_p2_tmc)
        tvP1Points = findViewById(R.id.tv_p1_punten)
        tvP2Points = findViewById(R.id.tv_p2_punten)
        tvInningScore = findViewById(R.id.tv_inning_score)
        tvRemaining = findViewById(R.id.tv_remaining)
        btnHelpTop = findViewById(R.id.btn_help_top)

        refreshPlayerLabels()
    }

    private fun refreshPlayerLabels() {
        tvP1Name.text = p1Name
        tvP2Name.text = p2Name
        tvP1TMC.text = p1TMC.toInt().toString()
        tvP2TMC.text = p2TMC.toInt().toString()
    }

    private fun setupClickListeners() {
        findViewById<Button>(R.id.btn_plus).setOnClickListener {
            if (!isFixedTurns) {
                val activeTmc = if (isPlayer1Turn) p1TMC else p2TMC
                val activeTotal = if (isPlayer1Turn) player1TotalCar else player2TotalCar
                if (currentTurnCar >= (activeTmc - activeTotal)) return@setOnClickListener
            }
            currentTurnCar++
            updateUI()
            saveGameState()
            sendBluetoothMatchMessage("score_plus")
        }

        findViewById<Button>(R.id.btn_minus).setOnClickListener {
            if (currentTurnCar > 0) {
                currentTurnCar--
                updateUI()
                saveGameState()
                sendBluetoothMatchMessage("score_minus")
            }
        }

        findViewById<Button>(R.id.btn_edit).setOnClickListener { noteAndNextTurn() }
        findViewById<Button>(R.id.btn_undo).setOnClickListener { undoLastAction() }
        findViewById<TextView>(R.id.btn_settings).setOnClickListener { showGlobalSettingsDialog() }
        btnHelpTop.setOnClickListener {
            val intent = Intent(this, HelpActivity::class.java)
            startActivity(intent)
        }

        tvP1Name.setOnLongClickListener { showEditPlayerDialog(1); true }
        tvP2Name.setOnLongClickListener { showEditPlayerDialog(2); true }
    }
    private fun sendBluetoothMatchMessage(command: String) {
        if (!ScoreKrijtBluetoothBox.isConnected()) return

        val p1CurrentTotal = player1TotalCar + if (isPlayer1Turn) currentTurnCar else 0
        val p2CurrentTotal = player2TotalCar + if (!isPlayer1Turn) currentTurnCar else 0
        val p1CurrentPoints = calculatePoints(p1CurrentTotal, p1TMC)
        val p2CurrentPoints = calculatePoints(p2CurrentTotal, p2TMC)
        val startColor = if (startColorYellow) "Geel" else "Wit"

        val message = JSONObject()
            .put("cmd", command)
            .put("turn", if (command == "match_finished") 0 else turnNumber)
            .put("active_player", if (isPlayer1Turn) 1 else 2)
            .put("current_player", if (isPlayer1Turn) p1Name else p2Name)
            .put("current_turn_car", currentTurnCar)
            .put("current_car", currentTurnCar)
            .put("player1", p1Name)
            .put("player2", p2Name)
            .put("player1_tmc", p1TMC.toInt())
            .put("player2_tmc", p2TMC.toInt())
            .put("player1_car", player1TotalCar)
            .put("player2_car", player2TotalCar)
            .put("player1_current_total_car", p1CurrentTotal)
            .put("player2_current_total_car", p2CurrentTotal)
            .put("player1_points", p1CurrentPoints)
            .put("player2_points", p2CurrentPoints)
            .put("start_color", startColor)
            .put("game_type", if (isFixedTurns) "Vaste beurten" else "Uit is uit")
            .put("game_turns", maxTurns)
            .put("fixed_turns", isFixedTurns)
            .put("max_turns", maxTurns)
            .put("player1_data", JSONObject()
                .put("name", p1Name)
                .put("total_car", player1TotalCar)
                .put("current_total_car", p1CurrentTotal)
                .put("tmc", p1TMC)
                .put("points", p1CurrentPoints)
            )
            .put("player2_data", JSONObject()
                .put("name", p2Name)
                .put("total_car", player2TotalCar)
                .put("current_total_car", p2CurrentTotal)
                .put("tmc", p2TMC)
                .put("points", p2CurrentPoints)
            )

        val bluetoothHistory = JSONArray()
        turnHistory.forEach { record ->
            bluetoothHistory.put(JSONObject()
                .put("turn", record.turn)
                .put("p1_score", record.p1Noted() ?: JSONObject.NULL)
                .put("p1_total", record.p1TotalAtEnd ?: JSONObject.NULL)
                .put("p2_score", record.p2Noted() ?: JSONObject.NULL)
                .put("p2_total", record.p2TotalAtEnd ?: JSONObject.NULL)
            )
        }
        message.put("turn_history", bluetoothHistory)

        ScoreKrijtBluetoothBox.send(message)
    }
    private fun updateUI() {
        val sdf = SimpleDateFormat("HH:mm", Locale.getDefault())
        tvStartTime.text = getString(R.string.start_time_label, sdf.format(Date(matchStartTime)))

        tvP1Caramboles.text = player1TotalCar.toString()
        tvP2Caramboles.text = player2TotalCar.toString()
        tvInningScore.text = currentTurnCar.toString()
        tvCurrentTurn.text = turnNumber.toString()

        val p1CurrentTotal = player1TotalCar + (if (isPlayer1Turn) currentTurnCar else 0)
        val p2CurrentTotal = player2TotalCar + (if (!isPlayer1Turn) currentTurnCar else 0)

        tvP1Points.text = calculatePoints(p1CurrentTotal, p1TMC).toString()
        tvP2Points.text = calculatePoints(p2CurrentTotal, p2TMC).toString()

        val activeTmc = if (isPlayer1Turn) p1TMC else p2TMC
        val activeTotal = if (isPlayer1Turn) p1CurrentTotal else p2CurrentTotal
        val remaining = calculateRemainingForNextPoint(activeTotal, activeTmc)

        // FIX: Geef 'remaining' door als getal (Int) en NIET als tekst (String)
        // Omdat strings.xml een getal verwacht (%1$d)
        tvRemaining.text = getString(R.string.remaining_format, remaining)

        tvActivePlayerName.text = if (isPlayer1Turn) p1Name else p2Name

        if (isPlayer1Turn) {
            tvP1Name.setBackgroundColor(if (startColorYellow) Color.parseColor("#FFC000") else Color.WHITE)
            tvP2Name.setBackgroundColor(Color.LTGRAY)
        } else {
            tvP1Name.setBackgroundColor(Color.LTGRAY)
            tvP2Name.setBackgroundColor(if (startColorYellow) Color.WHITE else Color.parseColor("#FFC000"))
        }
    }

    private fun calculatePoints(car: Int, tmc: Double): Int {
        if (tmc <= 0) return 0
        return (car / (tmc / 10.0)).toInt() //.coerceAtMost(10)
    }

    private fun calculateRemainingForNextPoint(car: Int, tmc: Double): Int {
        if (tmc <= 0) return 0
        val valPerPoint = tmc / 10.0
        val nextPointTarget = (car / valPerPoint).toInt() + 1
        return (ceil(nextPointTarget * valPerPoint).toInt() - car).coerceAtLeast(0)
    }

    private fun noteAndNextTurn() {
        ensureTurnRecord(turnNumber)
        val record = turnHistory[turnNumber - 1]

        if (isPlayer1Turn) {
            record.p1Noted()?.let { player1TotalCar -= it }
            player1TotalCar += currentTurnCar
            if (currentTurnCar > p1HighestSerie) p1HighestSerie = currentTurnCar
            record.p1Score = currentTurnCar
            record.p1TotalAtEnd = player1TotalCar
            isPlayer1Turn = false
            currentTurnCar = record.p2Score ?: 0
        } else {
            record.p2Noted()?.let { player2TotalCar -= it }
            player2TotalCar += currentTurnCar
            if (currentTurnCar > p2HighestSerie) p2HighestSerie = currentTurnCar
            record.p2Score = currentTurnCar
            record.p2TotalAtEnd = player2TotalCar
            if (checkEndOfMatch()) return
            isPlayer1Turn = true
            turnNumber++
            ensureTurnRecord(turnNumber)
            currentTurnCar = turnHistory[turnNumber - 1].p1Score ?: 0
        }
        updateUI()
        saveGameState()
        sendBluetoothMatchMessage("next_turn")
        saveMatchToCsv(false, "Lopend")
    }

    private fun ensureTurnRecord(turn: Int) {
        while (turnHistory.size < turn) {
            turnHistory.add(TurnRecord(turnHistory.size + 1))
        }
    }
    private fun checkEndOfMatch(): Boolean {
        if (isFixedTurns) {
            if (turnNumber >= maxTurns) {
                finishGame("Vaste beurten bereikt")
                return true
            }
        } else {
            val p1Points = calculatePoints(player1TotalCar, p1TMC)
            val p2Points = calculatePoints(player2TotalCar, p2TMC)
            if (p1Points == 10 && p2Points == 10) {
                if (drawAllowed) {
                    finishGame("Gelijkspel")
                    return true
                }
                p1TMC = ceil(p1TMC * 1.3); p2TMC = ceil(p2TMC * 1.3)
                Toast.makeText(this, "Verlenging!", Toast.LENGTH_SHORT).show()
                refreshPlayerLabels()
            } else if (p1Points == 10 || p2Points == 10) {
                finishGame("Speler is uit")
                return true
            }
        }
        return false
    }

    private fun showGlobalSettingsDialog() {
        val view = LayoutInflater.from(this).inflate(R.layout.dialog_global_settings, null)
        val etP1Name = view.findViewById<EditText>(R.id.et_p1_name)
        val etP1TMC = view.findViewById<EditText>(R.id.et_p1_tmc)
        val etP2Name = view.findViewById<EditText>(R.id.et_p2_name)
        val etP2TMC = view.findViewById<EditText>(R.id.et_p2_tmc)
        val rgColor = view.findViewById<RadioGroup>(R.id.rg_start_color)
        val btnHelp = view.findViewById<Button>(R.id.btn_open_help)
        val btnTempSummary = view.findViewById<Button>(R.id.btn_temp_summary)
        val syncActions = view.findViewById<android.view.View>(R.id.sk_box_sync_actions)
        val btnSkBoxSettings = view.findViewById<Button>(R.id.btn_sk_box_settings_dialog)
        val btnSyncTo = view.findViewById<Button>(R.id.btn_sync_to_sk_box)
        val btnSyncFrom = view.findViewById<Button>(R.id.btn_sync_from_sk_box)

        syncActions.visibility = if (ScoreKrijtBluetoothBox.isConnected()) android.view.View.VISIBLE else android.view.View.GONE
        btnSkBoxSettings.setOnClickListener { startActivity(Intent(this, SkBoxSettingsActivity::class.java)) }
        btnSyncTo.setOnClickListener {
            sendBluetoothMatchMessage("update_match")
            Toast.makeText(this, "Wedstrijd naar SK-Box verzonden", Toast.LENGTH_SHORT).show()
        }
        btnSyncFrom.setOnClickListener {
            AlertDialog.Builder(this)
                .setTitle("Synchroniseren van SK-Box?")
                .setMessage("De huidige wedstrijdstand op de telefoon wordt vervangen door de stand van de SK-Box.")
                .setNegativeButton("Annuleren", null)
                .setPositiveButton("Synchroniseren") { _, _ ->
                    syncFromSkBoxPending = true
                    if (!ScoreKrijtBluetoothBox.send(JSONObject().put("cmd", "status"))) {
                        syncFromSkBoxPending = false
                        Toast.makeText(this, "Stand opvragen mislukt", Toast.LENGTH_SHORT).show()
                    }
                }.show()
        }

        etP1Name.setText(p1Name)
        etP1TMC.setText(p1TMC.toInt().toString())
        etP2Name.setText(p2Name)
        etP2TMC.setText(p2TMC.toInt().toString())
        
        if (startColorYellow) {
            rgColor.check(R.id.rb_color_yellow)
        } else {
            rgColor.check(R.id.rb_color_white)
        }

        btnTempSummary.setOnClickListener { showTemporaryMatchSummaryDialog() }

        btnHelp.setOnClickListener {
            val intent = Intent(this, HelpActivity::class.java)
            startActivity(intent)
        }

        AlertDialog.Builder(this)
            .setTitle("Instellingen")
            .setView(view)
            .setPositiveButton("Opslaan") { _, _ ->
                p1Name = etP1Name.text.toString()
                p1TMC = etP1TMC.text.toString().toDoubleOrNull() ?: p1TMC
                p2Name = etP2Name.text.toString()
                p2TMC = etP2TMC.text.toString().toDoubleOrNull() ?: p2TMC
                startColorYellow = rgColor.checkedRadioButtonId == R.id.rb_color_yellow
                
                val prefs = getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
                prefs.edit().putBoolean("LAST_COLOR_YELLOW", startColorYellow).apply()

                refreshPlayerLabels()
                updateUI()
                saveGameState()
                sendBluetoothMatchMessage("update_match")
            }
            .setNegativeButton("Annuleren", null)
            .show()
    }

    private fun showEditPlayerDialog(playerNum: Int) {
        val view = LayoutInflater.from(this).inflate(R.layout.dialog_edit_player, null)
        val etName = view.findViewById<EditText>(R.id.et_edit_name)
        val etTMC = view.findViewById<EditText>(R.id.et_edit_tmc)
        etName.setText(if (playerNum == 1) p1Name else p2Name)
        etTMC.setText((if (playerNum == 1) p1TMC else p2TMC).toInt().toString())
        AlertDialog.Builder(this).setTitle("Wijzig Speler $playerNum").setView(view)
            .setPositiveButton("Opslaan") { _, _ ->
                if (playerNum == 1) {
                    p1Name = etName.text.toString(); p1TMC = etTMC.text.toString().toDoubleOrNull() ?: p1TMC
                } else {
                    p2Name = etName.text.toString(); p2TMC = etTMC.text.toString().toDoubleOrNull() ?: p2TMC
                }
                refreshPlayerLabels(); updateUI(); saveGameState(); sendBluetoothMatchMessage("update_match")
            }.setNegativeButton("Annuleren", null).show()
    }

    private fun undoLastAction() {
        ensureTurnRecord(turnNumber)

        val currentTurn = turnHistory[turnNumber - 1]

        if (isPlayer1Turn) {
            if (turnNumber == 1) return
            currentTurn.p1Score = currentTurnCar.takeIf { it > 0 }
            currentTurn.p1TotalAtEnd = null
            turnNumber--
            isPlayer1Turn = false
            val previousTurn = turnHistory[turnNumber - 1]
            previousTurn.p2Noted()?.let { player2TotalCar -= it }
            previousTurn.p2TotalAtEnd = null
            currentTurnCar = previousTurn.p2Score ?: 0
        } else {
            currentTurn.p2Noted()?.let { player2TotalCar -= it }
            currentTurn.p2Score = currentTurnCar.takeIf { it > 0 }
            currentTurn.p2TotalAtEnd = null
            isPlayer1Turn = true
            currentTurn.p1Noted()?.let { player1TotalCar -= it }
            currentTurn.p1TotalAtEnd = null
            currentTurnCar = currentTurn.p1Score ?: 0
        }
        updateUI()
        saveGameState()
        sendBluetoothMatchMessage("undo")
        saveMatchToCsv(false, "Undo gebruikt")
    }
    private fun saveMatchToCsv(isFinished: Boolean = false, finishReason: String = "", shareWhenFinished: Boolean = true) {
        val sdfDate = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        val sdfTime = SimpleDateFormat("HH:mm", Locale.getDefault())
        val dateStr = sdfDate.format(Date(matchStartTime))
        val startTimeStr = sdfTime.format(Date(matchStartTime))
        
        val duration = (System.currentTimeMillis() - matchStartTime) / 1000
        val durationStr = String.format("%02d:%02d", duration / 3600, (duration % 3600) / 60)

        val fileName = "${dateStr}_${startTimeStr.replace(":", "-")}_${p1Name}_vs_${p2Name}${if (isFinished) "_FINISH" else "_RUNNING"}.csv"
        
        try {
            val matchesDir = File(filesDir, "matches").apply { if (!exists()) mkdirs() }
            val file = File(matchesDir, fileName)
            file.writer().use { out ->
                out.write("sep=;\n")
                out.write("Datum;${dateStr}\n")
                out.write("Tijd;${durationStr}\n\n")
                
                out.write("Speler 1;${p1Name};TMC;${p1TMC.toInt()}\n")
                out.write("Speler 2;${p2Name};TMC;${p2TMC.toInt()}\n\n")
                
                out.write("Wedstrijdvorm;${if (isFixedTurns) "Vaste beurten" else if (drawAllowed) "Uit is uit - Gelijk aan" else "Uit is uit - Gelijk uit"}\n")
                if (isFixedTurns) out.write("Aantal beurten;${maxTurns}\n")
                out.write("\n")
                
                out.write("${p1Name}; ; ; ;${p2Name}\n")
                out.write("Beurt;Car;Tot; ;Beurt;Car;Tot\n")
                
                for (i in 0 until turnNumber) {
                    val record = if (i < turnHistory.size) turnHistory[i] else null
                    val b = i + 1
                    
                    val p1C = record?.p1Noted()?.toString() ?: ""
                    val p1T = record?.p1TotalAtEnd?.toString() ?: ""
                    
                    // Als we in de huidige beurt zijn en P1 heeft al gespeeld maar P2 nog niet
                    val p2C = record?.p2Noted()?.toString() ?: ""
                    val p2T = record?.p2TotalAtEnd?.toString() ?: ""
                    
                    out.write("${b};${p1C};${p1T}; ;${b};${p2C};${p2T}\n")
                }
                
                out.write("\n")
                out.write("${p1Name} totaal caramboles;${player1TotalCar}\n")
                out.write("${p2Name} totaal caramboles;${player2TotalCar}\n\n")
                
                val p1TimeStr = String.format("%02d:%02d:%02d", p1PlayTime / 3600, (p1PlayTime % 3600) / 60, p1PlayTime % 60)
                val p2TimeStr = String.format("%02d:%02d:%02d", p2PlayTime / 3600, (p2PlayTime % 3600) / 60, p2PlayTime % 60)
                
                out.write("${p1Name} speeltijd;${p1TimeStr}\n")
                out.write("${p2Name} speeltijd;${p2TimeStr}\n\n")
                
                out.write("###########################\n")
                out.write("WEDSTRIJDSTATUS\n")
                out.write("###########################\n")
                out.write("Eindstatus;${if (isFinished) "AFGEROND" else "LOPEND"}\n")
                out.write("Reden einde;${finishReason}\n\n")
                
                out.write("${p1Name} punten;${calculatePoints(player1TotalCar, p1TMC)}\n")
                out.write("${p2Name} punten;${calculatePoints(player2TotalCar, p2TMC)}\n\n")
                
                val p1Pts = calculatePoints(player1TotalCar, p1TMC)
                val p2Pts = calculatePoints(player2TotalCar, p2TMC)
                val winner = when {
                    p1Pts > p2Pts -> p1Name
                    p2Pts > p1Pts -> p2Name
                    else -> "Gelijkspel"
                }
                out.write("Winnaar;${winner}\n")
            }
            
            if (isFinished && shareWhenFinished) {
                shareCsvFile(file)
            }
        } catch (e: Exception) { 
            e.printStackTrace() 
            runOnUiThread {
                Toast.makeText(this, "Fout bij opslaan CSV: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun shareCsvFile(file: File) {
        val uri = androidx.core.content.FileProvider.getUriForFile(
            this,
            "${packageName}.fileprovider",
            file
        )
        
        val intent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
            type = "text/csv"
            putExtra(android.content.Intent.EXTRA_SUBJECT, "Wedstrijdverslag: ${p1Name} vs ${p2Name}")
            putExtra(android.content.Intent.EXTRA_STREAM, uri)
            addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        
        shareCsvLauncher.launch(android.content.Intent.createChooser(intent, "Deel wedstrijdverslag"))
    }

    private fun finishGame(reason: String) {
        matchFinished = true
        handler.removeCallbacks(timerRunnable)
        updateUI()
        sendBluetoothMatchMessage("match_finished")
        showMatchSummaryDialog(reason)
    }

    private fun buildMatchSummaryText(reason: String, includeCurrentTurn: Boolean): String {
        val sdfDate = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        val dateStr = sdfDate.format(Date(matchStartTime))
        val duration = (System.currentTimeMillis() - matchStartTime) / 1000
        val durationStr = String.format("%02d:%02d", duration / 3600, (duration % 3600) / 60)

        val p1Total = player1TotalCar + if (includeCurrentTurn && isPlayer1Turn) currentTurnCar else 0
        val p2Total = player2TotalCar + if (includeCurrentTurn && !isPlayer1Turn) currentTurnCar else 0

        val sb = StringBuilder()
        sb.append("WEDSTRIJD OVERZICHT\n")
        sb.append("----------------------------\n")
        sb.append("Datum: $dateStr\n")
        sb.append("Tijd: $durationStr\n\n")

        sb.append("SPELER 1: $p1Name\n")
        sb.append("TMC: ${p1TMC.toInt()}\n")
        sb.append("Totaal Caramboles: $p1Total\n")
        sb.append("Punten: ${calculatePoints(p1Total, p1TMC)}\n")
        val p1TimeStr = String.format("%02d:%02d:%02d", p1PlayTime / 3600, (p1PlayTime % 3600) / 60, p1PlayTime % 60)
        sb.append("Speeltijd: $p1TimeStr\n\n")

        sb.append("SPELER 2: $p2Name\n")
        sb.append("TMC: ${p2TMC.toInt()}\n")
        sb.append("Totaal Caramboles: $p2Total\n")
        sb.append("Punten: ${calculatePoints(p2Total, p2TMC)}\n")
        val p2TimeStr = String.format("%02d:%02d:%02d", p2PlayTime / 3600, (p2PlayTime % 3600) / 60, p2PlayTime % 60)
        sb.append("Speeltijd: $p2TimeStr\n\n")

        sb.append("Wedstrijdvorm: ${if (isFixedTurns) "Vaste beurten" else if (drawAllowed) "Uit is uit - Gelijk aan" else "Uit is uit - Gelijk uit"}\n")
        if (isFixedTurns) sb.append("Max beurten: $maxTurns\n")
        sb.append("Gespeelde beurten: $turnNumber\n")
        if (includeCurrentTurn) {
            sb.append("Huidige speler: ${if (isPlayer1Turn) p1Name else p2Name}\n")
            sb.append("Huidige beurt caramboles: $currentTurnCar\n")
        }
        sb.append("Reden overzicht: $reason\n\n")

        val p1Pts = calculatePoints(p1Total, p1TMC)
        val p2Pts = calculatePoints(p2Total, p2TMC)
        val winner = when {
            p1Pts > p2Pts -> p1Name
            p2Pts > p1Pts -> p2Name
            else -> "Gelijkspel"
        }
        sb.append("WINNAAR: $winner\n")
        sb.append("----------------------------\n\n")

        sb.append("BEURTENLIJST:\n")
        sb.append(String.format("%-4s | %-3s %-3s | %-3s %-3s\n", "Brt", "P1C", "P1T", "P2C", "P2T"))
        sb.append("-----|---------|---------\n")
        for (i in 0 until turnNumber) {
            val r = if (i < turnHistory.size) turnHistory[i] else null
            sb.append(String.format("%-4d | %-3s %-3s | %-3s %-3s\n",
                i + 1,
                r?.p1Noted()?.toString() ?: "",
                r?.p1TotalAtEnd?.toString() ?: "",
                r?.p2Noted()?.toString() ?: "",
                r?.p2TotalAtEnd?.toString() ?: ""))
        }

        return sb.toString()
    }

    private fun showTemporaryMatchSummaryDialog() {
        val summaryText = buildMatchSummaryText("Tijdelijk overzicht", includeCurrentTurn = true)
        val view = LayoutInflater.from(this).inflate(R.layout.dialog_match_summary, null)
        view.findViewById<TextView>(R.id.tv_summary_text).text = summaryText

        AlertDialog.Builder(this)
            .setTitle("Tijdelijk wedstrijd overzicht")
            .setView(view)
            .setPositiveButton("Verzenden") { _, _ -> shareSummaryText("Tijdelijk wedstrijd overzicht", summaryText) }
            .setNegativeButton("Sluiten", null)
            .show()
    }

    private fun saveLastMatchSummary(summaryText: String) {
        getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
            .edit()
            .putString("LAST_MATCH_SUMMARY_TEXT", summaryText)
            .putString("LAST_MATCH_SUMMARY_TITLE", "Laatste wedstrijd: $p1Name - $p2Name")
            .apply()
    }

    private fun shareSummaryText(title: String, summaryText: String) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, title)
            putExtra(Intent.EXTRA_TEXT, summaryText)
        }
        startActivity(Intent.createChooser(intent, "Deel wedstrijd overzicht"))
    }

    private fun showMatchSummaryDialog(reason: String) {
        val summaryText = buildMatchSummaryText(reason, includeCurrentTurn = false)
        saveLastMatchSummary(summaryText)

        val view = LayoutInflater.from(this).inflate(R.layout.dialog_match_summary, null)
        val tvSummary = view.findViewById<TextView>(R.id.tv_summary_text)
        tvSummary.text = summaryText

        AlertDialog.Builder(this)
            .setTitle("Wedstrijd Afgelopen")
            .setView(view)
            .setPositiveButton("Verzenden & Sluiten") { _, _ ->
                returnToMainAfterShare = true
                saveMatchToCsv(true, reason)
                clearSavedState()
            }
            .setNegativeButton("Alleen Sluiten") { _, _ ->
                clearSavedState()
                returnToMainMenu()
            }
            .setCancelable(true)
            .setOnCancelListener {
                matchFinished = false
                lastTickTime = System.currentTimeMillis()
                handler.post(timerRunnable)
            }
            .show()
    }
    private fun returnToMainMenu() {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
        startActivity(intent)
        finish()
    }
    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menu?.add(0, 1, 0, "Nieuwe Wedstrijd"); menu?.add(0, 2, 0, "Einde Wedstrijd")
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when (item.itemId) {
            1 -> resetGame()
            2 -> finishGame("Einde")
        }
        return super.onOptionsItemSelected(item)
    }

    private fun resetGame() {
        matchFinished = false
        player1TotalCar = 0; player2TotalCar = 0; currentTurnCar = 0; turnNumber = 1
        p1PlayTime = 0; p2PlayTime = 0; p1HighestSerie = 0; p2HighestSerie = 0
        isPlayer1Turn = true; turnHistory.clear(); updateUI()
        sendBluetoothMatchMessage("start_new_match")
    }

    override fun onPause() {
        super.onPause()
        saveGameState()
        ScoreKrijtBluetoothBox.clearListeners()
    }

    override fun onResume() {
        super.onResume()
        ScoreKrijtBluetoothBox.setListeners(
            onStatusChanged = { status ->
                if (status.contains("mislukt", true) || status.contains("verbroken", true)) {
                    runOnUiThread { Toast.makeText(this, status, Toast.LENGTH_SHORT).show() }
                }
            },
            onMessageReceived = { message -> runOnUiThread { handleGameBluetoothMessage(message) } }
        )
    }

    private fun handleGameBluetoothMessage(message: JSONObject) {
        if (!syncFromSkBoxPending || message.optString("event") != "game_state") return
        syncFromSkBoxPending = false
        val game = message.optJSONObject("game") ?: return
        p1Name = game.optString("player1", p1Name)
        p2Name = game.optString("player2", p2Name)
        p1TMC = game.optDouble("player1_tmc", p1TMC)
        p2TMC = game.optDouble("player2_tmc", p2TMC)
        player1TotalCar = game.optInt("player1_car", player1TotalCar)
        player2TotalCar = game.optInt("player2_car", player2TotalCar)
        currentTurnCar = game.optInt("current_car", currentTurnCar)
        turnNumber = game.optInt("turn", turnNumber)
        isPlayer1Turn = game.optInt("active_player", if (isPlayer1Turn) 1 else 2) == 1
        isFixedTurns = game.optString("game_type", if (isFixedTurns) "Vaste beurten" else "Uit is uit") == "Vaste beurten"
        maxTurns = game.optInt("game_turns", maxTurns)
        startColorYellow = game.optString("start_color", if (startColorYellow) "Geel" else "Wit") == "Geel"
        p1HighestSerie = game.optInt("player1_highest_serie", p1HighestSerie)
        p2HighestSerie = game.optInt("player2_highest_serie", p2HighestSerie)
        p1PlayTime = game.optLong("player1_play_time", p1PlayTime)
        p2PlayTime = game.optLong("player2_play_time", p2PlayTime)

        turnHistory.clear()
        val history = game.optJSONArray("turn_history") ?: JSONArray()
        for (index in 0 until history.length()) {
            val row = history.optJSONObject(index) ?: continue
            turnHistory.add(TurnRecord(
                row.optInt("turn", index + 1),
                if (row.isNull("p1_score")) null else row.optInt("p1_score"),
                if (row.isNull("p1_total")) null else row.optInt("p1_total"),
                if (row.isNull("p2_score")) null else row.optInt("p2_score"),
                if (row.isNull("p2_total")) null else row.optInt("p2_total")
            ))
        }
        refreshPlayerLabels(); updateUI(); saveGameState()
        Toast.makeText(this, "Wedstrijd van SK-Box overgenomen", Toast.LENGTH_SHORT).show()
    }

    override fun onDestroy() {
        super.onDestroy()
        handler.removeCallbacks(timerRunnable)
    }
}






















