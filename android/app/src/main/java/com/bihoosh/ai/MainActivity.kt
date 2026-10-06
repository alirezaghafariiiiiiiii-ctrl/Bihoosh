package com.bihoosh.ai

import android.app.Activity
import android.os.Bundle
import android.content.Intent
import android.net.Uri
import android.provider.OpenableColumns
import android.graphics.Color
import android.view.Gravity
import android.widget.*
import java.io.File

class MainActivity : Activity() {

    private lateinit var engine: InferenceEngine

    private lateinit var chatBox: LinearLayout
    private lateinit var input: EditText
    private lateinit var status: TextView

    private var modelLoaded = false

    companion object {
        private const val PICK_MODEL = 1001
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        engine = InferenceEngine(this)

        buildUI()
    }

    private fun buildUI() {

        val root = LinearLayout(this)

        root.orientation = LinearLayout.VERTICAL
        root.setPadding(20, 35, 20, 20)
        root.setBackgroundColor(
            Color.rgb(12, 14, 16)
        )

        val title = TextView(this)

        title.text = "👾 بی‌هوش"
        title.textSize = 28f
        title.setTextColor(Color.WHITE)
        title.gravity = Gravity.CENTER

        root.addView(
            title,
            LinearLayout.LayoutParams(
                -1,
                70
            )
        )

        status = TextView(this)

        status.text =
            "● هسته مستقل آماده\n" +
            "مدل محلی هنوز بارگذاری نشده"

        status.textSize = 15f
        status.setTextColor(
            Color.rgb(160, 220, 160)
        )
        status.gravity = Gravity.CENTER

        root.addView(
            status,
            LinearLayout.LayoutParams(
                -1,
                70
            )
        )

        val modelButton = Button(this)

        modelButton.text =
            "📁 انتخاب مدل GGUF"

        modelButton.setOnClickListener {
            selectModel()
        }

        root.addView(
            modelButton,
            LinearLayout.LayoutParams(
                -1,
                55
            )
        )

        val scroll = ScrollView(this)

        chatBox = LinearLayout(this)

        chatBox.orientation =
            LinearLayout.VERTICAL

        chatBox.setPadding(
            5,
            20,
            5,
            20
        )

        scroll.addView(chatBox)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(
                -1,
                0,
                1f
            )
        )

        val bottom = LinearLayout(this)

        bottom.orientation =
            LinearLayout.HORIZONTAL

        input = EditText(this)

        input.hint =
            "پیامت را بنویس..."

        input.setTextColor(Color.WHITE)
        input.setHintTextColor(
            Color.GRAY
        )

        bottom.addView(
            input,
            LinearLayout.LayoutParams(
                0,
                60,
                1f
            )
        )

        val send = Button(this)

        send.text = "ارسال"

        send.setOnClickListener {
            sendMessage()
        }

        bottom.addView(
            send,
            LinearLayout.LayoutParams(
                110,
                60
            )
        )

        root.addView(bottom)

        setContentView(root)
    }

    private fun selectModel() {

        val intent =
            Intent(Intent.ACTION_OPEN_DOCUMENT)

        intent.addCategory(
            Intent.CATEGORY_OPENABLE
        )

        intent.type =
            "application/octet-stream"

        startActivityForResult(
            intent,
            PICK_MODEL
        )
    }

    override fun onActivityResult(
        requestCode: Int,
        resultCode: Int,
        data: Intent?
    ) {
        super.onActivityResult(
            requestCode,
            resultCode,
            data
        )

        if (
            requestCode != PICK_MODEL ||
            resultCode != RESULT_OK ||
            data?.data == null
        ) {
            return
        }

        val uri = data.data!!

        copyModel(uri)
    }

    private fun copyModel(uri: Uri) {

        status.text =
            "⏳ در حال کپی کردن مدل..."

        Thread {

            try {

                val modelFile =
                    File(
                        filesDir,
                        "model.gguf"
                    )

                contentResolver
                    .openInputStream(uri)
                    .use { input ->

                        modelFile.outputStream()
                            .use { output ->

                            input?.copyTo(
                                output
                            )
                        }
                    }

                runOnUiThread {

                    status.text =
                        "⏳ مدل کپی شد؛ در حال بارگذاری..."

                }

                engine.loadModel(
                    modelFile.absolutePath
                ) { success, message ->

                    runOnUiThread {

                        if (success) {

                            modelLoaded = true

                            status.text =
                                "● مدل محلی آماده است"

                            addMessage(
                                "بی‌هوش",
                                "مدل محلی با موفقیت آماده شد 👾"
                            )

                        } else {

                            status.text =
                                "✖ خطا در بارگذاری مدل"

                            addMessage(
                                "خطا",
                                message
                            )
                        }
                    }
                }

            } catch (e: Exception) {

                runOnUiThread {

                    status.text =
                        "✖ خطا در خواندن مدل"

                    addMessage(
                        "خطا",
                        e.message ?: "خطای ناشناخته"
                    )
                }
            }
        }.start()
    }

    private fun sendMessage() {

        val message =
            input.text
                .toString()
                .trim()

        if (message.isEmpty()) {
            return
        }

        addMessage(
            "شما",
            message
        )

        input.text = ""

        if (!modelLoaded) {

            addMessage(
                "بی‌هوش",
                "اول یک مدل GGUF انتخاب کن."
            )

            return
        }

        addMessage(
            "بی‌هوش",
            "..."
        )

        engine.ask(
            message = message,
            predictLength = 512,

            onToken = { token ->

                runOnUiThread {

                    appendToLastMessage(
                        token
                    )
                }
            },

            onFinished = {
                runOnUiThread {
                    status.text =
                        "● آماده"
                }
            },

            onError = { error ->

                runOnUiThread {

                    status.text =
                        "✖ خطای مدل"

                    appendToLastMessage(
                        "\n$error"
                    )
                }
            }
        )
    }

    private fun addMessage(
        sender: String,
        message: String
    ) {

        val text = TextView(this)

        text.text =
            "$sender:\n$message"

        text.textSize = 17f
        text.setTextColor(Color.WHITE)

        text.setPadding(
            18,
            14,
            18,
            14
        )

        chatBox.addView(text)

        chatBox.post {
            (chatBox.parent as ScrollView)
                .fullScroll(
                    ScrollView.FOCUS_DOWN
                )
        }
    }

    private fun appendToLastMessage(
        text: String
    ) {

        if (chatBox.childCount == 0) {
            return
        }

        val last =
            chatBox.getChildAt(
                chatBox.childCount - 1
            ) as TextView

        last.append(text)

        chatBox.post {
            (chatBox.parent as ScrollView)
                .fullScroll(
                    ScrollView.FOCUS_DOWN
                )
        }
    }

    override fun onDestroy() {

        try {
            engine.destroy()
        } catch (_: Exception) {
        }

        super.onDestroy()
    }
}
