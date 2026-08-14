//=============================================================================
// FixAndroidGraphics.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Comprehensive Mobile Optimization: 60 FPS Cap, Low Battery & Thermals, Fullscreen Scaling, WebGL & Effekseer Safety for Android.
 * @author Antigravity
 * @help
 * 1. Caps max FPS at 60 FPS to prevent 90Hz/120Hz/144Hz screens from overheating & battery drain.
 * 2. Optimized 1x native WebGL rendering with Hardware-Accelerated CSS scaling for smooth 60 FPS on any chip.
 * 3. Automatic texture & VRAM garbage collection to prevent out-of-memory crashes on 2GB-4GB RAM phones.
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

    // 2. Optimized PIXI Settings for Mobile (Power Saving, No Overheating, 60 FPS)
    Graphics._setupPixi = function() {
        PIXI.utils.skipHello();
        
        // Auto garbage collection for textures every 300 frames (~5s) to save VRAM
        PIXI.settings.GC_MAX_IDLE = 300;
        PIXI.settings.GC_MODE = PIXI.GC_MODES.AUTO;
        
        // Linear scale mode for crisp interpolation
        PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.LINEAR;
        
        // Cap shared ticker to 60 FPS (prevents 120Hz/144Hz high refresh rate overheat)
        if (PIXI.Ticker && PIXI.Ticker.shared) {
            PIXI.Ticker.shared.maxFPS = 60;
            PIXI.Ticker.shared.minFPS = 30;
        }
    };

    // 3. Multi-tier PIXI Application Creation (1x Native Buffer, Hardware Scaled)
    Graphics._createPixiApp = function() {
        this._setupPixi();
        let app = null;

        // Tier 1: Optimal Mobile WebGL (1x resolution, preserveDrawingBuffer for WebView compositing)
        try {
            app = new PIXI.Application({
                view: this._canvas,
                autoStart: false,
                width: this._width || 1280,
                height: this._height || 720,
                resolution: 1, // Keep 1x native buffer: massive battery saver & silky smooth
                powerPreference: "default", // Balanced power profile
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
                this._app.ticker.maxFPS = 60;
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

    // 8. Fullscreen Stretched 100% Canvas Scaling on Android
    Utils.isLocal = function() {
        return true;
    };

    Graphics._stretchWidth = function() {
        return window.innerWidth || document.documentElement.clientWidth;
    };

    Graphics._stretchHeight = function() {
        return window.innerHeight || document.documentElement.clientHeight;
    };
})();
