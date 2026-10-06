package com.arm.aichat.internal

class InferenceEngineImpl {

    companion object {
        init {
            System.loadLibrary("bihoosh")
        }
    }

    external fun init(nativeLibDir: String)

    external fun load(modelPath: String): Int

    external fun prepare(): Int

    external fun systemInfo(): String

    external fun benchModel(
        pp: Int,
        tg: Int,
        pl: Int,
        nr: Int
    ): String

    external fun processSystemPrompt(
        systemPrompt: String
    ): Int

    external fun processUserPrompt(
        userPrompt: String,
        predictLength: Int
    ): Int

    external fun generateNextToken(): String?

    external fun unload()

    external fun shutdown()
}
