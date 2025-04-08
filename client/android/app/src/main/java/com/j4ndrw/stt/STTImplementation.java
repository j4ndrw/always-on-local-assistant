package com.j4ndrw.stt;

import android.content.Context;
import android.content.res.AssetManager;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import org.vosk.Model;
import org.vosk.Recognizer;
import org.vosk.android.SpeechService;
import org.vosk.android.RecognitionListener;
import org.vosk.android.StorageService;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;


public class STTImplementation implements RecognitionListener {
    public final float SAMPLE_RATE = 16000.0f;

    private Model model;
    private SpeechService speechService;
    private boolean isListening = false;
    private final StringBuilder partialResults = new StringBuilder();
    private String finalResult = "";

    public void initializeModel(Context context) {
        try {
            Executor executor = Executors.newSingleThreadExecutor(); // change according to your requirements
            Handler handler = new Handler(Looper.getMainLooper());
            executor.execute(() -> {
                try {
                    // This is needed because the Vosk API looks for the model in the external data of the application
                    // (e.g. /storage/emulated/0/Android/com.j4ndrw.lola), not the internal assets
                    String path = StorageService.sync(context, "public/vosk/model", "generated");
                    Model model = new Model(path);
                    handler.post(() -> {
                        this.model = model;
                        Log.d("Vosk", "Model load successfully");
                    });
                } catch (final IOException e) {
                    handler.post(() -> {
                        throw new RuntimeException("Error no model:" + e.getMessage());
                    });
                }
            });
        } catch (Exception e) {
            throw new RuntimeException("Could not initialize speech-to-text model" + e.getMessage());
        }
    }

    public void startListening(RecognitionListener listener) throws IOException {
        if (model == null) {
            throw new RuntimeException("Could not initialize speech-to-text model");
        }

        Recognizer recognizer = new Recognizer(model, SAMPLE_RATE);
        speechService = new SpeechService(recognizer, SAMPLE_RATE);
        speechService.startListening(listener);
        isListening = true;
    }

    public void stopListening() {
        if (speechService != null) {
            speechService.stop();
            isListening = false;
        }
    }

    public void pause(boolean checked) {
        if (speechService != null) {
            speechService.setPause(checked);
            isListening = checked;
        }
    }

    public void reset() {
        if (speechService != null) {
            speechService.reset();
        }
    }

    @Override
    public void onPartialResult(String hypothesis) {
        if (hypothesis != null && !hypothesis.isEmpty()) {
            partialResults.append(hypothesis).append(" ");
        }
    }

    @Override
    public void onResult(String hypothesis) {
        finalResult = hypothesis;
    }

    @Override
    public void onFinalResult(String hypothesis) {
        finalResult = hypothesis;
    }

    @Override
    public void onError(Exception exception) {
        Log.e("Vosk", "Error on speech recognition" + exception.getMessage());
    }

    @Override
    public void onTimeout() {
        Log.e("Vosk", "Expired");
    }

    public boolean isListening() {
        return isListening;
    }
}
