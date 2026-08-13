//=============================================================================
// MOG_TitleCommands_AlphaHit.js
// ----------------------------------------------------------------------------
// MOG_TitleCommands.js 用 透過部分クリック無効化パッチ
//=============================================================================

/*:
 * @target MZ
 * @plugindesc MOG_TitleCommandsのタイトルコマンド当たり判定から透過部分を除外します v1.0.0
 * @author 
 * @orderAfter MOG_TitleCommands
 *
 * @param AlphaThreshold
 * @text 不透明度しきい値
 * @desc この値以下のアルファ値のピクセルはクリック対象外になります。0なら完全透明のみ除外します。
 * @default 0
 * @type number
 * @min 0
 * @max 255
 *
 * @help
 * MOG_TitleCommands.js の画像コマンドについて、
 * PNGの透明部分をクリック判定に含めないようにします。
 *
 * ■ 導入順
 * MOG_TitleCommands.js
 * MOG_TitleCommands_AlphaHit.js
 *
 * ■ 仕様
 * ・画像の矩形内にマウスがあっても、その座標のピクセルが透明なら反応しません。
 * ・選択中/非選択中で上下に分かれている Command_x.png の現在表示フレームに対応します。
 *
 * ■ パラメータ
 * 不透明度しきい値:
 *   0   = 完全透明のみ無効
 *   10  = ほぼ透明も無効
 *   128 = 半透明以下を無効
 */

(() => {
    'use strict';

    const pluginName = 'MOG_TitleCommands_AlphaHit';
    const parameters = PluginManager.parameters(pluginName);
    const alphaThreshold = Number(parameters.AlphaThreshold || 0);

    if (typeof TpictureCom === 'undefined') {
        console.error(`${pluginName}: Không tìm thấy MOG_TitleCommands.js.`);
        return;
    }

    TpictureCom.prototype.isOnPicCom = function() {
        if (!this.bitmap || !this.bitmap.isReady()) {
            return false;
        }

        const touchX = TouchInput.x;
        const touchY = TouchInput.y;

        const width = this._cw || this.width;
        const height = this._ch || this.height;

        if (width <= 0 || height <= 0) {
            return false;
        }

        // 画面座標からスプライト内のローカル座標へ変換
        const localX = (touchX - this.x) / this.scale.x + this.anchor.x * width;
        const localY = (touchY - this.y) / this.scale.y + this.anchor.y * height;

        if (localX < 0 || localX >= width) {
            return false;
        }

        if (localY < 0 || localY >= height) {
            return false;
        }

        // 現在表示中のフレーム位置を考慮する
        const frame = this._frame;
        const bitmapX = Math.floor(frame.x + localX);
        const bitmapY = Math.floor(frame.y + localY);

        const alpha = this.bitmap.getAlphaPixel(bitmapX, bitmapY);

        return alpha > alphaThreshold;
    };
})();