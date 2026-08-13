//=============================================================================
// FadeSpinePicture.js
//============================================================================


var Imported = Imported || {};
Imported.SU_FadeSpine = true;
var SU = SU || {};
SU.FadeSpine = SU.FadeSpine || {};

/*:
 * @plugindesc Spineモデルの色調変化にフェード効果を適用できるようにする。
 * @author Su
 *
 * @param FrameCount
 * @text 変化時間（フレーム数）
 * @desc 指定した値をフェードフレーム数のデフォルト値として設定します。
 * @type number
 * @default 24
 * @min 1
 *
 * @help
 * ============================================================================
 * Introduction
 * ============================================================================

 * Spine のモデルに対してフェード効果を付けた色調変化を行うことができます。
 * * 必ずPictureSpine.js よりも下に配置してください。
 *
 * ============================================================================
 * Usage
 * ============================================================================
 *
 * 通常の手順でSpine画像を表示させた後、下記のようにプラグインコマンドを使用してフェードイン・フェードアウトを実行してください。
 *
 * S-in 1
 * パラメータで指定したフレーム数（デフォルトでは24フレーム）で画像をフェードインさせます。
 * 　フェードインで登場させる場合は、Spine モデルを表示する記述に次の処理を追加して透明の状態で表示させてください。
 *      .SetColor(1, 1, 1, 0)
 *
 * S-out 1 60
 * 60フレーム（１秒）で画像をフェードアウトさせます。
 * 
 * ============================================================================
 * Plugin Commands
 * ============================================================================
 * 
 * S-in xx (yy)
 * - フェードイン
 *  xx に指定したピクチャIDのピクチャを yy に指定したフレーム数でフェードインさせます。
 *  yy は省略可能で、その場合はプラグインパラメータに指定したフレーム数で変化します。
 *
 * S-showIn id x y scaleX scaleY skeleton (skin) (animation) (frame)
 * - ピクチャを作成してフェードイン
 *  ピクチャの表示コマンドとフェードイン処理を同時に行います。
 *  id には使用するピクチャ番号を指定する。
 *  x, y は位置、scaleX, scaleY は拡大率の幅と高さにそれぞれ該当します。
 *  skeleton にはスケルトン名、skin にはスキン名、animation にはアニメーションをそれぞれ指定してください
 *  animation はカンマ（,）で繋ぐことで、連続したアニメーションを指定でき、最後に指定したものをループ再生します。
 *  frame はフェード効果にかけるフレーム数です。
 *  skin、animation、frame は省略できますが、後ろの要素を指定したい場合は空白を入れるか、'' と指定してください
 *  例）ピクチャ番号１番を使用し、座標（100, 0）の位置に 30% の大きさで、
 *      「ハロルド」というスケルトンをスキン指定は省略するが、
 *      「攻撃」の後「待機」するアニメーションを指定し、デフォルトのフレーム数でフェードインさせる場合。
 *
 *       S-showIn 1 100 0 30 30 ハロルド '' 攻撃,待機
 *
 *  スロットを指定したアニメーションや、Mix値指定等の細かい設定は場合は個別に行ってください。
 *
 * S-out xx (yy)
 * - フェードアウト（※消去はしません）
 *  xx に指定したピクチャIDのピクチャを yy に指定したフレーム数でフェードアウトさせます。
 *  yy は省略可能で、その場合はプラグインパラメータに指定したフレーム数で変化します。
 *
 * S-delete xx (yy)
 * - フェードアウトして消去
 *  フェードアウトした後に当該ピクチャを消去します。
 *
 * S-setA xx yy (zz)
 * - 指定の不透明度に変化させる
 *  xx に指定したピクチャIDのピクチャを yy に指定した不透明度まで zz に指定したフレーム数でフェードさせます。
 *  yy は 0～１ の範囲で 1 が通常、0 で完全に透明になります。
 *  zz は省略可能で、その場合はプラグインパラメータに指定したフレーム数で変化します。
 *
 * S-setV xx yy (zz)
 * - 指定の明るさに変化させる
 *  xx に指定したピクチャIDのピクチャを yy に指定した明度まで zz に指定したフレーム数でフェードさせます。
 *  yy は 0～任意の数字で 1 が通常、0 で完全に黒になります。
 *  zz は省略可能で、その場合はプラグインパラメータに指定したフレーム数で変化します。
 *
 * S-waitOn
 * - フェード処理が完了するまでwaitが掛かるようになります。
 *
 * S-waitOff
 * - フェード処理の完了を待たずに次のコマンドを実行するようになります。
 *
 * ============================================================================
 * Changelog
 * ============================================================================
 * Version 1.6 2023/03/08:
 * - ピクチャの表示とフェードインを同時に行うコマンドと、フェードアウト後にピクチャを消去するコマンドを追加しました。
 *
 * Version 1.5.2 2023/03/02:
 * - 会話中キー長押しによるメッセージの早送りをしていると、
 *  ウェイトとフェードの終了タイミングがずれる不具合を修正しました。
 *
 * Version 1.5.1 2023/02/17:
 * - ファイル名を変更しました
 *  旧：FadeSpine.js
 *  新：SU_FadeSpine.js
 *
 * Version 1.5 2023/02/15:
 * プラグイン製作者向け
 * - フェード関数をピクチャID だけでなく Game_Spine のインスタンスを渡して指定できるようにしました
 * - フェード関数にコールバックを指定できるようになりました
 * - その他軽微な修正・変更
 *
 * Version 1.4.1:
 * - プラグインの説明欄に変更を加えました
 *
 * Version 1.4:
 * - 他のプラグインで使用するコマンドでもこのプラグインの警告ログが出る不具合を修正
 *
 * Version 1.3:
 * - 指定した不透明度や明度までフェードできるコマンドを追加しました
 *
 * Version 1.2:
 * - 前の不具合を潰しきれてませんでした！のでさらに修正
 *
 * Version 1.1:
 * - S-waitOn や S-waitOff 等の引数を必要としないコマンドに引数が与えられると実行されない不具合を修正
 * 
 * Version 1.0:
 * - Plugin released.
*/

