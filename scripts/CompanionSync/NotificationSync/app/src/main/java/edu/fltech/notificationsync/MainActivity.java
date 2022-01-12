package edu.fltech.notificationsync;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Context appContext = getApplicationContext();
        if (!notificationEnabled(appContext)) {
            Intent intent = new Intent(
                    "android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS");
            startActivity(intent);
        }
    }

    private boolean notificationEnabled(Context ctx) {
        String listeners = Settings.Secure.getString(ctx.getContentResolver(), "enabled_notification_listeners");
        if (listeners == null) return false;
        return listeners.contains(new ComponentName(ctx, NotificationService.class).flattenToString());
    }
}