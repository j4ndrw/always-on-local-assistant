package com.j4ndrw.audiomanager;

import android.content.Context;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "AudioManager")
public class AudioManagerPlugin extends Plugin {
    private final AudioManagerImplementation implementation = new AudioManagerImplementation();

    @PluginMethod
    public void muteNotifications(PluginCall call) {
        Context context = getContext();
        implementation.muteNotifications(context);
        call.resolve();
    }

    @PluginMethod
    public void unmuteNotifications(PluginCall call) {
        Context context = getContext();
        implementation.unmuteNotifications(context);
        call.resolve();
    }
}