//=============================================================================
// Parameters
//=============================================================================

const pluginName = document.currentScript.src.split('/').pop().replace(/\.js$/, '');
SU.Parameters = PluginManager.parameters(pluginName);

SU.FadeSpine.FSFrameCount = Number(SU.Parameters['FrameCount']) || Game_Interpreter.prototype.fadeSpeed();
SU.FadeSpine.executions = {};
SU.FadeSpine.onWait = false;

//=============================================================================
// Update
//=============================================================================
(_updateMain_ => {
    Scene_Map.prototype.updateMain = function () {
        _updateMain_.call(this);

        SU.FadeSpine.update();
    }
})(Scene_Map.prototype.updateMain);

(_update_ => {
    Scene_Battle.prototype.update = function () {
        _update_.call(this);

        SU.FadeSpine.update();
    }
})(Scene_Battle.prototype.update);

SU.FadeSpine.update = function () {
    let executions = this.executions;
    if (Object.keys(executions).length == 0) return;

    for (const key in executions) {
        let e = executions[key];
        e.update();
        if (e.duration() <= 0) {
            const callback = e.callback;
            if (callback || typeof callback === 'function') callback();
            delete executions[key];
        }
    }
};

SU.FadeSpine.getColor = (spine) => {
    let col = spine.color['/default/'];

    if (!col) return [1, 1, 1, 1];

    return [...col];
};

//=============================================================================
// Fade
//=============================================================================

SU.FadeSpine.setColor = function (spine, argColor, frame, callback) {
    let duration = (frame > 0) ? frame : this.FSFrameCount;

    const getColor = () => this.getColor(spine);

    const currentColor = getColor();
    const targetColor = argColor;

    // アルファ値の指定が無ければ現在のアルファ値で補間する
    if (targetColor[3] == undefined) {
        targetColor[3] = currentColor[3];
    }

    // 変化させる必要のある色インデックスを抽出
    let difIndex = targetColor
        .map((color, i) => (color != currentColor[i]) ? i : -1)
        .filter(index => index != -1);

    function fadeUpdate() {
        if (duration <= 0) return;

        let c = getColor();

        for (const i of difIndex) {
            c[i] = (c[i] * (duration - 1) + targetColor[i]) / duration;
        }

        spine.setColor(...c);

        duration--;
    }

    return {
        update: () => fadeUpdate(),
        duration: () => duration,
        callback: callback,
    }

};

SU.FadeSpine.setColorFromId = function (id, argColor, frame, callback) {
    const spine = $gameScreen.spine(id)
    return this.setColor(spine, argColor, frame, callback);
};

SU.FadeSpine.setAlpha = function (spine, alpha, frame, callback) {
    let targetColor = this.getColor(spine);
    // アルファ値を設定
    targetColor[3] = alpha

    return this.setColor(spine, targetColor, frame, callback);
};

