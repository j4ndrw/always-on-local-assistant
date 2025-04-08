package com.j4ndrw.applauncher;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.util.Log;

import com.getcapacitor.JSObject;
import com.getcapacitor.Logger;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.util.InternalUtils;

@CapacitorPlugin(name = "AppLauncher")
public class AppLauncherPlugin extends Plugin {

    @PluginMethod
    public void canOpenUrl(PluginCall call) {
        String url = call.getString("url");
        if (url == null) {
            call.reject("Must supply a url");
            return;
        }

        Context ctx = this.getActivity().getApplicationContext();
        final PackageManager pm = ctx.getPackageManager();

        JSObject ret = new JSObject();
        try {
            InternalUtils.getPackageInfo(pm, url, PackageManager.GET_ACTIVITIES);
            ret.put("value", true);
            call.resolve(ret);
            return;
        } catch (PackageManager.NameNotFoundException e) {
            Logger.error(getLogTag(), "Package name '" + url + "' not found!", null);
        }

        ret.put("value", false);
        call.resolve(ret);
    }

    @PluginMethod
    public void openUrl(PluginCall call) {
        String url = call.getString("url");
        if (url == null) {
            call.reject("Must provide a url to open");
            return;
        }

        JSObject ret = new JSObject();
        final PackageManager manager = getContext().getPackageManager();
        Intent launchIntent = manager.getLaunchIntentForPackage(url);
        if (launchIntent == null) {
            ret.put("completed", true);
            call.resolve(ret);
            return;
        }

        launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

        try {
            Log.d("APP LAUNCHER", "Attempting to launch package: " + url);
            getContext().startActivity(launchIntent);
            ret.put("completed", true);
        } catch (Exception ex) {
            ret.put("completed", false);
            Log.d("APP LAUNCHER EXCEPTION - FAILED TO START ACTIVITY: ", ex.getMessage());
        }

        call.resolve(ret);
    }
}
