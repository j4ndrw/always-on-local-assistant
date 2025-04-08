package com.j4ndrw.frontendcapabilities;

import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class FrontendCapabilitiesImplementation {
    public List<String> getInstalledApps(Context context) {
        final PackageManager pm = context.getPackageManager();
        List<ApplicationInfo> installedApps = pm.getInstalledApplications(PackageManager.GET_META_DATA);
        List<String> visiblePackageNames = new ArrayList<>();

        Set<String> queryPackages = new HashSet<>();
        queryPackages.add("com.google.android.youtube");
        queryPackages.add("ro.jerryspizza.android");
        queryPackages.add("com.chucklefish.stardewvalley");
        queryPackages.add("com.whatsapp");
        queryPackages.add("com.github.android");
        queryPackages.add("com.reddit.frontpage");
        queryPackages.add("com.brave.browser");
        queryPackages.add("com.microsoft.office.outlook");
        queryPackages.add("com.google.android.apps.maps");
        queryPackages.add("com.bolt.deliveryclient");
        queryPackages.add("com.google.android.contacts");
        queryPackages.add("com.android.chrome");
        queryPackages.add("ee.dustland.android.minesweeper");
        queryPackages.add("com.netflix.mediaclient");
        queryPackages.add("com.spotify.music");
        queryPackages.add("com.humble.SlayTheSpire");
        queryPackages.add("com.valvesoftware.android.steam.community");
        queryPackages.add("com.Slack");
        queryPackages.add("com.glovo");
        queryPackages.add("org.mozilla.firefox");
        queryPackages.add("com.google.android.apps.youtube.music");
        queryPackages.add("com.google.android.play.games");
        queryPackages.add("com.valvesoftware.steamlink");
        queryPackages.add("notion.id");
        queryPackages.add("com.lego.legobuildinginstructions");
        queryPackages.add("com.disney.disneyplus");
        queryPackages.add("com.microsoft.teams");

        for (ApplicationInfo appInfo : installedApps) {
            if (queryPackages.contains(appInfo.packageName)) {
                visiblePackageNames.add(appInfo.packageName);
            }
        }

        return visiblePackageNames;
    }
}
