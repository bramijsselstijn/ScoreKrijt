package com.example.scorekrijtapp

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import org.json.JSONObject

class BepalenAanvangWedstrijd : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_bepalen_aanvang_wedstrijd)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Data ophalen uit de Intent
        val p1Name = intent.getStringExtra("p1Name") ?: "Speler 1"
        val p1TMC = intent.getIntExtra("p1TMC", 6)
        val p2Name = intent.getStringExtra("p2Name") ?: "Speler 2"
        val p2TMC = intent.getIntExtra("p2TMC", 6)
        val numTurns = intent.getIntExtra("numTurns", 30)
        val isFixedTurns = intent.getBooleanExtra("isFixedTurns", true)
        val drawAllowed = intent.getBooleanExtra("DRAW_ALLOWED", false)

        // UI elementen koppelen
        val tvSummaryP1 = findViewById<TextView>(R.id.tvSummaryP1)
        val tvSummaryP2 = findViewById<TextView>(R.id.tvSummaryP2)
        val tvSummaryGameType = findViewById<TextView>(R.id.tvSummaryGameType)
        val rbStarterP1 = findViewById<RadioButton>(R.id.rbStarterP1)
        val rbStarterP2 = findViewById<RadioButton>(R.id.rbStarterP2)
        val btnStartMatch = findViewById<Button>(R.id.btnStartMatch)
        val btnResumeMatch = findViewById<Button>(R.id.btnResumeMatchBepalen)

        // Samenvatting invullen
        tvSummaryP1.text = "$p1Name ($p1TMC TMC)"
        tvSummaryP2.text = "$p2Name ($p2TMC TMC)"
        
        val gameTypeText = if (isFixedTurns) {
            "Vaste beurten ($numTurns)"
        } else {
            if (drawAllowed) "Uit is uit - Gelijk aan" else "Uit is uit - Gelijk uit"
        }
        tvSummaryGameType.text = "Wedstrijdvorm: $gameTypeText"

        // Namen op de RadioButtons zetten
        rbStarterP1.text = p1Name
        rbStarterP2.text = p2Name
        rbStarterP1.isChecked = true // Standaard speler 1 laten beginnen

        val prefs = getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
        val lastColorYellow = prefs.getBoolean("LAST_COLOR_YELLOW", false)

        val rbColorWhite = findViewById<RadioButton>(R.id.rbColorWhite)
        val rbColorYellow = findViewById<RadioButton>(R.id.rbColorYellow)
        
        if (lastColorYellow) {
            rbColorYellow.isChecked = true
        } else {
            rbColorWhite.isChecked = true
        }

        // Check for resume
        val statePrefs = getSharedPreferences("ScoreKrijtState", MODE_PRIVATE)
        // Een afgeronde wedstrijd (alleen nog te heropenen vanuit het hoofdmenu) telt hier niet mee.
        val inProgress = statePrefs.getBoolean("GAME_IN_PROGRESS", false) &&
            !statePrefs.getBoolean("GAME_FINISHED", false)
        btnResumeMatch.visibility = if (inProgress) View.VISIBLE else View.GONE

        // Laat de namen en TMC alvast op de SK-Box zien. Een wedstrijd die op de SK-Box loopt blijft
        // ongemoeid: de SK-Box negeert dit bericht dan zelf. Een oudere SK-Box kent het commando niet
        // en antwoordt met een melding die hier niet wordt getoond.
        if (ScoreKrijtBluetoothBox.isConnected()) {
            ScoreKrijtBluetoothBox.send(
                JSONObject()
                    .put("cmd", "prepare_match")
                    .put("player1", p1Name)
                    .put("player2", p2Name)
                    .put("player1_tmc", p1TMC)
                    .put("player2_tmc", p2TMC)
                    .put("game_type", if (isFixedTurns) "Vaste beurten" else "Uit is uit")
                    .put("game_turns", numTurns)
            )
        }

        btnResumeMatch.setOnClickListener {
            val intentResume = android.content.Intent(this, BiljardGame::class.java).apply {
                putExtra("RESUME_GAME", true)
            }
            startActivity(intentResume)
        }

        btnStartMatch.setOnClickListener {
            if (inProgress) {
                AlertDialog.Builder(this)
                    .setTitle("Nieuwe wedstrijd starten?")
                    .setMessage("Er is nog een wedstrijd gaande. Als je een nieuwe wedstrijd start, gaan de gegevens van de huidige wedstrijd verloren. Weet je het zeker?")
                    .setPositiveButton("Start Nieuwe") { _, _ ->
                        startNewGame(p1Name, p1TMC, p2Name, p2TMC, rbStarterP1.isChecked, isFixedTurns, numTurns, rbColorYellow.isChecked, drawAllowed)
                    }
                    .setNegativeButton("Annuleren", null)
                    .show()
            } else {
                startNewGame(p1Name, p1TMC, p2Name, p2TMC, rbStarterP1.isChecked, isFixedTurns, numTurns, rbColorYellow.isChecked, drawAllowed)
            }
        }
    }

    private fun startNewGame(p1Name: String, p1TMC: Int, p2Name: String, p2TMC: Int, startWithP1: Boolean, isFixedTurns: Boolean, numTurns: Int, isYellow: Boolean, drawAllowed: Boolean) {
        val prefs = getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
        prefs.edit()
            .putBoolean("LAST_COLOR_YELLOW", isYellow)
            .putBoolean("LAST_FIXED_TURNS", isFixedTurns)
            .putInt("LAST_NUM_TURNS", numTurns)
            .putBoolean("LAST_DRAW_ALLOWED", drawAllowed)
            .apply()

        val intent = android.content.Intent(this, BiljardGame::class.java).apply {
            putExtra("P1_NAME", p1Name)
            putExtra("P2_NAME", p2Name)
            putExtra("P1_TMC", p1TMC.toDouble())
            putExtra("P2_TMC", p2TMC.toDouble())
            putExtra("START_WITH_P1", startWithP1)
            putExtra("FIXED_TURNS", isFixedTurns)
            putExtra("NUM_TURNS", numTurns)
            putExtra("START_COLOR_YELLOW", isYellow)
            putExtra("DRAW_ALLOWED", drawAllowed)
        }
        startActivity(intent)
    }
}



