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

    external fun unload()

    external fun shutdown()

    external fun generate(
        prompt: String,
        maxTokens: Int
    ): String
}
