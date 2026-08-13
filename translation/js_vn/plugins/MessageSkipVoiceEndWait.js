//=============================================================================
// MessageSkipVoiceEndWait.js
//=============================================================================

/*:
 * @target MZ
 * @plugindesc MessageSkip/SimpleVoice用 ボイス終了後オート送り待機プラグイン v1.0.0
 * @author 
 * @orderAfter MessageSkip
 * @orderAfter SimpleVoice
 *
 * @param WaitFrame
 * @text ボイス終了後ウェイト
 * @desc SimpleVoiceのボイス終了後、オートで次のメッセージへ進むまで待機するフレーム数です。
 * @default 30
 * @type number
 * @min 0
 *
 * @help
 * MessageSkip.js と SimpleVoice.js の併用時に、
 * ボイスが流れ終わったあと、指定フレーム数だけ
 * オートモードの次メッセージ送りを待機します。
 *
 * ■ 前提
 * ・MessageSkip.js
 * ・SimpleVoice.js
 *
 * ■ プラグイン管理の順番
 * 1. SimpleVoice.js
 * 2. MessageSkip.js
 * 3. MessageSkipVoiceEndWait.js
 *
 * ■ 仕様
 * ・MessageSkip.js のオートモードに対して動作します。
 * ・SimpleVoice の通常ボイスが再生中の間は、従来通り次へ進みません。
 * ・ボイス終了後、パラメータ「ボイス終了後ウェイト」のフレーム数だけ待ちます。
 * ・その後、オートで次のメッセージへ進みます。
 *
 * ■ 注意
 * ・クリック、決定キー、スキップモードによる手動送りは制限しません。
 * ・ループボイスは MessageSkip.js 側の仕様に合わせて待機対象外です。
 *
 * ■ フレーム数の目安
 * 30 = 約0.5秒
 * 60 = 約1秒
 *
 */

(() => {
    'use strict';

    const pluginName = 'MessageSkipVoiceEndWait';
    const parameters = PluginManager.parameters(pluginName);
    const waitFrame = Number(parameters.WaitFrame || 0);

    if (!AudioManager.isExistVoice) {
        console.error(`${pluginName}: Không tìm thấy MessageSkip.js hoặc SimpleVoice.js.`);
        return;
    }

    const VoiceEndWaitManager = {
        _wasVoicePlaying: false,
        _waitCount: 0,

        reset() {
            this._wasVoicePlaying = false;
            this._waitCount = 0;
        },

        update(isVoicePlaying) {
            if (waitFrame <= 0) {
                return isVoicePlaying;
            }

            if (isVoicePlaying) {
                this._wasVoicePlaying = true;
                this._waitCount = waitFrame;
                return true;
            }

            if (this._wasVoicePlaying && this._waitCount > 0) {
                this._waitCount--;
                return true;
            }

            this._wasVoicePlaying = false;
            this._waitCount = 0;
            return false;
        }
    };

    const _AudioManager_isExistVoice = AudioManager.isExistVoice;
    AudioManager.isExistVoice = function() {
        const isVoicePlaying = _AudioManager_isExistVoice.apply(this, arguments);
        return VoiceEndWaitManager.update(isVoicePlaying);
    };

    const _Window_Message_startMessage = Window_Message.prototype.startMessage;
    Window_Message.prototype.startMessage = function() {
        VoiceEndWaitManager.reset();
        _Window_Message_startMessage.apply(this, arguments);
    };

    const _Game_Player_performTransfer = Game_Player.prototype.performTransfer;
    Game_Player.prototype.performTransfer = function() {
        if (this.isTransferring()) {
            VoiceEndWaitManager.reset();
        }
        _Game_Player_performTransfer.apply(this, arguments);
    };

    const _Scene_Map_stop = Scene_Map.prototype.stop;
    Scene_Map.prototype.stop = function() {
        VoiceEndWaitManager.reset();
        _Scene_Map_stop.apply(this, arguments);
    };
})();