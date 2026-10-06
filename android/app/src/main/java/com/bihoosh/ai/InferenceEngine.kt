package com.bihoosh.ai

import android.content.Context
import com.arm.aichat.internal.InferenceEngineImpl
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class InferenceEngine(context: Context) {

    private val nativeEngine = InferenceEngineImpl()

    private val executor: ExecutorService =
        Executors.newSingleThreadExecutor()

    init {
        nativeEngine.init(
            context.applicationInfo.nativeLibraryDir
        )
    }

    fun loadModel(
        modelPath: String,
        onResult: (Boolean, String) -> Unit
    ) {
        executor.execute {

            try {
                val result = nativeEngine.load(modelPath)

                if (result == 0) {
                    val prepareResult =
                        nativeEngine.prepare()

                    if (prepareResult == 0) {
                        onResult(
                            true,
                            "مدل با موفقیت بارگذاری شد."
                        )
                    } else {
                        onResult(
                            false,
                            "خطا در آماده‌سازی مدل."
                        )
                    }
                } else {
                    onResult(
                        false,
                        "خطا در بارگذاری مدل."
                    )
                }

            } catch (e: Exception) {

                onResult(
                    false,
                    "خطای موتور:\n${e.message}"
                )
            }
        }
    }

    fun setSystemPrompt(prompt: String) {

        executor.execute {

            nativeEngine.processSystemPrompt(
                prompt
            )
        }
    }

    fun ask(
        message: String,
        predictLength: Int = 512,
        onToken: (String) -> Unit,
        onFinished: () -> Unit,
        onError: (String) -> Unit
    ) {

        executor.execute {

            try {

                val result =
                    nativeEngine.processUserPrompt(
                        message,
                        predictLength
                    )

                if (result != 0) {
                    onError(
                        "خطا در ارسال پیام به مدل."
                    )
                    return@execute
                }

                while (true) {

                    val token =
                        nativeEngine.generateNextToken()

                    if (token == null) {
                        break
                    }

                    if (token.isNotEmpty()) {
                        onToken(token)
                    }
                }

                onFinished()

            } catch (e: Exception) {

                onError(
                    "خطا در اجرای مدل:\n${e.message}"
                )
            }
        }
    }

    fun systemInfo(): String {

        return try {
            nativeEngine.systemInfo()
        } catch (e: Exception) {
            "اطلاعات موتور در دسترس نیست."
        }
    }

    fun close() {

        executor.execute {

            try {
                nativeEngine.unload()
            } catch (_: Exception) {
            }
        }
    }

    fun destroy() {

        executor.execute {

            try {
                nativeEngine.shutdown()
            } catch (_: Exception) {
            }

            executor.shutdown()
        }
    }
}
