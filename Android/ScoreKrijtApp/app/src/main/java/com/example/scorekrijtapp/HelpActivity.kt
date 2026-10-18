package com.example.scorekrijtapp

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.appbar.MaterialToolbar

class HelpActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_help)

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar_help)
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        toolbar.setNavigationOnClickListener { finish() }

        val rv = findViewById<RecyclerView>(R.id.rv_help_categories)
        rv.layoutManager = LinearLayoutManager(this)
        
        val categories = listOf(
            HelpCategory(
                getString(R.string.help_category_general),
                listOf(
                    HelpTopic(getString(R.string.help_topic_biljart), getString(R.string.help_content_biljart)),
                    HelpTopic(getString(R.string.help_topic_acquitstoot), getString(R.string.help_content_acquitstoot)),
                    HelpTopic(getString(R.string.help_topic_fouten), getString(R.string.help_content_fouten))
                )
            ),
            HelpCategory(
                getString(R.string.help_category_libre),
                listOf(
                    HelpTopic(getString(R.string.help_topic_libre_spel), getString(R.string.help_content_libre_spel)),
                    HelpTopic(getString(R.string.help_topic_uitspringen), getString(R.string.help_content_uitspringen_libre)),
                    HelpTopic(getString(R.string.help_topic_vastliggen), getString(R.string.help_content_vastliggen_libre))
                )
            ),
            HelpCategory(
                getString(R.string.help_category_bandstoten),
                listOf(
                    HelpTopic(getString(R.string.help_topic_bandstoten_spel), getString(R.string.help_content_bandstoten_spel)),
                    HelpTopic(getString(R.string.help_topic_uitspringen), getString(R.string.help_content_uitspringen_libre)),
                    HelpTopic(getString(R.string.help_topic_vastliggen), getString(R.string.help_content_vastliggen_libre))
                )
            ),
            HelpCategory(
                getString(R.string.help_category_driebanden),
                listOf(
                    HelpTopic(getString(R.string.help_topic_driebanden_spel), getString(R.string.help_content_driebanden_spel)),
                    HelpTopic(getString(R.string.help_topic_uitspringen), getString(R.string.help_content_uitspringen_driebanden)),
                    HelpTopic(getString(R.string.help_topic_vastliggen), getString(R.string.help_content_vastliggen_driebanden))
                )
            ),
            HelpCategory(
                getString(R.string.help_category_sk_box),
                listOf(
                    HelpTopic(getString(R.string.help_topic_sk_box_connection), getString(R.string.help_content_sk_box_connection)),
                    HelpTopic(getString(R.string.help_topic_sk_box_sync), getString(R.string.help_content_sk_box_sync)),
                    HelpTopic(getString(R.string.help_topic_sk_box_display), getString(R.string.help_content_sk_box_display)),
                    HelpTopic(getString(R.string.help_topic_sk_box_debug), getString(R.string.help_content_sk_box_debug))
                )
            ),
            HelpCategory(
                getString(R.string.help_common_help_title),
                listOf(
                    HelpTopic(getString(R.string.help_common_help_title), getString(R.string.help_common_help_content))
                )
            ),
            HelpCategory(
                getString(R.string.help_about_title),
                listOf(
                    HelpTopic(getString(R.string.help_about_title), getString(R.string.help_about_content))
                )
            )
        )

        rv.adapter = CategoryAdapter(categories) { category ->
            showTopicSelection(category)
        }
    }

    private fun showTopicSelection(category: HelpCategory) {
        if (category.topics.size == 1) {
            openDetail(category.topics[0])
            return
        }

        val topicNames = category.topics.map { it.title }.toTypedArray()
        AlertDialog.Builder(this)
            .setTitle(category.name)
            .setItems(topicNames) { _, which ->
                openDetail(category.topics[which])
            }
            .show()
    }

    private fun openDetail(topic: HelpTopic) {
        val intent = Intent(this, HelpDetailActivity::class.java).apply {
            putExtra("TITLE", topic.title)
            putExtra("CONTENT", topic.content)
        }
        startActivity(intent)
    }

    data class HelpCategory(val name: String, val topics: List<HelpTopic>)
    data class HelpTopic(val title: String, val content: String)

    inner class CategoryAdapter(
        private val categories: List<HelpCategory>,
        private val onClick: (HelpCategory) -> Unit
    ) : RecyclerView.Adapter<CategoryAdapter.ViewHolder>() {

        inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val tvName: TextView = view.findViewById(R.id.tv_category_name)
            val tvTopics: TextView = view.findViewById(R.id.tv_category_topics)
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.item_help_category, parent, false)
            return ViewHolder(view)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val category = categories[position]
            holder.tvName.text = category.name
            holder.tvTopics.text = category.topics.joinToString(", ") { it.title }
            holder.itemView.setOnClickListener { onClick(category) }
        }

        override fun getItemCount() = categories.size
    }
}
