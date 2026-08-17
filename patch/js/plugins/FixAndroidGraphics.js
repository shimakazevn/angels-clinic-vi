//=============================================================================
// FixAndroidGraphics.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc High Refresh Rate (60-165 FPS), Fullscreen 100% Scaling, WebGL & Effekseer Safety for Android.
 * @author Antigravity
 * @help
 * 1. High Refresh Rate: Unlocks smooth 60 FPS up to 165 FPS (supports 60Hz, 90Hz, 120Hz, 144Hz, 165Hz gaming screens, min 60 FPS).
 * 2. Optimized 1x native WebGL rendering with Hardware-Accelerated CSS scaling.
 * 3. Automatic texture & VRAM garbage collection to prevent memory leaks.
 * 4. Fullscreen responsive scaling for all aspect ratios (16:9, 18:9, 19.5:9, 20:9, tablets).
 * 5. Fixes Android WebView document.hasFocus() freeze.
 * 6. Multi-tier WebGL fallback and Effekseer safety guard.
 */

(() => {
    // 1. Robust WebGL Availability Check
    Utils.canUseWebGL = function() {
        try {
            const canvas = document.createElement("canvas");
            return !!(
                canvas.getContext("webgl2") ||
                canvas.getContext("webgl") ||
                canvas.getContext("experimental-webgl")
            );
        } catch (e) {
            return false;
        }
    };

    // 2. High-Performance PIXI Settings (Min 60 FPS, Max 165 FPS)
    Graphics._setupPixi = function() {
        PIXI.utils.skipHello();
        
        // Auto garbage collection for textures every 600 frames to save VRAM
        PIXI.settings.GC_MAX_IDLE = 600;
        PIXI.settings.GC_MODE = PIXI.GC_MODES.AUTO;
        
        // Linear scale mode for crisp rendering
        PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.LINEAR;
        
        // High Refresh Rate: Min 60 FPS, Max 165 FPS
        if (PIXI.Ticker && PIXI.Ticker.shared) {
            PIXI.Ticker.shared.minFPS = 60;
            PIXI.Ticker.shared.maxFPS = 165;
        }
    };

    // 3. Multi-tier PIXI Application Creation (1x Native Buffer, Hardware Scaled)
    Graphics._createPixiApp = function() {
        this._setupPixi();
        let app = null;

        // Tier 1: Standard High-Performance WebGL
        try {
            app = new PIXI.Application({
                view: this._canvas,
                autoStart: false,
                width: this._width || 1280,
                height: this._height || 720,
                resolution: 1,
                powerPreference: "high-performance",
                antialias: false,
                preserveDrawingBuffer: true
            });
        } catch (e1) {
            console.warn("[FixAndroidGraphics] Tier 1 PIXI init failed, trying Tier 2 fallback...", e1);
        }

        // Tier 2: Safe Mobile WebGL initialization
        if (!app) {
            try {
                app = new PIXI.Application({
                    view: this._canvas,
                    autoStart: false,
                    failIfMajorPerformanceCaveat: false,
                    antialias: false,
                    resolution: 1,
                    preserveDrawingBuffer: true
                });
            } catch (e2) {
                console.warn("[FixAndroidGraphics] Tier 2 PIXI init failed, trying Tier 3 fallback...", e2);
            }
        }

        // Tier 3: Minimal fallback
        if (!app) {
            try {
                app = new PIXI.Application({
                    view: this._canvas,
                    autoStart: false,
                    antialias: false
                });
            } catch (e3) {
                console.error("[FixAndroidGraphics] All PIXI initialization tiers failed.", e3);
                app = null;
            }
        }

        if (app) {
            this._app = app;
            this._app.ticker.remove(this._app.render, this._app);
            this._app.ticker.add(this._onTick, this);
            if (this._app.ticker) {
                this._app.ticker.minFPS = 60;
                this._app.ticker.maxFPS = 165;
            }
        } else {
            this._app = null;
        }
    };

    // 4. Safe Effekseer Context creation
    Graphics._createEffekseerContext = function() {
        this._effekseer = null;
        if (this._app && window.effekseer && typeof effekseer.createContext === "function") {
            try {
                const gl = this._app.renderer ? this._app.renderer.gl : null;
                if (gl) {
                    const ctx = effekseer.createContext();
                    if (ctx) {
                        ctx.init(gl);
                        ctx.setRestorationOfStatesFlag(false);
                        this._effekseer = ctx;
                    }
                }
            } catch (e) {
                console.warn("[FixAndroidGraphics] Effekseer WebGL initialization skipped on this device/WebView:", e);
                this._effekseer = null;
            }
        }
    };

    // 5. Safe Sprite_Animation hooks when Effekseer is unavailable
    const _Sprite_Animation_render = Sprite_Animation.prototype._render;
    Sprite_Animation.prototype._render = function(renderer) {
        if (Graphics.effekseer && this._targets.length > 0 && this._handle && this._handle.exists) {
            try {
                _Sprite_Animation_render.call(this, renderer);
            } catch (e) {
                console.warn("[FixAndroidGraphics] Animation render error caught:", e);
            }
        }
    };

    // 6. Safe EffectManager hooks
    if (typeof EffectManager !== "undefined") {
        const _EffectManager_load = EffectManager.load;
        EffectManager.load = function(filename) {
            if (Graphics.effekseer) {
                return _EffectManager_load.call(this, filename);
            }
            return null;
        };
    }

    // 7. Fix Android WebView document.hasFocus() freeze / permanent black screen
    SceneManager.isGameActive = function() {
        return true;
    };

    // 8. Edge-to-Edge Fullscreen Stretched Canvas Scaling on Mobile (100% Fullscreen, No Black Bars)
    Utils.isLocal = function() {
        return true;
    };

    Graphics._stretchWidth = function() {
        return window.innerWidth || document.documentElement.clientWidth;
    };

    Graphics._stretchHeight = function() {
        return window.innerHeight || document.documentElement.clientHeight;
    };

    Graphics._centerElement = function(element) {
        element.style.position = "fixed";
        element.style.top = "0px";
        element.style.left = "0px";
        element.style.width = "100vw";
        element.style.height = "100vh";
        element.style.margin = "0px";
        element.style.padding = "0px";
        element.style.zIndex = "1";
    };

    // Pixel-perfect touch / click coordinate conversion using getBoundingClientRect
    Graphics.pageToCanvasX = function(x) {
        if (this._canvas) {
            const rect = this._canvas.getBoundingClientRect();
            if (rect.width > 0) {
                const clientX = x - (window.pageXOffset || window.scrollX || 0);
                return Math.round((clientX - rect.left) * ((this._width || 1280) / rect.width));
            }
        }
        return 0;
    };

    Graphics.pageToCanvasY = function(y) {
        if (this._canvas) {
            const rect = this._canvas.getBoundingClientRect();
            if (rect.height > 0) {
                const clientY = y - (window.pageYOffset || window.scrollY || 0);
                return Math.round((clientY - rect.top) * ((this._height || 720) / rect.height));
            }
        }
        return 0;
    };

    // isInsideCanvas receives ALREADY converted canvas coordinates (x: 0..width, y: 0..height)
    Graphics.isInsideCanvas = function(x, y) {
        return x >= 0 && x < (this._width || 1280) && y >= 0 && y < (this._height || 720);
    };
})();


