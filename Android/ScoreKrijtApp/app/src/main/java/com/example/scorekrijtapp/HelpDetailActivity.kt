package com.example.scorekrijtapp

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.appbar.MaterialToolbar

class HelpDetailActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_help_detail)

        val title = intent.getStringExtra("TITLE") ?: ""
        val content = intent.getStringExtra("CONTENT") ?: ""

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar_help_detail)
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        toolbar.title = title
        toolbar.setNavigationOnClickListener { finish() }

        findViewById<TextView>(R.id.tv_help_content).text = content
    }
}
