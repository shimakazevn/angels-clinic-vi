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
import android.view.WindowInsets;
import android.view.WindowInsetsController;
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
    private long mBackPressedTime = 0;

    private void hideSystemUI() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Window window = getWindow();
            if (window != null) {
                window.setDecorFitsSystemWindows(false);
                WindowInsetsController controller = window.getInsetsController();
                if (controller != null) {
                    controller.hide(WindowInsets.Type.statusBars() | WindowInsets.Type.navigationBars());
                    controller.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
                }
            }
        } else {
            View decorView = getWindow().getDecorView();
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Lock to landscape
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        hideSystemUI();

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        mWebView = new WebView(this);
        mWebView.setBackgroundColor(Color.BLACK);
        mWebView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        mWebView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        setContentView(mWebView);

        WebSettings settings = mWebView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        // TRUE Device-Width Viewport for 100% Fullscreen
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(false);

        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

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

    @Override
    public void onBackPressed() {
        if (mWebView != null && mWebView.canGoBack()) {
            mWebView.goBack();
        } else {
            if (mBackPressedTime + 2000 > System.currentTimeMillis()) {
                super.onBackPressed();
            } else {
                android.widget.Toast.makeText(
                    this,
                    "Nhan Back mot lan nua de thoat",
                    android.widget.Toast.LENGTH_SHORT
                ).show();
                mBackPressedTime = System.currentTimeMillis();
            }
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
