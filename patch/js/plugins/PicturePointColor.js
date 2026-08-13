/**
 *  @file    PicturePointColor
 *  @author  moca
 *  @version 1.0.1 2022/08/29
 */

/*:ja
 * @target MZ
 * @plugindesc マウスカーソルがピクチャ上にある時、その色を変数に代入します
 * @author moca
 * @help マウスカーソルがピクチャ上にある時、その色を変数に代入します
 * 
 * ●ピクチャの色を16進数で取得する
 * 
 * PPC_GET_RGB [ピクチャ番号] [変数番号]
 * 
 * 例：マウス座標にあるピクチャ番号1の色を変数番号10に代入する
 * 　PPC_GET_RGB 1 10
 * 
 * スクリプト呼び出し
 *  $gameScreen.getPicturePointerColorRGB([ピクチャ番号], [変数番号]);
 * 
 * 
 * ●ピクチャの色を10進数で取得する
 * 
 * PPC_GET_RGB_DEC [ピクチャ番号] [変数番号]
 * 
 * 例：マウス座標にあるピクチャ番号1の色を10進数に変換して変数番号10に代入する
 * 　PPC_GET_RGB_DEC 1 10
 * 
 * スクリプト呼び出し
 *  $gameScreen.getPicturePointerColorRGB_DEC([ピクチャ番号], [変数番号]);
 * 
 * ## バージョン履歴
 * 2022/08/29 ピクチャの色を10進数で取得する機能を追加
 * 2022/08/24 1.0.0 初版
 * 
 * 利用規約：
 *  プラグイン作者に無断で使用、改変、再配布は不可です。
*/

/*
(function () {
    'use strict';

    ///**
     * ゲーム内変数を取得する
     * @param {String} text \V[n]形式の制御文字
     * @returns {number} ゲーム内変数
     */
     /*
    var getUsingVariable = function (text) {
        text = text.replace(/\\/g, '\x1b');
        text = text.replace(/\x1b\x1b/g, '\\');
        text = text.replace(/\\/g, '\x1b');
        text = text.replace(/\x1b\x1b/g, '\\');
        text = text.replace(/\x1bV\[(\d+)\]/gi, function () {
            return $gameVariables.value(parseInt(arguments[1]));
        }.bind(this));
        text = text.replace(/\x1bV\[(\d+)\]/gi, function () {
            return $gameVariables.value(parseInt(arguments[1]));
        }.bind(this));
        return parseInt(text);
    };

    // プラグインコマンド
    const _Game_Interpreter_pluginCommand = Game_Interpreter.prototype.pluginCommand;
    Game_Interpreter.prototype.pluginCommand = function (command, args) {
        _Game_Interpreter_pluginCommand.apply(this, arguments);

        if (command.toLowerCase() === "ppc_get_rgb") {
            if (args.length < 2) {
                throw "Thiếu tham số lệnh plugin PPC_GET_RGB"
            }
            else {
                $gameScreen.getPicturePointColorRGB(getUsingVariable(args[0]), getUsingVariable(args[1]));
            }
        }
        else if (command.toLowerCase() === "ppc_get_rgb_dec") {
            if (args.length < 2) {
                throw "Thiếu tham số lệnh plugin PPC_GET_RGB_DEC"
            }
            else {
                $gameScreen.getPicturePointColorRGB_DEC(getUsingVariable(args[0]), getUsingVariable(args[1]));
            }
        }
    };

    Game_Screen.prototype._getPicturePointColor = function (pictureId) {
        let pic = this.picture(pictureId);
        let result = -1;
        if (pic !== undefined) {
            let sprite = new Sprite_Picture(pictureId);

            let w = sprite.bitmap.width;
            let h = sprite.bitmap.height;
            let scaleX = pic.scaleX() / 100;
            let scaleY = pic.scaleY() / 100;

            let sx = TouchInput.x - pic.x();
            let sy = TouchInput.y - pic.y();

            // ピクチャの基点が中央ならずらす
            if (pic.origin() === 1) {
                sx += scaleX * w / 2;
                sy += scaleY * h / 2;
            }
            let x = sx * (w / (w * scaleX));
            let y = sy * (h / (h * scaleY));

            let color = sprite.bitmap.getPixel(x, y);
            // ピクチャの外だった場合は-1を返す
            if (x < 0 || y < 0 || x > w || y > h) {
                color = -1;
            }

            result = color;
        }

        return result;
    };

    Game_Screen.prototype.getPicturePointColorRGB = function (pictureId, valueId) {
        let color = $gameScreen._getPicturePointColor(pictureId);
        $gameVariables.setValue(valueId, color);
    };

    Game_Screen.prototype.getPicturePointColorRGB_DEC = function (pictureId, valueId) {
        let color = $gameScreen._getPicturePointColor(pictureId);
        if (color !== -1) {
            color = parseInt(color.replace('#', ''), 16);
        }
        $gameVariables.setValue(valueId, color);
    };

    TouchInput._onMouseMove = function (event) {
        var x = Graphics.pageToCanvasX(event.pageX);
        var y = Graphics.pageToCanvasY(event.pageY);
        this._onMove(x, y);
    };
})();
*/



