package com.j4ndrw.frontendcapabilities;

import android.Manifest;
import android.content.ContentResolver;
import android.content.Context;
import android.database.Cursor;
import android.provider.Contacts;
import android.provider.ContactsContract;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;

import java.util.HashMap;

@CapacitorPlugin(name = "FrontendCapabilities", permissions = { @Permission(strings = { Manifest.permission.READ_CONTACTS }) })
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
