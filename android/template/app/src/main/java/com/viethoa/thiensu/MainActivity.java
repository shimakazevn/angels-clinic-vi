package com.viethoa.thiensu;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.webkit.WebViewAssetLoader;

import java.io.IOException;
import java.io.InputStream;
import java.net.URLDecoder;

public class MainActivity extends Activity {

    private static final String TAG = "ThienSuGame";
    private WebView mWebView;

    private void hideSystemUI() {
        try {
            Window window = getWindow();
            if (window != null) {
                View decorView = window.getDecorView();
                if (decorView != null) {
                    decorView.setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                    );
                }
            }
        } catch (Exception e) {
            Log.w(TAG, "hideSystemUI warning: " + e.getMessage());
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE);
        } catch (Exception ignored) {}

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            WindowManager.LayoutParams lp = getWindow().getAttributes();
            lp.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            getWindow().setAttributes(lp);
        }

        mWebView = new WebView(this);
        mWebView.setBackgroundColor(Color.BLACK);
        mWebView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        mWebView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        setContentView(mWebView);

        mWebView.post(new Runnable() {
            @Override
            public void run() {
                hideSystemUI();
            }
        });


        WebSettings settings = mWebView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        // Fullscreen viewport settings
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(false);

        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        mWebView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage cm) {
                String msg = cm.message() + " -- From line " + cm.lineNumber() + " of " + cm.sourceId();
                switch (cm.messageLevel()) {
                    case ERROR:
                        Log.e(TAG, "[JS] " + msg);
                        break;
                    case WARNING:
                        Log.w(TAG, "[JS] " + msg);
                        break;
                    default:
                        Log.d(TAG, "[JS] " + msg);
                        break;
                }
                return true;
            }
        });

        final WebViewAssetLoader assetLoader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        mWebView.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri url = request.getUrl();
                String path = url.getPath();
                if (path != null) {
                    try {
                        String rawPath = URLDecoder.decode(path, "UTF-8");
                        String assetPath = rawPath.startsWith("/assets/") ? rawPath.substring(8) : (rawPath.startsWith("/") ? rawPath.substring(1) : rawPath);
                        
                        String mimeType = null;
                        if (rawPath.endsWith(".wasm")) mimeType = "application/wasm";
                        else if (rawPath.endsWith(".png")) mimeType = "image/png";
                        else if (rawPath.endsWith(".jpg") || rawPath.endsWith(".jpeg")) mimeType = "image/jpeg";
                        else if (rawPath.endsWith(".ogg")) mimeType = "audio/ogg";
                        else if (rawPath.endsWith(".m4a")) mimeType = "audio/mp4";
                        else if (rawPath.endsWith(".json")) mimeType = "application/json";
                        else if (rawPath.endsWith(".js")) mimeType = "application/javascript";
                        else if (rawPath.endsWith(".css")) mimeType = "text/css";
                        else if (rawPath.endsWith(".html")) mimeType = "text/html";

                        if (mimeType != null) {
                            try {
                                InputStream is = getAssets().open(assetPath);
                                return new WebResourceResponse(mimeType, "UTF-8", is);
                            } catch (IOException ignored) {}
                        }
                    } catch (Exception ignored) {}
                }
                return assetLoader.shouldInterceptRequest(request.getUrl());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        mWebView.loadUrl("https://appassets.androidplatform.net/assets/index.html");
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            hideSystemUI();
        }
    }

    /**
     * Nút Back Android: Đóng vai trò nút Hủy / Quay lại (Escape / Cancel) trong game,
     * giúp người chơi thoát các menu, bảng lưu game, danh sách tùy chọn...
     * Muốn thoát ứng dụng, người chơi mở đa nhiệm (Recents / Task switcher) để đóng app.
     */
    @Override
    public void onBackPressed() {
        if (mWebView != null) {
            mWebView.evaluateJavascript(
                "(function() {" +
                "    if (window.TouchInput && typeof TouchInput._onCancel === 'function') {" +
                "        TouchInput._newState.cancelled = true;" +
                "    }" +
                "    if (window.Input && typeof Input.virtualClick === 'function') {" +
                "        Input.virtualClick('cancel');" +
                "        Input.virtualClick('escape');" +
                "    }" +
                "    const evtDown = new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, which: 27, code: 'Escape', bubbles: true });" +
                "    const evtUp = new KeyboardEvent('keyup', { key: 'Escape', keyCode: 27, which: 27, code: 'Escape', bubbles: true });" +
                "    document.dispatchEvent(evtDown);" +
                "    setTimeout(function() { document.dispatchEvent(evtUp); }, 50);" +
                "})();",
                null
            );
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        hideSystemUI();
        if (mWebView != null) {
            mWebView.onResume();
            mWebView.resumeTimers();
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            hideSystemUI();
        }
    }


    @Override
    protected void onPause() {
        super.onPause();
        if (mWebView != null) {
            mWebView.onPause();
            mWebView.pauseTimers();
        }
    }

    @Override
    protected void onDestroy() {
        if (mWebView != null) {
            mWebView.destroy();
        }
        super.onDestroy();
    }
}
