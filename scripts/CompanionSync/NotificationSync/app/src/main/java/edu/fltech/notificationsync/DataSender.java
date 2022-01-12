package edu.fltech.notificationsync;
import android.app.IntentService;
import android.content.Intent;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class DataSender extends IntentService {

    private Socket socket;
    private void connect() {
        while (socket == null || !socket.isConnected()) {
            try {
                socket = new Socket("192.168.2.100", 8765);
            } catch (IOException e) {
                e.printStackTrace();
                socket = null;
                try {
                    Thread.sleep(500); // I'm trash.
                } catch (InterruptedException f) {
                    f.printStackTrace();
                }
            }
        }
    }
    public DataSender() {
        super("DataSender");
    }
    @Override
    protected void onHandleIntent(Intent data) {
        while (true)
            try {
                connect();
                OutputStream write = null;
                write = socket.getOutputStream();
                write.write(data.getStringExtra("data").getBytes(StandardCharsets.US_ASCII));
                write.flush();
                write.close();
                socket.close();

                break;
            } catch (IOException e) {
                e.printStackTrace();
                socket = null;
            }
    }
}
