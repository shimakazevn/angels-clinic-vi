package com.viethoa.thiensu;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.webkit.WebViewAssetLoader;

public class MainActivity extends Activity {

    private static final String TAG = "ThienSuGame";
    private WebView mWebView;
    private long mBackPressedTime = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Fullscreen Sticky Immersive Mode
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        );

        // Enable WebView remote debugging via chrome://inspect (debug only)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        mWebView = new WebView(this);
        setContentView(mWebView);

        WebSettings settings = mWebView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        // Viewport / layout settings (important for PIXI.js canvas sizing)
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setAllowFileAccess(true);

        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        // Hardware acceleration is set at window level; LAYER_TYPE_HARDWARE
        // enables GPU compositing for WebGL. Do NOT use LAYER_TYPE_SOFTWARE
        // as it disables WebGL entirely.
        mWebView.setLayerType(View.LAYER_TYPE_HARDWARE, null);

        // WebChromeClient is REQUIRED for WebGL to work in Android WebView.
        // Without it the GL surface is never created and PIXI.js renders nothing
        // (audio still works because Web Audio API is independent of WebGL).
        mWebView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage cm) {
                // Forward all JS console output to Android logcat for debugging
                String level = cm.messageLevel().name();
                String msg = cm.message() + " -- From line " + cm.lineNumber()
                        + " of " + cm.sourceId();
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

        // Asset loader bypasses CORS & file:// restrictions on Android 11+
        final WebViewAssetLoader assetLoader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        mWebView.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return assetLoader.shouldInterceptRequest(request.getUrl());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        // Load game safely over virtual https domain
        mWebView.loadUrl("https://appassets.androidplatform.net/assets/index.html");
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
