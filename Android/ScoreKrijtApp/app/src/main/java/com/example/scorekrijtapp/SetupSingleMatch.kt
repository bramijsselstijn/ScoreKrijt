package com.example.scorekrijtapp

import android.content.Intent
import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import android.widget.RadioGroup
import android.view.View

class SetupSingleMatch : AppCompatActivity() {

    private lateinit var etPlayer1Name: TextInputEditText
    private lateinit var etPlayer1TMC: TextInputEditText
    private lateinit var etPlayer2Name: TextInputEditText
    private lateinit var etPlayer2TMC: TextInputEditText
    private lateinit var tilPlayer1TMC: TextInputLayout
    private lateinit var tilPlayer2TMC: TextInputLayout
    private lateinit var etNumberOfRounds: TextInputEditText
    private lateinit var rgGameType: RadioGroup
    private lateinit var rgDrawOption: RadioGroup
    private lateinit var tvDrawOption: android.widget.TextView
    private lateinit var tilNumTurns: TextInputLayout // Veranderd naar TextInputLayout




    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_setup_single_match)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        initializeViews()
        setupListeners()

    }

    private fun initializeViews() {
        etPlayer1Name = findViewById(R.id.editTextSpeler1Naam)
        etPlayer1TMC = findViewById(R.id.editTextSpeler1TMC)
        tilPlayer1TMC = findViewById(R.id.textInputLayoutSpeler1TMC)
        etPlayer2Name = findViewById(R.id.editTextSpeler2Naam)
        etPlayer2TMC = findViewById(R.id.editTextSpeler2TMC)
        tilPlayer2TMC = findViewById(R.id.textInputLayoutSpeler2TMC)
        etNumberOfRounds = findViewById(R.id.TextInputEditAantalBeurten)
        rgGameType = findViewById(R.id.RadioGroupWedstrijdvorm)
        rgDrawOption = findViewById(R.id.RadioGroupGelijkspel)
        tvDrawOption = findViewById(R.id.textViewGelijkspel)
        tilNumTurns = findViewById(R.id.TextInputAantalBeurten)

        val prefs = getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
        val lastFixedTurns = prefs.getBoolean("LAST_FIXED_TURNS", true)
        val lastDrawAllowed = prefs.getBoolean("LAST_DRAW_ALLOWED", false)
        val lastNumTurns = prefs.getInt("LAST_NUM_TURNS", 30)
        rgGameType.check(if (lastFixedTurns) R.id.radioButtonVasteBeurten else R.id.radioButtonUitIsUit)
        rgDrawOption.check(if (lastDrawAllowed) R.id.radioButtonGelijkAan else R.id.radioButtonGelijkUit)
        etNumberOfRounds.setText(lastNumTurns.toString())
        tilNumTurns.visibility = if (lastFixedTurns) View.VISIBLE else View.GONE
        tvDrawOption.visibility = if (lastFixedTurns) View.GONE else View.VISIBLE
        rgDrawOption.visibility = if (lastFixedTurns) View.GONE else View.VISIBLE
    }
    private fun setupListeners() {
        rgGameType.setOnCheckedChangeListener { _, checkedId ->
            if (checkedId == R.id.radioButtonVasteBeurten) {
                tilNumTurns.visibility = View.VISIBLE
                tvDrawOption.visibility = View.GONE
                rgDrawOption.visibility = View.GONE
            }
            else {
                tilNumTurns.visibility = View.GONE
                tvDrawOption.visibility = View.VISIBLE
                rgDrawOption.visibility = View.VISIBLE
            }
        }


    }


    fun onButtonBepalenAanvangWedstrijd(view: android.view.View) {
        val p1Name = etPlayer1Name.text.toString().ifBlank { getString(R.string.Speler1TitleText) }
        val p1TMCString = etPlayer1TMC.text.toString()
        val p2Name = etPlayer2Name.text.toString().ifBlank { getString(R.string.Speler2TitleText) }
        val p2TMCString = etPlayer2TMC.text.toString()

        val p1TMC = p1TMCString.toIntOrNull()
        val p2TMC = p2TMCString.toIntOrNull()

        val numTurnString = etNumberOfRounds.text.toString().ifBlank { getString(R.string.AantalBeurten) }
        val numTurns = numTurnString.toIntOrNull()

        val isFixedTurns = rgGameType.checkedRadioButtonId == R.id.radioButtonVasteBeurten
        val drawAllowed = !isFixedTurns && rgDrawOption.checkedRadioButtonId == R.id.radioButtonGelijkAan

        getSharedPreferences("ScoreKrijtPrefs", MODE_PRIVATE)
            .edit()
            .putBoolean("LAST_FIXED_TURNS", isFixedTurns)
            .putInt("LAST_NUM_TURNS", numTurns ?: 30)
            .putBoolean("LAST_DRAW_ALLOWED", rgDrawOption.checkedRadioButtonId == R.id.radioButtonGelijkAan)
            .apply()

        var isValid = true

        if (p1TMC == null || p1TMC < 6) {
            tilPlayer1TMC.error = getString(R.string.Minimumetmc)
            isValid = false
        } else {
            tilPlayer1TMC.error = null
        }

        if (p2TMC == null || p2TMC < 6) {
            tilPlayer2TMC.error = getString(R.string.Minimumetmc)
            isValid = false
        } else {
            tilPlayer2TMC.error = null
        }
        if (numTurns == null || numTurns < 10) {
            tilNumTurns.error = getString(R.string.Minimumetmc)
            isValid = false
        } else {
            tilNumTurns.error = null
        }

        if (!isValid) return

        val intent = Intent(this, BepalenAanvangWedstrijd::class.java).apply {
            putExtra("p1Name", p1Name)
            putExtra("p1TMC", p1TMC)
            putExtra("p2Name", p2Name)
            putExtra("p2TMC", p2TMC)
            putExtra("numTurns", numTurns)
            putExtra("isFixedTurns", isFixedTurns)
            putExtra("DRAW_ALLOWED", drawAllowed)

        }

        startActivity(intent)
    }
}





