package edu.fltech.notificationsync;
import android.app.Notification;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.json.JSONException;
import org.json.JSONObject;
public class NotificationService extends NotificationListenerService {
    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        String pack = sbn.getPackageName();
        Notification obj = sbn.getNotification();
        Bundle extras = obj.extras;
        Date formatted = new java.util.Date(obj.when);
        JSONObject output = new JSONObject();
        try {
            output.put("package", pack);
            if (obj.tickerText != null)
                output.put("accessibilityText", obj.tickerText.toString());
            if (extras.containsKey("android.title"))
                output.put("title", extras.getString("android.title"));
            CharSequence text = extras.getCharSequence("android.text");
            if (text != null) // ring notifications threw errors without check, and containsKey failed to save me
                output.put("text", text.toString());
            output.put("date",new SimpleDateFormat("MMMM dd, yyyy 'at' hh:mm:ssaa").format(formatted).toString()); // might move to server and just send unix ts
        } catch (JSONException e) {
            e.printStackTrace();
        }
        cancelNotification(sbn.getKey());
        Intent msgSend = new Intent(this, DataSender.class);
        msgSend.putExtra("data", output.toString());
        startService(msgSend);
    }
}
