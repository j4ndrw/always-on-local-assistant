package com.j4ndrw.lola;

import android.os.Bundle;

import com.getcapacitor.BridgeActivity;
import com.j4ndrw.audiomanager.AudioManagerPlugin;
import com.j4ndrw.frontendcapabilities.FrontendCapabilitiesPlugin;
import com.j4ndrw.stt.STTPlugin;
import com.j4ndrw.applauncher.AppLauncherPlugin;

public class MainActivity extends BridgeActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    registerPlugin(AudioManagerPlugin.class);
    registerPlugin(STTPlugin.class);
    registerPlugin(FrontendCapabilitiesPlugin.class);
    registerPlugin(AppLauncherPlugin.class);
    super.onCreate(savedInstanceState);
  }
}
