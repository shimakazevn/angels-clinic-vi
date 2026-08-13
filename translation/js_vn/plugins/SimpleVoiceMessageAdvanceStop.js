/*:
 * @target MZ
 * @plugindesc SimpleVoice用 メッセージ送り・マップ移動時ボイス停止プラグイン v1.5.0
 * @author
 * @base PluginCommonBase
 * @orderAfter SimpleVoice
 * @orderAfter SaveWindow
 *
 * @help
 * SimpleVoice.js で再生中のボイスを、
 * 以下のタイミングで停止します。
 *
 * ・メッセージ送り入力時
 *   クリック / タップ / 決定キーで文章を次へ進めた瞬間
 *
 * ・メッセージ終了時
 *
 * ・マップ移動時
 *   場所移動、マップ切り替え、イベントによるマップ遷移など
 *
 * ■ v1.2.0
 * メッセージが全文表示される前にクリックして全文表示した場合は、
 * ボイスを停止しないように変更。
 *
 * ■ v1.3.0
 * メッセージウィンドウ上のクリック可能なボタン類を押した場合は、
 * ボイスを停止しないように変更。
 *
 * ■ v1.4.0
 * SaveWindow.js の _customIconSprites に対応。
 *
 * ■ v1.5.0
 * SaveWindow.js のログボタンおよび callTextLog を直接フック。
 * ログ表示時の Scene_Map.stop でもボイスを停止しないように修正。
 *
 * ■ 前提
 * ・SimpleVoice.js 導入済み
 * ・SaveWindow.js のログボタンを使う場合、このプラグインは SaveWindow.js より下に配置してください
 *
 * ■ 注意
 * AudioManager.stopVoice() を呼び出すため、
 * SimpleVoice で再生中のボイスは全チャンネル停止します。
 */