SU.FadeSpine.setAlphaFromId = function (id, alpha, frame, callback) {
    let spine = $gameScreen.spine(id)
    return this.setAlpha(spine, alpha, frame, callback);
};


//=============================================================================
// Plugin Commands
//=============================================================================
(_pluginCommand_ => {
    Game_Interpreter.prototype.pluginCommand = function (command, args) {
        _pluginCommand_.call(this, command, args);

        // コマンドの接頭辞を確認
        let commandParts = command.split('-');
        let prefix = commandParts[0];
        if (prefix !== 'S') return;

        let commandName = commandParts[1];

        //=============================================================================
        // 引数無しのコマンド
        //=============================================================================
        switch (commandName) {
            case 'waitOn':
                SU.FadeSpine.onWait = true;
                return;
            case 'waitOff':
                SU.FadeSpine.onWait = false;
                return;
        }

        let numArgs = args.length;
        if (!numArgs) {
            console.warn(`Command "${command}" needs pictureId at first argument`);
            return;
        }
        //=============================================================================
        // 引数ありのコマンド
        //=============================================================================

        let spineId = Number(args[0]);

        if (commandName === 'showIn') {
            const x = Number(args[1]);
            const y = Number(args[2]);
            const scaleX = Number(args[3]);
            const scaleY = Number(args[4]);
            // ピクチャを作成
            $gameScreen.showPicture(spineId, '', origin, x, y, scaleX, scaleY, 255, 0);

            const skeleton = args[5];
            const skin = args[6].replace(/\'/g, '');
            const animation = args[7].replace(/\'/g, '') || '';
            const spine = $gameScreen.spine(spineId);
            // Spineモデルをセット
            spine.setSkeleton(skeleton)
                .setColor(1, 1, 1, 0);
            if (skin) spine.setSkin(skin);
            if (animation) spine.setAnimation(0, animation.split(','), 'sequential', 'continue', true);

            let frame = args[8] || SU.FadeSpine.FSFrameCount;
            // フェードイン
            SU.FadeSpine.executions[spineId] = SU.FadeSpine.setAlphaFromId(spineId, 1, frame);
            if (SU.FadeSpine.onWait) this.wait(frame);
            return;
        }

        // 使用していないSpriteIDなら無視する
        if (!$gameScreen.picture(spineId)) {
            console.warn(`Not found picture(${spineId}) of plugin command "${command}"`);
            return;
        } else if (!$gameScreen.spine(spineId).skeleton) {
            console.warn(`Not found spine(${spineId}) of plugin command "${command}"`);
            return;
        }

        // フレーム数の指定が無い場合はパラメータに指定された値を使用する
        let frame = args[1] || SU.FadeSpine.FSFrameCount;

        switch (commandName) {
            case 'in':
                SU.FadeSpine.executions[spineId] = SU.FadeSpine.setAlphaFromId(spineId, 1, frame);
                if (SU.FadeSpine.onWait) this.wait(frame);
                return;
            case 'out':
                SU.FadeSpine.executions[spineId] = SU.FadeSpine.setAlphaFromId(spineId, 0, frame);
                if (SU.FadeSpine.onWait) this.wait(frame);
                return;
            case 'delete':
                SU.FadeSpine.executions[spineId] = SU.FadeSpine.setAlphaFromId(spineId, 0, frame,
                    () => $gameScreen.erasePicture(spineId));
                if (SU.FadeSpine.onWait) this.wait(frame);
                return;
        }

        // 引数が2つ以上必要なコマンド
        if (numArgs < 2) {
            console.warn(`Plugin command "${command}" needs value at second argument`);
            return;
        }
        frame = args[2] || SU.FadeSpine.FSFrameCount;
        switch (commandName) {
            case 'setA':
                let alpha = Number(args[1]);

                SU.FadeSpine.executions[spineId] = SU.FadeSpine.setAlphaFromId(spineId, alpha, frame);
                if (SU.FadeSpine.onWait) this.wait(frame);
                return;
            case 'setV':
                let scale = Number(args[1]);
                let targetColor = new Array(3).fill(scale);

                SU.FadeSpine.executions[spineId] = SU.FadeSpine.setColorFromId(spineId, targetColor, frame);
                if (SU.FadeSpine.onWait) this.wait(frame);
                return;
            case 'showIn':
        }

    }

})(Game_Interpreter.prototype.pluginCommand);