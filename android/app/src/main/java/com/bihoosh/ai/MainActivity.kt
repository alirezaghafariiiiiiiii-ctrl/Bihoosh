package com.bihoosh.ai

import android.app.Activity
import android.os.Bundle
import android.widget.LinearLayout
import android.widget.TextView
import android.graphics.Color
import android.view.Gravity

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this)

        root.orientation = LinearLayout.VERTICAL
        root.setPadding(32, 48, 32, 32)
        root.setBackgroundColor(Color.rgb(15, 15, 18))

        val title = TextView(this)

        title.text = "👾 بی‌هوش"
        title.textSize = 28f
        title.setTextColor(Color.WHITE)
        title.gravity = Gravity.CENTER

        root.addView(
            title,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                80
            )
        )

        val status = TextView(this)

        status.text =
            "هسته مستقل آماده است\n\n" +
            "مدل زبانی محلی هنوز متصل نشده."

        status.textSize = 18f
        status.setTextColor(Color.LTGRAY)
        status.gravity = Gravity.CENTER

        root.addView(
            status,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        setContentView(root)
    }
}
