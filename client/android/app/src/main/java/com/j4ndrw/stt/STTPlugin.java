package com.j4ndrw.stt;

import android.Manifest;
import android.content.Context;
import android.speech.SpeechRecognizer;
import android.util.Log;

import com.getcapacitor.JSObject;
import com.getcapacitor.PermissionState;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;

import org.vosk.android.RecognitionListener;

@CapacitorPlugin(name = "STT", permissions = { @Permission(strings = { Manifest.permission.RECORD_AUDIO }) })
public class STTPlugin extends Plugin {
    private final STTImplementation STTImplementation = new STTImplementation();

    @PluginMethod
    public void initializeModel(PluginCall call) {
        Context context = getContext();
        try {
            STTImplementation.initializeModel(context);
            call.resolve();
        } catch (RuntimeException e) {
            call.reject("Failed to initialize model: " + e.getMessage());
        }
    }

    @PluginMethod
    public void available(PluginCall call) {
        boolean val = isSpeechRecognitionAvailable();
        JSObject result = new JSObject();
        result.put("available", val);
        call.resolve(result);
    }

    private boolean isSpeechRecognitionAvailable() {
        Context context = getContext();
        return SpeechRecognizer.isRecognitionAvailable(context);
    }

    @PluginMethod
    public void startListening(PluginCall call) {
        try {
            if (!isSpeechRecognitionAvailable()) {
                call.unavailable("Speech recognition service is not available.");
                return;

            }
            if (getPermissionState("speechRecognition") == PermissionState.DENIED) {
                call.reject("Speech recognition permission denied");
                return;
            }

            RecognitionListener recognitionListener = new RecognitionListener() {
                @Override
                public void onPartialResult(String hypothesis) {
                    if (hypothesis != null && !hypothesis.isEmpty()) {
                        try {
                            JSObject hypothesisObj = new JSObject(hypothesis);
                            String partialResult = hypothesisObj.getString("partial");

                            JSObject result = new JSObject();
                            result.put("matches", partialResult);

                            notifyListeners("partialResult", result);
                        } catch (Exception e) {
                            call.reject("Failed to process partial result: " + e.getMessage());
                        }
                    }
                }

                @Override
                public void onResult(String hypothesis) {
                    try {
                        JSObject hypothesisObj = new JSObject(hypothesis);
                        String resultText = hypothesisObj.getString("text");

                        JSObject result = new JSObject();
                        result.put("result", resultText);

                        notifyListeners("result", result);
                        Log.d("Vosk", "result: " + result);
                    } catch (Exception e) {
                        call.reject("Failed to process result: " + e.getMessage());
                    }
                }

                /*Called after stream end*/
                @Override
                public void onFinalResult(String hypothesis) {
                    try {
                        JSObject hypothesisObj = new JSObject(hypothesis);
                        String finalText = hypothesisObj.getString("text");

                        JSObject result = new JSObject();
                        result.put("final", finalText);

                        notifyListeners("finalResult", result);
                    } catch (Exception e) {
                        call.reject("Failed to process final result: " + e.getMessage());
                    }
                }

                @Override
                public void onError(Exception exception) {
                    Log.e("Vosk", "Speech recognition error: " + exception.getMessage());
                    call.reject("Speech recognition error: " + exception.getMessage());
                }

                @Override
                public void onTimeout() {
                    Log.e("Vosk", "Speech recognition timed out.");
                    call.reject("Speech recognition timed out.");
                }
            };
            STTImplementation.startListening(recognitionListener);
        } catch (Exception e) {
            call.reject("Failed to start speech recognition: " + e.getMessage());
        }
    }

    @PluginMethod
    public void stopListening(PluginCall call) {
        try {
            STTImplementation.stopListening();
            call.resolve();
        } catch (Exception e) {
            call.reject("Failed to stop speech recognition: " + e.getMessage());
        }
    }

    @PluginMethod
    public void pauseListening(PluginCall call) {
        try {
            STTImplementation.pause(true);
            call.resolve();
        } catch (Exception e) {
            call.reject("Failed to pause speech recognition: " + e.getMessage());
        }
    }

    @PluginMethod
    public void resumeListening(PluginCall call) {
        try {
            STTImplementation.pause(false);
            call.resolve();
        } catch (Exception e) {
            call.reject("Failed to resume speech recognition: " + e.getMessage());
        }
    }

    @PluginMethod
    public void isListening(PluginCall call) {
        boolean isListening = STTImplementation.isListening();
        JSObject ret = new JSObject();
        ret.put("isListening", isListening);
        call.resolve(ret);
    }
}