(() => {
    'use strict';

    if (!AudioManager.playVoice || !AudioManager.stopVoice) {
        console.error('SimpleVoiceMessageAdvanceStop: Không tìm thấy SimpleVoice.js.');
        return;
    }

    let voiceStopSuppressCount = 0;
    let logOpeningSuppress = false;

    const stopSimpleVoice = () => {
        AudioManager.stopVoice();
    };

    const suppressVoiceStop = (frame = 30) => {
        voiceStopSuppressCount = Math.max(voiceStopSuppressCount, frame);
    };

    const isVoiceStopSuppressed = () => {
        return voiceStopSuppressCount > 0 || logOpeningSuppress;
    };

    const updateSuppressCount = () => {
        if (voiceStopSuppressCount > 0) {
            voiceStopSuppressCount--;
        }
        if (voiceStopSuppressCount <= 0) {
            logOpeningSuppress = false;
        }
    };

    //--------------------------------------------------------------------------
    // ログ表示開始時の抑制
    //--------------------------------------------------------------------------

    const startLogSuppress = () => {
        logOpeningSuppress = true;
        suppressVoiceStop(30);
    };

    // SaveWindow.js のログボタンを直接フック
    if (Window_Message.prototype.onMenuIconClick) {
        const _Window_Message_onMenuIconClick = Window_Message.prototype.onMenuIconClick;
        Window_Message.prototype.onMenuIconClick = function() {
            startLogSuppress();
            _Window_Message_onMenuIconClick.apply(this, arguments);
        };
    }

    // Scene_Map.callTextLog が存在する場合も直接フック
    if (Scene_Map.prototype.callTextLog) {
        const _Scene_Map_callTextLog = Scene_Map.prototype.callTextLog;
        Scene_Map.prototype.callTextLog = function() {
            startLogSuppress();
            _Scene_Map_callTextLog.apply(this, arguments);
        };
    }

    //--------------------------------------------------------------------------
    // SaveWindow.js のカスタムアイコン判定
    //--------------------------------------------------------------------------

    const isTouchedSaveWindowCustomIcon = messageWindow => {
        if (!TouchInput.isTriggered()) {
            return false;
        }

        if (!messageWindow || !messageWindow._customIconSprites) {
            return false;
        }

        return messageWindow._customIconSprites.some(sprite => {
            if (!sprite || !sprite.visible || sprite.opacity <= 0) {
                return false;
            }

            if (typeof sprite.isTouchInFrame === 'function') {
                return sprite.isTouchInFrame();
            }

            return false;
        });
    };

    //--------------------------------------------------------------------------
    // 汎用ボタン判定
    //--------------------------------------------------------------------------

    const isPointInSprite = (sprite, x, y) => {
        if (!sprite || !sprite.visible || sprite.opacity <= 0) {
            return false;
        }

        if (!sprite.worldTransform) {
            return false;
        }

        const point = sprite.worldTransform.applyInverse(new PIXI.Point(x, y));

        const width = sprite.width || (sprite.bitmap ? sprite.bitmap.width : 0);
        const height = sprite.height || (sprite.bitmap ? sprite.bitmap.height : 0);

        if (width <= 0 || height <= 0) {
            return false;
        }

        const anchorX = sprite.anchor ? sprite.anchor.x : 0;
        const anchorY = sprite.anchor ? sprite.anchor.y : 0;

        const left = -width * anchorX;
        const top = -height * anchorY;
        const right = left + width;
        const bottom = top + height;

        return point.x >= left && point.x < right && point.y >= top && point.y < bottom;
    };

    const isClickableSprite = sprite => {
        if (!sprite) {
            return false;
        }

        if (typeof Sprite_Clickable !== 'undefined' && sprite instanceof Sprite_Clickable) {
            return true;
        }

        const name = sprite.constructor ? sprite.constructor.name : '';
        return /Button|Clickable|Icon/i.test(name);
    };

    const isTouchedClickableChild = root => {
        if (!TouchInput.isTriggered()) {
            return false;
        }

        const x = TouchInput.x;
        const y = TouchInput.y;

        const search = parent => {
            if (!parent || !parent.children) {
                return false;
            }

            for (let i = parent.children.length - 1; i >= 0; i--) {
                const child = parent.children[i];

                if (!child || !child.visible) {
                    continue;
                }

                if (search(child)) {
                    return true;
                }

                if (isClickableSprite(child) && isPointInSprite(child, x, y)) {
                    return true;
                }
            }

            return false;
        };

        return search(root);
    };

    const isTouchedAnyMessageButton = messageWindow => {
        return isTouchedSaveWindowCustomIcon(messageWindow) || isTouchedClickableChild(messageWindow);
    };

    //--------------------------------------------------------------------------
    // updateInput
    //--------------------------------------------------------------------------

    const _Window_Message_updateInput = Window_Message.prototype.updateInput;
    Window_Message.prototype.updateInput = function() {
        if (isTouchedSaveWindowCustomIcon(this)) {
            suppressVoiceStop(30);
        }

        return _Window_Message_updateInput.apply(this, arguments);
    };

    //--------------------------------------------------------------------------
    // メッセージ送り時に停止
    //--------------------------------------------------------------------------

    const _Window_Message_isTriggered = Window_Message.prototype.isTriggered;
    Window_Message.prototype.isTriggered = function() {
        const touchedButton = isTouchedAnyMessageButton(this);

        if (touchedButton) {
            suppressVoiceStop(30);
        }

        const result = _Window_Message_isTriggered.apply(this, arguments);

        if (
            result &&
            this.pause &&
            this.isOpen() &&
            this.active &&
            $gameMessage.hasText() &&
            !touchedButton &&
            !isVoiceStopSuppressed()
        ) {
            stopSimpleVoice();
        }

        return result;
    };

    //--------------------------------------------------------------------------
    // メッセージ終了時に停止
    //--------------------------------------------------------------------------

    const _Window_Message_terminateMessage = Window_Message.prototype.terminateMessage;
    Window_Message.prototype.terminateMessage = function() {
        if (!isVoiceStopSuppressed()) {
            stopSimpleVoice();
        }

        _Window_Message_terminateMessage.apply(this, arguments);
    };

    //--------------------------------------------------------------------------
    // マップ移動時に停止
    //--------------------------------------------------------------------------

    const _Game_Player_performTransfer = Game_Player.prototype.performTransfer;
    Game_Player.prototype.performTransfer = function() {
        if (this.isTransferring()) {
            stopSimpleVoice();
        }

        _Game_Player_performTransfer.apply(this, arguments);
    };

    //--------------------------------------------------------------------------
    // Scene_Map 更新
    //--------------------------------------------------------------------------

    const _Scene_Map_update = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() {
        _Scene_Map_update.apply(this, arguments);
        updateSuppressCount();
    };

    //--------------------------------------------------------------------------
    // マップシーン終了時に停止
    //
    // ログ表示による Scene_Map.stop の場合は停止しない。
    //--------------------------------------------------------------------------

    const _Scene_Map_stop = Scene_Map.prototype.stop;
    Scene_Map.prototype.stop = function() {
        if (!isVoiceStopSuppressed()) {
            stopSimpleVoice();
        }

        _Scene_Map_stop.apply(this, arguments);
    };
})();