import UIKit
import WebKit

class ViewController: UIViewController, WKNavigationDelegate, WKUIDelegate {

    private var webView: WKWebView!

    override var prefersStatusBarHidden: Bool {
        return true
    }

    override var prefersHomeIndicatorAutoHidden: Bool {
        return true
    }

    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        return .landscape
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.backgroundColor = .black

        setupWebView()
        setupGestures()
        loadGame()
    }

    private func setupWebView() {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        config.suppressesIncrementalRendering = false

        // Enable universal local file access to load sound, images and scripts smoothly
        let preferences = WKWebpagePreferences()
        preferences.allowsContentJavaScript = true
        config.defaultWebpagePreferences = preferences
        config.setValue(true, forKey: "allowUniversalAccessFromFileURLs")

        // Unlock WebAudio on first touch & inject high refresh rate
        let audioUnlockScript = WKUserScript(
            source: """
            (function() {
                function unlockAudio() {
                    if (typeof WebAudio !== 'undefined' && WebAudio._context && WebAudio._context.state === 'suspended') {
                        WebAudio._context.resume();
                    }
                    if (typeof AudioManager !== 'undefined' && AudioManager.resumeAudioContext) {
                        AudioManager.resumeAudioContext();
                    }
                    window.removeEventListener('touchstart', unlockAudio, true);
                    window.removeEventListener('touchend', unlockAudio, true);
                    window.removeEventListener('click', unlockAudio, true);
                }
                window.addEventListener('touchstart', unlockAudio, true);
                window.addEventListener('touchend', unlockAudio, true);
                window.addEventListener('click', unlockAudio, true);
            })();
            """,
            injectionTime: .atDocumentEnd,
            forMainFrameOnly: false
        )
        config.userContentController.addUserScript(audioUnlockScript)

        webView = WKWebView(frame: self.view.bounds, configuration: config)
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        webView.navigationDelegate = self
        webView.uiDelegate = self
        webView.isOpaque = false
        webView.backgroundColor = .black
        webView.scrollView.backgroundColor = .black
        webView.scrollView.isScrollEnabled = false
        webView.scrollView.bounces = false
        webView.scrollView.contentInsetAdjustmentBehavior = .never

        self.view.addSubview(webView)
    }

    private func setupGestures() {
        // Two-finger tap triggers in-game Cancel / Escape
        let twoFingerTap = UITapGestureRecognizer(target: self, action: #selector(handleTwoFingerTap))
        twoFingerTap.numberOfTouchesRequired = 2
        twoFingerTap.cancelsTouchesInView = false
        self.view.addGestureRecognizer(twoFingerTap)
    }

    @objc private func handleTwoFingerTap() {
        let js = """
        if (typeof Input !== 'undefined' && typeof Input.virtualClick === 'function') {
            Input.virtualClick('cancel');
        } else {
            const event = new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', keyCode: 27, which: 27, bubbles: true });
            document.dispatchEvent(event);
        }
        """
        webView.evaluateJavaScript(js, completionHandler: nil)
    }

    private func loadGame() {
        guard let resourceURL = Bundle.main.resourceURL else {
            print("Resource URL not found")
            return
        }

        let wwwURL = resourceURL.appendingPathComponent("www")
        let indexURL = wwwURL.appendingPathComponent("index.html")

        if FileManager.default.fileExists(atPath: indexURL.path) {
            webView.loadFileURL(indexURL, allowingReadAccessTo: wwwURL)
        } else {
            // Fallback placeholder message if game is not yet injected
            let html = """
            <!DOCTYPE html>
            <html>
            <head><meta charset="utf-8"><title>Thien Su Clinic</title>
            <style>
            body { background: #121212; color: #ffffff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; text-align: center; }
            h1 { font-size: 28px; color: #4fc3f7; }
            p { font-size: 16px; color: #e0e0e0; }
            </style>
            </head>
            <body>
            <div>
            <h1>Thien Su Clinic iOS Shell</h1>
            <p>Vỏ ứng dụng đã sẵn sàng! Vui lòng dùng script tiêm dữ liệu game vào file IPA.</p>
            </div>
            </body>
            </html>
            """
            webView.loadHTMLString(html, baseURL: nil)
        }
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        print("Game Loaded Successfully")
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("Navigation error: \(error.localizedDescription)")
    }
}
