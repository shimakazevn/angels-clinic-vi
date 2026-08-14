//=============================================================================
// FixAndroidGraphics.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Fixes "Failed to initialize graphics" on Android, WebViews, mobile GPUs, and WebGL compatibility issues.
 * @author Antigravity
 * @help
 * 1. Prevents Effekseer failure from destroying the PIXI Application.
 * 2. Adds multi-tier WebGL fallback options for Android WebViews & mobile GPUs.
 * 3. Gracefully handles devices without WebGL2 or 3D Effekseer support.
 */

(() => {
    // 1. Robust WebGL Check
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

    // 2. Multi-tier PIXI Application Creation for Mobile & Android WebViews
    Graphics._createPixiApp = function() {
        this._setupPixi();
        let app = null;

        // Tier 1: Standard initialization
        try {
            app = new PIXI.Application({
                view: this._canvas,
                autoStart: false,
                powerPreference: "high-performance"
            });
        } catch (e1) {
            console.warn("[FixAndroidGraphics] Standard PIXI init failed, trying Tier 2 fallback...", e1);
        }

        // Tier 2: Safe Mobile WebGL initialization
        if (!app) {
            try {
                app = new PIXI.Application({
                    view: this._canvas,
                    autoStart: false,
                    powerPreference: "default",
                    failIfMajorPerformanceCaveat: false,
                    antialias: false,
                    resolution: 1,
                    preserveDrawingBuffer: true
                });
            } catch (e2) {
                console.warn("[FixAndroidGraphics] Tier 2 PIXI init failed, trying Tier 3 fallback...", e2);
            }
        }

        // Tier 3: Minimal fallback options
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
        } else {
            this._app = null;
        }
    };

    // 3. Prevent Effekseer failure from destroying working PIXI Application
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
                // CRITICAL: DO NOT set this._app = null! Keep PIXI working!
            }
        }
    };

    // 4. Safe Sprite_Animation hooks when Effekseer is unavailable
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

    // 5. Safe EffectManager hooks
    if (typeof EffectManager !== "undefined") {
        const _EffectManager_load = EffectManager.load;
        EffectManager.load = function(filename) {
            if (Graphics.effekseer) {
                return _EffectManager_load.call(this, filename);
            }
            return null;
        };
    }
})();
