package com.j4ndrw.frontendcapabilities;

import android.content.Context;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "FrontendCapabilities")
public class FrontendCapabilitiesPlugin extends Plugin {
    private final FrontendCapabilitiesImplementation implementation = new FrontendCapabilitiesImplementation();

    @PluginMethod
    public void getInstalledApps(PluginCall call) {
        Context context = getContext();
        JSArray arr = new JSArray();
        for (String packageName : implementation.getInstalledApps(context)) {
            arr.put(packageName);
        }
        JSObject ret = new JSObject();
        ret.put("installedApps", arr);
        call.resolve(ret);
    }
}
