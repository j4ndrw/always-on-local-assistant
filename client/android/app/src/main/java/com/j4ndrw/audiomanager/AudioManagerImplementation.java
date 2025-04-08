package com.j4ndrw.audiomanager;

import android.annotation.SuppressLint;
import android.content.Context;
import android.media.AudioManager;

public class AudioManagerImplementation {
    public void muteNotifications(Context context) {
        @SuppressLint("ServiceCast") AudioManager audioManager= (AudioManager) context.getSystemService(Context.AUDIO_SERVICE);
        audioManager.adjustStreamVolume(AudioManager.STREAM_NOTIFICATION, AudioManager.ADJUST_UNMUTE, 0);
    }
    public void unmuteNotifications(Context context) {
        @SuppressLint("ServiceCast") AudioManager audioManager=(AudioManager)context.getSystemService(Context.AUDIO_SERVICE);
        audioManager.adjustStreamVolume(AudioManager.STREAM_NOTIFICATION, AudioManager.ADJUST_MUTE, 0);
    }
}