(() => {
    'use strict';

    const _Game_Interpreter_pluginCommand = Game_Interpreter.prototype.pluginCommand;
    Game_Interpreter.prototype.pluginCommand = function (command, args) {
        _Game_Interpreter_pluginCommand.apply(this, arguments);

        if (command.toLowerCase() === "ppc_get_rgb") {
            if (args.length < 2) {
                throw new Error("Thiếu tham số lệnh plugin PPC_GET_RGB");
            } else {
                this.getPicturePointColorRGB(parseInt(args[0]), parseInt(args[1]));
            }
        } else if (command.toLowerCase() === "ppc_get_rgb_dec") {
            if (args.length < 2) {
                throw new Error("Thiếu tham số lệnh plugin PPC_GET_RGB_DEC");
            } else {
                this.getPicturePointColorRGB_DEC(parseInt(args[0]), parseInt(args[1]));
            }
        }
    };

    var getUsingVariable = function (text) {
        text = text.replace(/\\/g, '\x1b');
        text = text.replace(/\x1b\x1b/g, '\\');
        text = text.replace(/\\/g, '\x1b');
        text = text.replace(/\x1b\x1b/g, '\\');
        text = text.replace(/\x1bV\[(\d+)\]/gi, function () {
            return $gameVariables.value(parseInt(arguments[1]));
        }.bind(this));
        text = text.replace(/\x1bV\[(\d+)\]/gi, function () {
            return $gameVariables.value(parseInt(arguments[1]));
        }.bind(this));
        return parseInt(text);
    };

    Game_Screen.prototype.getPicturePointerColorRGB = function (pictureId, valueId) {
        let color = this._getPicturePointColor(pictureId);
        $gameVariables.setValue(valueId, color.toString(16).padStart(6, '0'));
    };

    Game_Screen.prototype.getPicturePointerColorRGB_DEC = function (pictureId, valueId) {
        let color = this._getPicturePointColor(pictureId);
        $gameVariables.setValue(valueId, color);
    };

    Game_Screen.prototype._getPicturePointColor = function (pictureId) {
        let pic = this.picture(pictureId);
        let result = -1;
        if (pic !== undefined) {
            let sprite = new Sprite_Picture(pictureId);

            let w = sprite.bitmap.width;
            let h = sprite.bitmap.height;
            let scaleX = pic.scaleX() / 100;
            let scaleY = pic.scaleY() / 100;

            let sx = Math.round(TouchInput.x - pic.x()); // 座標を整数値に丸める
            let sy = Math.round(TouchInput.y - pic.y()); // 座標を整数値に丸める

            // ピクチャの基点が中央ならずらす
            if (pic.origin() === 1) {
                sx += scaleX * w / 2;
                sy += scaleY * h / 2;
            }
            let x = Math.floor(sx * (w / (w * scaleX))); // 座標を整数値に丸める
            let y = Math.floor(sy * (h / (h * scaleY))); // 座標を整数値に丸める

            if (x >= 0 && x < w && y >= 0 && y < h) {
                let canvas = SceneManager._scene._spriteset._pictureContainer.children[pictureId - 1].bitmap.canvas;
                let context = canvas.getContext('2d');
                let imageData = context.getImageData(x, y, 1, 1);
                let data = imageData.data;
                result = (data[0] << 16) | (data[1] << 8) | data[2];
            }
        }

        return result;
    };

    const _TouchInput_onMouseMove = TouchInput._onMouseMove;
    TouchInput._onMouseMove = function (event) {
        _TouchInput_onMouseMove.call(this, event);

        var x = Graphics.pageToCanvasX(event.pageX);
        var y = Graphics.pageToCanvasY(event.pageY);
        this._onMove(x, y);
    };
})();
