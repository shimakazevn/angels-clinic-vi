//=============================================================================
// FullScreenStretch.js
// Plugin hỗ trợ chế độ Tràn Viền Toàn Màn Hình (Full Screen Stretch / No Black Bars)
// và tùy chỉnh Tỉ lệ hiển thị cho RPG Maker MZ (PC / Android / iOS).
//=============================================================================

/*:
 * @target MZ
 * @plugindesc Hỗ trợ hiển thị Tràn Viền Toàn Màn Hình (Stretch to Fit Screen) và giữ đúng tọa độ cảm ứng/chuột.
 * @author Antigravity
 *
 * @param defaultStretch
 * @text Chế độ tràn viền mặc định
 * @desc Bật (true) để mặc định tràn toàn màn hình, Tắt (false) để giữ tỉ lệ 16:9 có viền đen.
 * @type boolean
 * @default true
 *
 * @param optionName
 * @text Tên mục trong Tùy Chọn
 * @desc Tên hiển thị trong menu Tùy Chọn (Options).
 * @default Tràn viền toàn màn hình
 */

(() => {
    const pluginName = "FullScreenStretch";
    const parameters = PluginManager.parameters(pluginName);
    const defaultStretch = parameters["defaultStretch"] !== "false";
    const optionName = parameters["optionName"] || "Tràn viền toàn màn hình";

    // 1. ConfigManager
    ConfigManager.screenStretch = defaultStretch;

    const _ConfigManager_makeData = ConfigManager.makeData;
    ConfigManager.makeData = function() {
        const config = _ConfigManager_makeData.call(this);
        config.screenStretch = this.screenStretch;
        return config;
    };

    const _ConfigManager_applyData = ConfigManager.applyData;
    ConfigManager.applyData = function(config) {
        _ConfigManager_applyData.call(this, config);
        if (typeof config.screenStretch !== "undefined") {
            this.screenStretch = config.screenStretch;
        } else {
            this.screenStretch = defaultStretch;
        }
        if (Graphics._canvas) {
            Graphics._updateRealScale();
            Graphics._centerElement(Graphics._canvas);
        }
    };

    // 2. Options Window
    const _Window_Options_addGeneralOptions = Window_Options.prototype.addGeneralOptions;
    Window_Options.prototype.addGeneralOptions = function() {
        _Window_Options_addGeneralOptions.call(this);
        this.addCommand(optionName, "screenStretch");
    };

    // 3. Graphics Scaling Overrides
    Graphics._realScaleX = function() {
        if (ConfigManager.screenStretch && this._width > 0) {
            return this._stretchWidth() / this._width;
        }
        return this._realScale;
    };

    Graphics._realScaleY = function() {
        if (ConfigManager.screenStretch && this._height > 0) {
            return this._stretchHeight() / this._height;
        }
        return this._realScale;
    };

    const _Graphics_centerElement = Graphics._centerElement;
    Graphics._centerElement = function(element) {
        if (ConfigManager.screenStretch) {
            const width = this._stretchWidth();
            const height = this._stretchHeight();
            element.style.position = "absolute";
            element.style.margin = "0";
            element.style.top = "0px";
            element.style.left = "0px";
            element.style.right = "0px";
            element.style.bottom = "0px";
            element.style.width = width + "px";
            element.style.height = height + "px";
        } else {
            _Graphics_centerElement.call(this, element);
        }
    };

    Graphics.pageToCanvasX = function(x) {
        if (this._canvas) {
            const left = this._canvas.offsetLeft || 0;
            const scaleX = this._realScaleX();
            return Math.round((x - left) / scaleX);
        }
        return 0;
    };

    Graphics.pageToCanvasY = function(y) {
        if (this._canvas) {
            const top = this._canvas.offsetTop || 0;
            const scaleY = this._realScaleY();
            return Math.round((y - top) / scaleY);
        }
        return 0;
    };

    Graphics.isInsideCanvas = function(x, y) {
        if (this._canvas) {
            const left = this._canvas.offsetLeft || 0;
            const top = this._canvas.offsetTop || 0;
            const width = parseFloat(this._canvas.style.width) || (this._canvas.width * this._realScale);
            const height = parseFloat(this._canvas.style.height) || (this._canvas.height * this._realScale);
            return x >= left && x <= left + width && y >= top && y <= top + height;
        }
        return false;
    };

    // 4. Hotkey F10 to toggle stretch mode
    document.addEventListener("keydown", (event) => {
        if (event.key === "F10") {
            ConfigManager.screenStretch = !ConfigManager.screenStretch;
            ConfigManager.save();
            Graphics._updateRealScale();
            if (Graphics._canvas) {
                Graphics._centerElement(Graphics._canvas);
            }
        }
    });

    // Auto-apply on window resize
    window.addEventListener("resize", () => {
        if (Graphics._canvas) {
            Graphics._updateRealScale();
            Graphics._centerElement(Graphics._canvas);
        }
    });

})();
