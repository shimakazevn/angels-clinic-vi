//=============================================================================
// RPG Maker MZ - Plugin Analysis Common Base
//=============================================================================
// Version
// 0.1.2 2024/7/4
//=============================================================================
/*:
* @target MZ
* @plugindesc MessageWindowCustomize
* @author DB

 *
 * @command SetMessageWindowBackground
 * @text メッセージ背景画像変更
 * @desc メッセージウィンドウの背景画像（img/system）をゲーム途中で変更します。空欄で背景を消します。
 *
 * @arg fileName
 * @text ファイル名
 * @desc img/system/ のファイル名（拡張子なし）。空欄で背景を消去。
 * @type string
 * @default custom_window
 *
 * @arg visible
 * @text 表示する
 * @desc 背景画像を表示するかどうか。
 * @type boolean
 * @default true
 *
 * @command SetMessageWindowHeight
 * @text メッセージウィンドウ高さ変更
 * @desc メッセージウィンドウの高さをゲーム途中で変更します（次回生成時も維持）。
 *
 * @arg height
 * @text 高さ
 * @type number
 * @min 1
 * @default 300
 *
 * @command SetMessageTextOffset
 * @text テキスト開始位置変更
 * @desc メッセージ本文の開始座標（textState.x,y）をゲーム途中で変更します。
 *
 * @arg startX
 * @text 開始X
 * @type number
 * @default 290
 *
 * @arg startY
 * @text 開始Y
 * @type number
 * @default 92
 *
 * @command ApplyMessageWindowConfig
 * @text 設定を即時反映
 * @desc 現在表示中のメッセージウィンドウに、保存済み設定を即時反映します。
 *
 * @command ResetMessageWindowConfig
 * @text 設定リセット
 * @desc 変更した設定を初期値に戻し、現在のメッセージウィンドウにも反映します。


 * @param backSpriteOffSwiche
 * @text ウィンドウ背景画像消去スイッチ
 * @desc マップやシーンの移行前に、ここで指定したスイッチをONにすると、移行先のメッセージウィンドウ背景画像が消えます。（アイコンと文字は消えません）
 * @default 101
 * @type number
 *
 * @param iconYOffset
 * @text アイコンYオフセット
 * @desc アイコンのY座標の追加オフセット値です。
 * @type number
 * @default 0
 
 *
 * @param bgX
 * @text 背景画像X
 * @desc メッセージ背景画像（カスタム背景スプライト）のX座標（メッセージウィンドウ内のローカル座標）
 * @type number
 * @default 50
 *
 * @param bgY
 * @text 背景画像Y
 * @desc メッセージ背景画像（カスタム背景スプライト）のY座標（メッセージウィンドウ内のローカル座標）
 * @type number
 * @default 0
 *
 * @param iconBaseX
 * @text アイコン基準X
 * @desc アイコンボタン群の基準X座標（左端。メッセージウィンドウ内のローカル座標）
 * @type number
 * @default 542
 *
 * @param iconBaseY
 * @text アイコン基準Y
 * @desc アイコンボタン群の基準Y座標（上端。メッセージウィンドウ内のローカル座標）
 * @type number
 * @default 215
 *
 * @param nameWindowX
 * @text 名前ウィンドウX
 * @desc 名前ウィンドウ（NameBox）のX座標（画面座標）
 * @type number
 * @default 0
 *
 * @param nameWindowY
 * @text 名前ウィンドウY
 * @desc 名前ウィンドウ（NameBox）のY座標（画面座標）
 * @type number
 * @default 0
 *
 * @param textStartXDefault
 * @text 本文開始X(初期)
 * @desc メッセージ本文の開始X座標の初期値（ゲーム中にコマンドで変更可能）
 * @type number
 * @default 290
 *
 * @param textStartYDefault
 * @text 本文開始Y(初期)
 * @desc メッセージ本文の開始Y座標の初期値（ゲーム中にコマンドで変更可能）
 * @type number
 * @default 92

 *
 * @command SetMessageWindowBgPos
 * @text 背景画像座標変更
 * @desc メッセージ背景画像（カスタム背景スプライト）のX/Y座標をゲーム途中で変更します（補正なし、指定値をそのまま使用）。
 *
 * @arg x
 * @text X
 * @type number
 * @default 50
 *
 * @arg y
 * @text Y
 * @type number
 * @default 0
 *
 * @command SetMessageWindowIconPos
 * @text アイコン基準座標変更
 * @desc メッセージウィンドウ内のアイコンボタン群の基準X/Y座標（左上）をゲーム途中で変更します（補正なし、指定値をそのまま使用）。
 *
 * @arg x
 * @text X
 * @type number
 * @default 542
 *
 * @arg y
 * @text Y
 * @type number
 * @default 215
 *
 * @command SetNameWindowPos
 * @text 名前ウィンドウ座標変更
 * @desc 名前ウィンドウ（NameBox）のX/Y座標をゲーム途中で変更します（画面座標、補正なし）。
 *
 * @arg x
 * @text X
 * @type number
 * @default 0
 *
 * @arg y
 * @text Y
 * @type number
 * @default 0
*/

const script = document.currentScript;
const param = PluginManagerEx.createParameter(script);

const ICON_Y_OFFSET = Number(param["iconYOffset"] || 0);

const BG_X = Number(param["bgX"] || 50);
const BG_Y = Number(param["bgY"] || 0);
const ICON_BASE_X = Number(param["iconBaseX"] || 542);
const ICON_BASE_Y = Number(param["iconBaseY"] || 215);
const NAME_WINDOW_X = Number(param["nameWindowX"] || 0);
const NAME_WINDOW_Y = Number(param["nameWindowY"] || 0);
const TEXT_START_X_DEFAULT = Number(param["textStartXDefault"] || 290);
const TEXT_START_Y_DEFAULT = Number(param["textStartYDefault"] || 92);



// クリック可能なスプライトクラスの定義
class CustomSpriteClickable extends Sprite {
    constructor() {
        super();
        this._clickHandler = null;
        this.interactive = true;
        this.buttonMode = true;
        this.on('pointerdown', this.onClick.bind(this));
    }

    setClickHandler(handler) {
        this._clickHandler = handler;
        //console.log("this._clickHandler",this._clickHandler());
    }

    onClick(event) {
        if (this._clickHandler) {
            //console.log("this._clickHandler",this._clickHandler());
            this._clickHandler();
        }
    }

    isTouchInFrame() {
        const x = this.canvasToLocalX(TouchInput.x);
        const y = this.canvasToLocalY(TouchInput.y);

        return x >= 0 && y >= 0 && x < this.width && y < this.height;
    }

    canvasToLocalX(x) {
        let node = this;
        while (node) {
            x -= node.x;
            node = node.parent;
        }
        return x;
    }

    canvasToLocalY(y) {
        let node = this;
        while (node) {
            y -= node.y;
            node = node.parent;
        }
        return y;
    }
}

// メッセージウィンドウのカスタマイズ
(() => {



    const _Window_Message_initialize = Window_Message.prototype.initialize;
    Window_Message.prototype.initialize = function(rect) {

        _Window_Message_initialize.call(this, rect);
        this.createCustomIcons();
        this._autoMessage = false;
        this._autoMessageInterval = 120; // 自動進行の間隔（フレーム数）
        this._autoMessageTimer = 0;
        this._skipMessage = false;
        this._skipMessageInterval = 1; // 自動進行の間隔（フレーム数）
        this._skipMessageTimer = 0;        
        //this.x = Graphics.width / 2 - 600;//ウィンドウそのものの座標。背景と連動してるけど別で調整の必要あり・。・

        
    };

    Window_Message.prototype.updatePlacement = function() {
        const goldWindow = this._goldWindow;
        this._positionType = $gameMessage.positionType();
        this.y = (this._positionType * (Graphics.boxHeight - this.height)) / 2 + 41;//ウィンドウの高さ調整
        if (goldWindow) {
            goldWindow.y = this.y > 0 ? 0 : Graphics.boxHeight - goldWindow.height;
        }
        this.updateCustomIconPositions();

    };

    Window_Message.prototype.createCustomIcons = function() {
        const iconData = [
            //{ name: 'icon_save', clickHandler: this.onSaveIconClick.bind(this) },
            //{ name: 'icon_load', clickHandler: this.onLoadIconClick.bind(this) },
            { name: 'icon_menu', clickHandler: this.onMenuIconClick.bind(this) },
            { name: 'icon_auto', clickHandler: this.onAutoMessageIconClick.bind(this) }, // 新しいアイコンの追加
            { name: 'icon_skip', clickHandler: this.onSkipMessageIconClick.bind(this) }  // 新しいアイコンの追加2            
       
        ];
        this._customIconSprites = [];
        this._iconAutoSprite = null;

        const iconSize = 44;//アイコンのサイズをここ入力 
        const padding = 10;

        iconData.forEach((data, index) => {
            const bitmap = ImageManager.loadBitmap('img/system/', data.name);
            var sizePlus_x = 0; //オートとスキップのアイコンサイズ変更用
            var sizePlus_y = 0; 
            var paddingPlus_x = 0; //アイコンの間隔調整
            var paddingPlus_y = 0; //アイコンの高さ位置調整              

            if (data.name === 'icon_auto' || data.name === 'icon_skip') {
                sizePlus_x = 31; //アイコンのデフォルトサイズとの差を入力
                sizePlus_y = -10; //アイコンのデフォルトサイズとの差を入力
                paddingPlus_x = 33; //アイコンの間隔調整
                paddingPlus_y = 18 //アイコンの高さ位置調整 28変数の中身でアイコン座標の位置がずれる               
            }
 
            const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) ? $gameSystem.dbGetMessageWindowRuntimeConfig() : null;
            const baseX = (cfg && cfg.iconBaseX != null) ? Number(cfg.iconBaseX) : ICON_BASE_X;
            const baseY = (cfg && cfg.iconBaseY != null) ? Number(cfg.iconBaseY) : ICON_BASE_Y;
            var x = baseX + (iconSize + padding + paddingPlus_x) * index; // アイコン基準Xから配置（補正なし）
            var y = baseY + sizePlus_y; // アイコン基準Yから配置（補正なし）
            const sprite = new CustomSpriteClickable();
            sprite.bitmap = new Bitmap(iconSize + sizePlus_x, iconSize + sizePlus_y);                
            bitmap.addLoadListener(() => {
                sprite.bitmap.blt(bitmap, 0, 0, bitmap.width, bitmap.height, 0, 0, iconSize + sizePlus_x, iconSize + sizePlus_y);
            });
            sprite.x = x;
            sprite.y = y + paddingPlus_y;
            sprite.setClickHandler(data.clickHandler);
            sprite.opacity = 0;
            this.addChild(sprite);
            this._customIconSprites.push(sprite);

            if (data.name === 'icon_auto') {
                this._iconAutoSprite = sprite;
            }

            if (data.name === 'icon_skip') {
                this._iconSkipSprite = sprite;

            }
        });
    };

Window_Message.prototype.updateCustomIconPositions = function() {
    if (!this._customIconSprites) return;

    const iconSize = 44;
    const padding = 10;

    this._customIconSprites.forEach((sprite, index) => {
        const name = sprite._bitmapName || ""; // 名前を取得する方法を必要に応じて調整
        let sizePlus_x = 0, sizePlus_y = 0;
        let paddingPlus_x = 0, paddingPlus_y = 0;

        if (index >= 1) { // auto と skip が後ろにあると仮定
            sizePlus_x = 20;
            sizePlus_y = -10;
            paddingPlus_x = 44;
            paddingPlus_y = 18;
        }

        const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) ? $gameSystem.dbGetMessageWindowRuntimeConfig() : null;
        const baseX = (cfg && cfg.iconBaseX != null) ? Number(cfg.iconBaseX) : ICON_BASE_X;
        const baseY = (cfg && cfg.iconBaseY != null) ? Number(cfg.iconBaseY) : ICON_BASE_Y;
        const x = baseX + (iconSize + padding + paddingPlus_x) * index;
        const y = baseY + sizePlus_y + paddingPlus_y;
        sprite.x = x;
        sprite.y = y;
    });
};




    Window_Message.prototype.onSaveIconClick = function() {
        //$gameSystem.onBeforeSave();
        SceneManager.push(Scene_Save);
    };

    Window_Message.prototype.onLoadIconClick = function() {
        SceneManager.push(Scene_Load);
    };

    Window_Message.prototype.onMenuIconClick = function() {
        SceneManager._scene.callTextLog();
    };



//
//フェードイン・フェードアウトを実装中
/*
Window_Base.prototype.update = function() {
    Window.prototype.update.call(this);
    this.updateTone();
    this.updateOpen();
    this.updateClose();
    this.updateBackgroundDimmer();
};
*/  

    Window_Message.prototype.updateOpen = function() {
        if (this._opening) {
            //this.openness += 32;
            this.spriteOpacityToMax(); //代わりに濃くする opacityは効かないので、メソッド作ってそこでspriteの不透明度を操作しようぜ
            if (this.isOpen()) {
                this._opening = false;
            }
        }
    };
    
    Window_Message.prototype.updateClose = function() {
        if (this._closing) {
            //this.openness -= 32;//縮こまる必要はないので消す
            this.spriteOpacityToZero(); //代わりに薄くする opacityは効かないので、メソッド作ってそこでspriteの不透明度を操作しようぜ
            if (this.isClosed()) {
                this._closing = false;
            }
        }
    };



    
    
    
    Window_Message.prototype.spriteOpacityToMax = function() {
        //メッセージウィンドウで使用しているspriteの不透明度を上げる
        //this._customIconSprites
        //this._customBackground
        this._customIconSprites.forEach(sprite => {

            sprite.opacity += 32;
        });
        this._customBackground.opacity += 32;
        this.contents.paintOpacity += 32;
        // 名前ウィンドウのスプライトも上げる
        if (this._nameBoxWindow) {
            this._nameBoxWindow.opacity += 32;
        }        

    };

    Window_Message.prototype.spriteOpacityToZero = function() {
        //メッセージウィンドウで使用しているspriteの不透明度を下げる
        //this._customIconSprites        
        //this._customBackground

        this._customIconSprites.forEach(sprite => {

            sprite.opacity -= 32;
        });             
        
        this._customBackground.opacity -= 32;
        this.contents.paintOpacity -= 32;
        // 名前ウィンドウのスプライトも下げる
        if (this._nameBoxWindow) {
            this._nameBoxWindow.opacity -= 32;
        }  

    };

    Window_Message.prototype.spriteOpacityZero = function() {
        //メッセージウィンドウで使用しているspriteの不透明度を下げる
        //this._customIconSprites        
        //this._customBackground

        this._customIconSprites.forEach(sprite => {
            sprite.opacity = 0;
        });
        this._customBackground.opacity = 0;
        this.contents.paintOpacity = 0;
      

    };    

    Window_Message.prototype.open = function() {
        this.openness = 255; //初めから全開しててね
        //this.spriteOpacityZero(); //ただし不透明度はゼロからよ

        if (!this.isOpen()) {
            this._opening = true;
        }
        this._closing = false;
    };
    
    Window_Message.prototype.close = function() {
        if (!this.isClosed()) {
            this._closing = true;
        }
        
        this._opening = false;
    };
    /*
    Window_Base.prototype.isOpening = function() {
        return this._opening;
    };
    
    Window_Base.prototype.isClosing = function() {
        return this._closing;
    };
    */
    Window_Message.prototype.isOpen = function() {
        //ここでメッセージウィンドウが表示完了したかを判定返す
        //return this._openness >= 255; //デフォルトは判定につかえないので消す
        var i = this._nameBoxWindow.contentsOpacity;
        var unko = false;
        this._customIconSprites.forEach(sprite => {
            if (sprite.opacity < 255) {
                unko = true; 
            }
        });
        if (this._customBackground.opacity < 255){
            if (this._nameBoxWindow && this._opening){
                i += 32;     
                this._nameBoxWindow.updateOpacity(i);
            }
            unko = true; 
        }
        //無理やり名前ウィンドウと結び付けてopenしてるならこっちもopenじゃい
        if (!unko){
            this._nameBoxWindow.updateOpacity(255);

        }
        //全てのspriteが２５５チェックOK
        return !unko;
    };

    Window_Message.prototype.isClosed = function() {
        //ここでメッセージウィンドウが完全透明化したかの判定返す
        //return this._openness <= 0; //デフォルトは判定につかえないので消す
        //this._customIconSprites        
        //const sprite = this._customIconSprites ;//メッセージウィンドウで使用されている画像データ読み込み
        var i = this._nameBoxWindow.contentsOpacity;
        var unko = false;
        this._customIconSprites.forEach(sprite => {
            if (sprite.opacity > 0) {
                unko = true; 
            }
        });
        if (this._customBackground.opacity > 0){
            if (this._nameBoxWindow && this._closing){
                i -= 32;
                this._nameBoxWindow.updateOpacity(i); // 名前ウィンドウ全体を半透明に
            }
            unko = true; 
        }

        //無理やり名前ウィンドウと結び付けてクローズしてるならこっちもクローズじゃい
        if (!unko){
            this._nameBoxWindow.updateOpacity(0);
        }
        return !unko;
    };

//名前部分をもどせ

Window_NameBox.prototype._refreshFrame = function() {
    const w = this._width;
    const h = this._height;
    const m = 24; // フレームの幅

    const bitmap = new Bitmap(1, 1);//強制ビットマップからっぽ
    const sprite = this._frameSprite;
    const frameBitmap = new Bitmap(w, h);

    // フレーム画像の描画（左上部分を読み取る）
    const sx = 0; const sy = 0; const sw = m; const sh = m; // ウィンドウスキン左上
    frameBitmap.blt(bitmap, sx, sy, sw, sh, 0, 0, m, m); // 上左のフレーム部分を描画

    // 同様に他の部分も描画していく...

    sprite.bitmap = frameBitmap;
};


Window_NameBox.prototype.initialize = function() {
    Window_Base.prototype.initialize.call(this, new Rectangle());
    this.openness = 0;
    this._name = "";
    this.opacity = 0;
    this.frameOpacity = 0;
    this.updateOpacity(0);
};


Window_NameBox.prototype.updateOpacity = function(opacity) {
    //this.opacity = opacity;               // ウィンドウフレームの透明度
    this.contentsOpacity = opacity;      // ビットマップの透明度
    this.frameOpacity = 0;
};










    // オートアイコンのクリック処理を変更して、MessageSkip.jsのオート機能を使用
Window_Message.prototype.onAutoMessageIconClick = function() {
    $gameMessage._skipFlg = false;      
    $gameMessage.toggleAuto();  // MessageSkip.jsのオート機能を呼び出す  
  
};
/*
    // オートアイコンのクリック処理
    Window_Message.prototype.onAutoMessageIconClick = function() {
        this._autoMessage = !this._autoMessage;
        if (this._autoMessage) {
            this._autoMessageTimer = this._autoMessageInterval;
            this._skipMessage = false; // スキップ機能を停止
            this.changeSkipIcon(false); // スキップアイコン画像を戻す
        }
        this.changeAutoIcon(this._autoMessage);
    };


    Window_Message.prototype.changeAutoIcon = function(isAuto) {
        const iconName = isAuto ? 'icon_auto2' : 'icon_auto';
        const bitmap = ImageManager.loadBitmap('img/system/', iconName);
        const sprite = this._iconAutoSprite;
        if (sprite) {
            sprite.bitmap.clear();
            bitmap.addLoadListener(() => {
                sprite.bitmap.blt(bitmap, 0, 0, bitmap.width, bitmap.height, 0, 0, sprite.width, sprite.height);
            });
        }
    };
    */

    Window_Message.prototype.changeAutoIcon = function(isAuto) {

        const iconName = $gameMessage._autoFlg ? 'icon_auto2' : 'icon_auto';  // オート状態によってアイコンを切り替える
        const bitmap = ImageManager.loadBitmap('img/system/', iconName);
        const sprite = this._iconAutoSprite;
        if (sprite) {
            sprite.bitmap.clear();
            bitmap.addLoadListener(() => {
                sprite.bitmap.blt(bitmap, 0, 0, bitmap.width, bitmap.height, 0, 0, sprite.width, sprite.height);
            });
        }
    };


// スキップアイコンのクリック処理を変更して、MessageSkip.jsのスキップ機能を使用
Window_Message.prototype.onSkipMessageIconClick = function() {
    $gameMessage._autoFlg = false;  
    $gameMessage.toggleSkip();  // MessageSkip.jsのスキップ機能を呼び出す  


};
/*
    // スキップアイコンのクリック処理
    Window_Message.prototype.onSkipMessageIconClick = function() {
        this._skipMessage = !this._skipMessage;
        if (this._skipMessage) {
            this._skipMessageTimer = this._skipMessageInterval;
            this._autoMessage = false; // オート機能を停止
            this.changeAutoIcon(false); // オートアイコン画像を戻す
        }
        this.changeSkipIcon(this._skipMessage);
    };

    Window_Message.prototype.changeSkipIcon = function(isSkip) {
        const iconName = isSkip ? 'icon_skip2' : 'icon_skip';
        const bitmap = ImageManager.loadBitmap('img/system/', iconName);
        const sprite = this._iconSkipSprite;
        if (sprite) {
            sprite.bitmap.clear();
            bitmap.addLoadListener(() => {
                sprite.bitmap.blt(bitmap, 0, 0, bitmap.width, bitmap.height, 0, 0, sprite.width, sprite.height);
            });
        }
    };
    */

    Window_Message.prototype.changeSkipIcon = function(isSkip) {
        const iconName = $gameMessage._skipFlg ? 'icon_skip2' : 'icon_skip';  // スキップ状態によってアイコンを切り替える
        const bitmap = ImageManager.loadBitmap('img/system/', iconName);
        const sprite = this._iconSkipSprite;
        if (sprite) {
            sprite.bitmap.clear();
            bitmap.addLoadListener(() => {
                sprite.bitmap.blt(bitmap, 0, 0, bitmap.width, bitmap.height, 0, 0, sprite.width, sprite.height);
            });
        }
    };

Window_Message.prototype.isCustomSkipIconPressed = function() {
    const sprite = this._iconSkipSprite;
    if (!sprite) return false;
    return sprite.visible && sprite.isTouchInFrame() && TouchInput.isPressed();
};


    const _Window_Message_update = Window_Message.prototype.update;
    Window_Message.prototype.update = function() {
        _Window_Message_update.call(this);
        //console.log("SceneManager._scene._messageWindow",SceneManager._scene._messageWindow);
        this.updateAutoMessage();
        this.updateSkipMessage();        

    };

    Window_Message.prototype.updateAutoMessage = function() {
        if (this._autoMessage) {
            this._autoMessageTimer -= 1;
            if (this._autoMessageTimer <= 0) {
                this._autoMessageTimer = this._autoMessageInterval;
                this.onAutoMessageTimer();
            }
        }
    };

    Window_Message.prototype.updateSkipMessage = function() {
        if (this._skipMessage) {
            this._skipMessageTimer -= 1;
            if (this._skipMessageTimer <= 0) {
                this._skipMessageTimer = this._skipMessageInterval;
                this.onSkipMessageTimer();
            }
        }
    };

    Window_Message.prototype.onAutoMessageTimer = function() {
        this.pause = false;
        if (!this._textState) {
            this.terminateMessage();
        }
    };

    Window_Message.prototype.onSkipMessageTimer = function() {
        this.pause = false;
        if (!this._textState) {
            this.terminateMessage();
        }
    };    

    const _Window_Message_updateInput = Window_Message.prototype.updateInput;
    Window_Message.prototype.updateInput = function() {
        if (this.isOpen() && TouchInput.isTriggered()) {
            for (const sprite of this._customIconSprites) {
                if (sprite.isTouchInFrame()) {
                    sprite.onClick();
                    return true; // メッセージの進行を停止
                }
            }
            this._autoMessage = false; // オートフラグリセット
            this._autoMessageTimer = this._autoMessageInterval; // オートカウントリセット
            this._skipMessage = false; // スキップフラグリセット
            this._skipMessageTimer = this._skipMessageInterval; // オートカウントリセット            
            this.changeAutoIcon(false); // オートアイコンの色をリセット
            this.changeSkipIcon(false); // スキップアイコンの色をリセット
        }
        return _Window_Message_updateInput.call(this);
    };







    Window_NameBox.prototype.windowWidth = function() {
        if (this._name) {
            return 500; //改造
            const textWidth = this.textSizeEx(this._name).width;
            const padding = this.padding + this.itemPadding();
            const width = Math.ceil(textWidth) + padding * 2;
            return Math.min(width, Graphics.boxWidth);
        } else {
            this.openness = 0;//なまえなし
            return 300;
        }
    };

    Window_NameBox.prototype.updateBackground = function() {

        // 背景スプライトを初期化
        if (!this._backgroundSprite) {
            this._backgroundSprite = new Sprite();
            this.addChildToBack(this._backgroundSprite);
        }

        // 名前欄のテキストを取得
        const nameBoxText = $gameMessage.speakerName();
        
        
        //魔改造
        this._backgroundSprite.bitmap = new Bitmap(0, 0);
        this._backgroundSprite.visible = false;
        
/*
        // 名前欄が空の場合、独自の背景画像を表示
        if (!nameBoxText || nameBoxText.trim() === '') {
            this._backgroundSprite.bitmap = new Bitmap(0, 0);
            this._backgroundSprite.visible = false;
        } else {
            const bitmap = ImageManager.loadBitmap('img/system/', 'icon_name');
            bitmap.addLoadListener(() => {
                this._backgroundSprite.bitmap = bitmap;
                this._backgroundSprite.visible = true;
            });
        }
*/        

    };

    Window_NameBox.prototype._refreshBack = function() {

        return;
        const m = this._margin;
        const w = Math.max(0, this._width - m * 2);
        const h = Math.max(0, this._height - m * 2);
        const sprite = this._backSprite;
        const tilingSprite = sprite.children[0];
        // [Note] We use 95 instead of 96 here to avoid blurring edges.
        sprite.bitmap = this._windowskin;
        sprite.setFrame(0, 0, 95, 95);
        sprite.move(m, m);
        sprite.scale.x = w / 95;
        sprite.scale.y = h / 95;
        tilingSprite.bitmap = this._windowskin;
        tilingSprite.setFrame(0, 96, 96, 96);
        tilingSprite.move(0, 0, w, h);
        tilingSprite.scale.x = 1 / sprite.scale.x;
        tilingSprite.scale.y = 1 / sprite.scale.y;
        sprite.setColorTone(this._colorTone);
    };


    Window_NameBox.prototype.refresh = function() {

        const rect = this.baseTextRect();
        this.contents.clear();
        //console.log("this._name",this._name);        
        var namelen = this.drawTextExlength(this._name);
        //console.log("namelen",namelen);
        //this.drawTextEx(this._name, this.width / 2 - (namelen.length * 24) / 2  - 36, rect.y + 4, rect.width);
        this.drawTextEx(this._name, this.width / 2 - 66, rect.y + 4, rect.width);
    };

    Window_NameBox.prototype.drawTextExlength = function(text) {
        //console.log("tekisutoha:",text);
        const textState = this.convertEscapeCharacters(text);
        return textState;
    };

// Game_Map クラスに保存用メソッドを追加
Game_Map.prototype.saveInterpreterState = function(interpreter) {
    if (!interpreter) {
        return null;
    }
    const state = {
        index: interpreter._index,
        list: interpreter._list ? interpreter._list.slice() : [],
        eventId: interpreter._eventId,
        waitMode: interpreter._waitMode,
        isRunning: interpreter.isRunning(),
        childInterpreter: this.saveInterpreterState(interpreter._childInterpreter)
    };

    return state;
};

Game_Map.prototype.saveCommonEventState = function() {
    const commonEvents = $gameMap._commonEvents.filter(commonEvent => commonEvent._interpreter && commonEvent._interpreter.isRunning());
    const state = commonEvents.map(commonEvent => {
        return {
            id: commonEvent._commonEventId,
            interpreter: this.saveInterpreterState(commonEvent._interpreter)
        };
    });

    return state;
};








Scene_Map.prototype.initialize = function() {
    //console.log("initialize");

    //ちょいすプラグインチェック
    this.checkSelectWindowMessage($gameMap._interpreter);        

    Scene_Message.prototype.initialize.call(this);
    this._waitCount = 0;
    this._encounterEffectDuration = 0;
    this._mapLoaded = false;
    this._touchCount = 0;
    this._menuEnabled = false;
};





Scene_Map.prototype.checkSelectWindowMessage = function(checkInterpre){
    if(!checkInterpre || !checkInterpre._list) return;
    // guard: index might be out of range when returning from other scenes
    const list = checkInterpre._list;
    const idx = checkInterpre._index;
    if(!list || idx == null || idx < 0 || idx >= list.length) return;
    if(!list[idx] || list[idx].code == null) return;
    {
    const cmd = (i)=> (list && i>=0 && i<list.length)? list[i] : null;
        
        //（ここバグ）
        
        if(cmd(checkInterpre._index) && cmd(checkInterpre._index).code == 657){
          
            checkInterpre._index -= 1;

            if(cmd(checkInterpre._index) ? cmd(checkInterpre._index).code : null== 357){
                 
                checkInterpre._index -= 1;

                if(cmd(checkInterpre._index) ? cmd(checkInterpre._index).code : null == 121){

                    checkInterpre._index -= 1;
                    
                    while (cmd(checkInterpre._index) ? cmd(checkInterpre._index).code : null == 401) {
                        $gameMessage._galgeChoices = [];

                        checkInterpre._index -= 1;
                    }



                }
            }
        };
    }

    if (checkInterpre._childInterpreter) {
        //console.log("checkInterpre._childInterpreterはあるよ");
        this.checkSelectWindowMessage(checkInterpre._childInterpreter);
    }      

}


Game_Map.prototype.loadInterpreterState = function(interpreter, state) {
    if (state) {

        interpreter.clear();
        interpreter.setup(state.list, state.eventId);
        interpreter._index = state.index;

      if(state.list.length > 0){
        //ちょいすプラグイン対応（ここバグ怖い）
        if(state.list[interpreter._index].code == 657){
            interpreter._index -= 1;
            state.index -= 1;

            if(state.list[interpreter._index].code == 357){

                state.index -= 1;
                interpreter._index -= 1;
                if(state.list[interpreter._index].code == 121){

                    interpreter._index -= 1;
                    state.index -= 1;
                    
                    while (state.list[interpreter._index].code == 401) {

                        interpreter._index -= 1;
                        state.index -= 1;
                    }



                }
            }
        };
      };
        interpreter._waitMode = state.waitMode;
        if (state.childInterpreter) {
            interpreter._childInterpreter = new Game_Interpreter();
            this.loadInterpreterState(interpreter._childInterpreter, state.childInterpreter);
        }      
       
    }
};

Game_Map.prototype.loadCommonEventState = function(state) {
    state.forEach(eventState => {
        const commonEvent = $gameMap._commonEvents.find(ce => ce._commonEventId === eventState.id);
        if (commonEvent && eventState.interpreter) {
            this.loadInterpreterState(commonEvent._interpreter, eventState.interpreter);
        }
    });
    this.refreshTileEvents(); // イベントの状態を更新
};



















// Game_CommonEvent クラスの修正
function Game_CommonEvent() {
    this.initialize(...arguments);
}

Game_CommonEvent.prototype.initialize = function(commonEventId) {
    this._commonEventId = commonEventId;
    this.refresh();
};

Game_CommonEvent.prototype.refresh = function() {
    const commonEvent = $dataCommonEvents[this._commonEventId];
    if (commonEvent) {
        if (this._interpreter) {
            this._interpreter.clear();
        } else {
            this._interpreter = new Game_Interpreter();
        }
        this._interpreter.setup(commonEvent.list);
    } else {
        this._interpreter = null;
    }
};

Game_CommonEvent.prototype.isActive = function() {
    const commonEvent = $dataCommonEvents[this._commonEventId];
    return commonEvent && $gameSwitches.value(commonEvent.switchId);
};

Game_CommonEvent.prototype.update = function() {
    if (this.isActive()) {
        this._interpreter.update();
    }
};

// 実行中のコモンイベントを探し出すメソッドを追加
Game_Map.prototype.findRunningCommonEvents = function() {
    const runningCommonEvents = [];
    const interpreters = this._interpreter ? [this._interpreter].concat(this._interpreter._childInterpreters) : [];
    interpreters.forEach(interpreter => {
        if(!interpreter){return};
        const eventId = interpreter.eventId();
        if (eventId > 0) {
            const event = $dataCommonEvents[eventId];
            if (event) {
                runningCommonEvents.push({
                    id: eventId,
                    interpreter: interpreter
                });
            }
        }
    });
    // Common event queue from Game_Temp
    $gameTemp._commonEventQueue.forEach(eventId => {
        const event = $dataCommonEvents[eventId];
        if (event) {
            runningCommonEvents.push({
                id: eventId,
                interpreter: null // 直接のインタープリターはなし
            });
        }
    });
    return runningCommonEvents;
};

// デバッグ用に実行中のコモンイベントの情報をログに出力
Game_Map.prototype.logRunningCommonEvents = function() {
  
    const runningCommonEvents = this.findRunningCommonEvents();

    runningCommonEvents.forEach((commonEvent, index) => {
        if (commonEvent.interpreter) {
            console.log(`Common Event ${index}:`, {
                id: commonEvent.id,
                interpreter: {
                    index: commonEvent.interpreter._index,
                    list: commonEvent.interpreter._list,
                    eventId: commonEvent.interpreter._eventId,
                    waitMode: commonEvent.interpreter._waitMode,
                    isRunning: commonEvent.interpreter.isRunning()
                }
            });
        } else {
            console.log(`Common Event ${index} (queued):`, {
                id: commonEvent.id
            });
        }
    });
};

// Game_System クラスの saveMessageState を修正
Game_System.prototype.saveMessageState = function() {
    const message = $gameMessage;
    const interpreter = $gameMap._interpreter;
    $gameMap.logRunningCommonEvents(); // デバッグ用ログの追加
    this._savedMessageState = {
        allText: message.allText(),
        choices: message._choices,
        choiceCallback: message._choiceCallback,
        background: message._background,
        positionType: message._positionType,
        faceName: message._faceName,
        faceIndex: message._faceIndex,
        text: message._texts ? message._texts.slice() : [],
        windowSkin: message._windowSkin,
        nameBoxText: message._speakerName,
        nameBoxColor: message._nameBoxColor,
        interpreterState: $gameMap.saveInterpreterState(interpreter),
        commonEvents: $gameMap.saveCommonEventState() // コモンイベントの状態を保存
    };

};

// Game_System クラスの loadMessageState を修正
Game_System.prototype.loadMessageState = function() {
    if (this._savedMessageState) {
        const state = this._savedMessageState;
        const message = $gameMessage;
        message.clear();
        message._texts = state.text.slice();
        message._choices = state.choices;
        message._choiceCallback = state.choiceCallback;
        message._background = state.background;
        message._positionType = state.positionType;
        message._faceName = state.faceName;
        message._faceIndex = state.faceIndex;
        message._windowSkin = state.windowSkin;
        message._speakerName = state.nameBoxText;
        message._nameBoxColor = state.nameBoxColor;
        // インタープリターの状態を復元
        $gameMap.loadInterpreterState($gameMap._interpreter, state.interpreterState);

        // コモンイベントの状態を復元
        $gameMap.loadCommonEventState(state.commonEvents);

        $gameMap.logRunningCommonEvents(); // デバッグ用ログの追加
        this._savedMessageState = null;
    }
};


// セーブやロード時の状態管理を引き続き行います
const _Game_System_onBeforeSave = Game_System.prototype.onBeforeSave;
Game_System.prototype.onBeforeSave = function() {
    _Game_System_onBeforeSave.call(this);
    this.saveMessageState();
};

const _Game_System_onAfterLoad = Game_System.prototype.onAfterLoad;
Game_System.prototype.onAfterLoad = function() {
    _Game_System_onAfterLoad.call(this);
    this.loadMessageState();
};

const _Scene_Load_onLoadSuccess = Scene_Load.prototype.onLoadSuccess;
Scene_Load.prototype.onLoadSuccess = function() {
    _Scene_Load_onLoadSuccess.call(this);
    $gameSystem.loadMessageState();
    $gameSystem._savedMessageState = null;
};

const _Scene_Save_onSaveSuccess = Scene_Save.prototype.onSaveSuccess;
Scene_Save.prototype.onSaveSuccess = function() {
    _Scene_Save_onSaveSuccess.call(this);
    $gameSystem._savedMessageState = null;
};

const _Scene_Save_onCancel = Scene_Save.prototype.onCancel;
Scene_Save.prototype.onCancel = function() {
    _Scene_Save_onCancel.call(this);
    $gameSystem.loadMessageState();
    $gameSystem._savedMessageState = null;
};

const _SceneManager_pop = SceneManager.pop;
SceneManager.pop = function() {
    _SceneManager_pop.call(this);
    if (this._stack.length > 0 && this._stack[this._stack.length - 1] === Scene_Map) {
        $gameSystem.loadMessageState();
        $gameSystem._savedMessageState = null;
    }
};

// コモンイベントの状態を適切に復元するためにイベントリフレッシュ
const _Game_Map_setupEvents = Game_Map.prototype.setupEvents;
Game_Map.prototype.setupEvents = function() {
    _Game_Map_setupEvents.call(this);
    if (this._savedCommonEventState) {
        this.loadCommonEventState(this._savedCommonEventState);
        this._savedCommonEventState = null;
    }
};


    const _Window_Message_terminateMessage = Window_Message.prototype.terminateMessage;
    Window_Message.prototype.terminateMessage = function() {
        _Window_Message_terminateMessage.call(this);
        if ($gameSystem._savedMessageState) {
            $gameSystem.loadMessageState();
        }
    };


//並列処理イベントの終了（terminate）が、メッセージ関係のフラグリセットに影響しないように作成
    Game_Interpreter.prototype.getrunnningevent = function() {

            const events = $gameMap.events();
            let isNonParallelEventRunning = false;
        
            // 現在のイベントインタープリターを取得
            const interpreter = $gameMap._interpreter;
        
            for (const event of events) {
                const page = event.page();
                if (page) {
                    const trigger = page.trigger;
                    // 並列処理以外のトリガー（0: トリガー起動, 1: プレイヤー接触, 2: イベント接触, 3: 自動実行）
                    if (trigger !== 4) {
                        // 現在のイベントIDとインタープリターのイベントIDを比較
                        if (interpreter.eventId() === event.eventId() && interpreter.isRunning()) {
                            isNonParallelEventRunning = true;
                            break;
                        }
                    }
                }
            }
        
            if (isNonParallelEventRunning) {
                return true;
            } else {
                return false;
            }

    }
    
    


    const _Game_Interpreter_update = Game_Interpreter.prototype.update;
    Game_Interpreter.prototype.update = function() {
        if ($gameSystem._savedMessageState) {
            $gameSystem.loadMessageState();
        }
        _Game_Interpreter_update.call(this);
    };

    const _Window_Message_updateWait = Window_Message.prototype.updateWait;
    Window_Message.prototype.updateWait = function() {
        if ($gameSystem._savedMessageState) {
            return true;
        }
        return _Window_Message_updateWait.call(this);
    };

})();












(function() {
    // ログを管理するグローバル変数を追加
    const globalMessageLog = [];

    const _Window_Message_terminateMessageLog = Window_Message.prototype.terminateMessage;
    Window_Message.prototype.terminateMessage = function() {
        const text = this.convertEscapeCharacters($gameMessage.allText());
        globalMessageLog.push(text);

        _Window_Message_terminateMessageLog.call(this);
    };

    Window_Message.prototype.getMessageLog = function() {

        return globalMessageLog;
    };
})();

// ログメッセージウィンドウのスクリプト
function Window_MessageLog() {
    this.initialize(...arguments);
}

Window_MessageLog.prototype = Object.create(Window_Base.prototype);
Window_MessageLog.prototype.constructor = Window_MessageLog;

Window_MessageLog.prototype.initialize = function(rect) {
    Window_Base.prototype.initialize.call(this, rect);
    this._scrollY = 0;
    this._maxScrollY = 0;
    this.setScrollEventHandlers(); // スクロールイベントハンドラの設定を追加
    this.refresh();
};

Window_MessageLog.prototype.setScrollEventHandlers = function() {
    // マウスホイールイベントのリスナーを追加
    this._onWheelHandler = this.onWheel.bind(this);
    window.addEventListener('wheel', this._onWheelHandler);
};

Window_MessageLog.prototype.removeScrollEventHandlers = function() {
    // マウスホイールイベントのリスナーを削除
    window.removeEventListener('wheel', this._onWheelHandler);
};

Window_MessageLog.prototype.onWheel = function(event) {
    // ホイールのスクロール量に基づいてスクロール方向を決定
    if (event.deltaY < 0) {
        this.scrollUp();
    } else {
        this.scrollDown();
    }
};

Window_MessageLog.prototype.refresh = function() {
    this.contents.clear();
    const logs = SceneManager._scene._messageWindow.getMessageLog();

    let y = -this._scrollY;
    let totalHeight = 0; // ログ全体の高さを計算するための変数
    for (const log of logs) {

        this.drawTextEx(log, 0, y);
        const lineCount = log.split('\n').length; // メッセージ内の改行の数をカウント
        const logHeight = this.lineHeight() * lineCount + this.lineHeight(); // メッセージの高さ
        y += logHeight; // y座標を更新
        totalHeight += logHeight; // 総高さを更新
    }

    // 全体が収まるようにスクロールの最大値を設定
    this._maxScrollY = Math.max(0, totalHeight - this.contents.height);
};

Window_MessageLog.prototype.update = function() {
    Window_Base.prototype.update.call(this);
    this.processHandling();
};

Window_MessageLog.prototype.processHandling = function() {
    if (this.isOpenAndActive()) {
        if (Input.isRepeated('up')) {
            this.scrollUp();
        }
        if (Input.isRepeated('down')) {
            this.scrollDown();
        }
    }
};

Window_MessageLog.prototype.scrollUp = function() {
    this._scrollY = Math.max(0, this._scrollY - this.lineHeight());
    this.refresh();
};

Window_MessageLog.prototype.scrollDown = function() {
    this._scrollY = Math.min(this._maxScrollY, this._scrollY + this.lineHeight());
    this.refresh();
};

Window_MessageLog.prototype.isOpenAndActive = function() {
    return this.isOpen() && this.active;
};

Window_MessageLog.prototype.hide = function() {
    Window_Base.prototype.hide.call(this);
    this.removeScrollEventHandlers(); // ウィンドウが隠れたときにイベントハンドラを削除
};

Window_MessageLog.prototype.show = function() {
    Window_Base.prototype.show.call(this);
    this.setScrollEventHandlers(); // ウィンドウが表示されたときにイベントハンドラを設定
};


Scene_Map.prototype.createMessageLogWindow = function() {
    const rect = this.messageLogWindowRect();
    this._messageLogWindow = new Window_MessageLog(rect);
    this.addWindow(this._messageLogWindow);
    this._messageLogWindow.hide();
};

Scene_Map.prototype.messageLogWindowRect = function() {
    const ww = Graphics.boxWidth;
    const wh = Graphics.boxHeight / 2;
    const wx = 0;
    const wy = Graphics.boxHeight / 2;
    return new Rectangle(wx, wy, ww, wh);
};

const _Scene_Map_update = Scene_Map.prototype.update;
Scene_Map.prototype.update = function() {
    _Scene_Map_update.call(this);
    if (Input.isTriggered('L')) {
        this.toggleMessageLogWindow();
    }
    if (this._messageLogWindow && this._messageLogWindow.visible) {
        this._messageLogWindow.processHandling();
    }
};

Scene_Map.prototype.toggleMessageLogWindow = function() {
    if (this._messageLogWindow.visible) {
        this._messageLogWindow.hide();
        this._messageLogWindow.deactivate();
    } else {
        this._messageLogWindow.refresh();
        this._messageLogWindow.show();
        this._messageLogWindow.activate();

    }
};

Input.keyMapper[76] = 'L'; // 'L'キー





/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//メッセージウィンドウの背景を透明にする
Window_Message.prototype.setBackgroundType = function(type) {
    this.opacity = 0;
    this.hideBackgroundDimmer();
};

Window_Message.prototype.newPage = function(textState) {
    this.contents.clear();
    this.resetFontSettings();
    this.clearFlags();
    this.updateSpeakerName();
    this.loadMessageFace();
    const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) ? $gameSystem.dbGetMessageWindowRuntimeConfig() : null;
    const sx = (cfg && cfg.textStartX != null) ? Number(cfg.textStartX) : 290;
    const sy = (cfg && cfg.textStartY != null) ? Number(cfg.textStartY) : 92;
    textState.startX = sx;//追加。ここでテキストの開始ｘ座標を変更してる。
    textState.x = sx;
    textState.y = sy;
    textState.height = this.calcTextHeight(textState);
};


    Window_Message.prototype.createCustomBackground = function() {
        const swnum = param.backSpriteOffSwiche;
        this._customBackground = new Sprite();

        if ($gameSwitches.value(swnum)) {
            this._customBackground.bitmap = new Bitmap(0, 0);
            this._customBackground.visible = false;
        } else {
            this._customBackground.bitmap = ImageManager.loadSystem(ClearBackgroundPlugin.dbGetCurrentBackgroundFile());
        }

        // 背景スプライトを最背面に追加
        this.addChildToBack(this._customBackground);

        // 背景スプライトの位置とサイズを設定
        const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) ? $gameSystem.dbGetMessageWindowRuntimeConfig() : null;
        this._customBackground.x = (cfg && cfg.bgX != null) ? Number(cfg.bgX) : BG_X;
        this._customBackground.y = (cfg && cfg.bgY != null) ? Number(cfg.bgY) : BG_Y;
        this._customBackground.width = this.width;
        this._customBackground.height = this.height;
    };








    (function() {
        // 既存の Window_Message の initialize メソッドを保持
        const _Window_Message_initialize = Window_Message.prototype.initialize;
    
        Window_Message.prototype.initialize = function(rect) {
            // rect を書き換える
            const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) ? $gameSystem.dbGetMessageWindowRuntimeConfig() : null;
            const wh = (cfg && cfg.height != null) ? Number(cfg.height) : 300;
            rect = new Rectangle(0, 0, Graphics.width, wh);
            _Window_Message_initialize.call(this, rect);
            this.createCustomBackground();
        };
    
        Window_Message.prototype.createCustomBackground = function() {
            const swnum = param.backSpriteOffSwiche;
    
            this._customBackground = new Sprite();
    
            if ($gameSwitches.value(swnum)) {
                this._customBackground.bitmap = new Bitmap(0, 0);
                this._customBackground.visible = false;
            } else {
                this._customBackground.bitmap = ImageManager.loadSystem(ClearBackgroundPlugin.dbGetCurrentBackgroundFile());
            }
    
            // 背景スプライトを最背面に追加
            this.addChildToBack(this._customBackground);
    
            // 背景スプライトの位置とサイズを設定
            const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) ? $gameSystem.dbGetMessageWindowRuntimeConfig() : null;
            this._customBackground.x = (cfg && cfg.bgX != null) ? Number(cfg.bgX) : BG_X;
            this._customBackground.y = (cfg && cfg.bgY != null) ? Number(cfg.bgY) : BG_Y;
            this._customBackground.opacity = 0;
            this._customBackground.width = this.width;
            this._customBackground.height = this.height;
        };
    
        //startじゃないとマップが読み込めてないのでメッセージに反映できない
        Scene_Map.prototype.start = function() {
            Scene_Message.prototype.start.call(this);
            if($gameSystem._backgroundOppacityFlag != true){
      
            }else{
     
                ClearBackgroundPlugin.clearMessageWindowBackground();
            };        


            SceneManager.clearStack();
            if (this._transfer) {
                this.fadeInForTransfer();
                this.onTransferEnd();
            } else if (this.needsFadeIn()) {
                this.startFadeIn(this.fadeSpeed(), false);
            }
            this.menuCalling = false;
        };
        
        // グローバル関数としてプラグインを定義
        window.ClearBackgroundPlugin = window.ClearBackgroundPlugin || {};
    
        ClearBackgroundPlugin.clearMessageWindowBackground = function() {

            const sceneMap = SceneManager._scene;
            const messageWindow = sceneMap._messageWindow;


            if (messageWindow && messageWindow._customBackground) {
                messageWindow._customBackground.bitmap = new Bitmap(messageWindow.width, messageWindow.height);
                messageWindow._customBackground.visible = false;
                

                $gameSystem._backgroundOppacityFlag = true;
            }
        };
    
        ClearBackgroundPlugin.restoreMessageWindowBackground = function() {
            if (SceneManager._scene instanceof Scene_Map) {
                const sceneMap = SceneManager._scene;
                const messageWindow = sceneMap._messageWindow;
    
                if (messageWindow && messageWindow._customBackground) {
                    messageWindow._customBackground.bitmap = ImageManager.loadSystem(ClearBackgroundPlugin.dbGetCurrentBackgroundFile());
                    messageWindow._customBackground.visible = true;
                    $gameSystem._backgroundOppacityFlag = false;

                    messageWindow.setBackgroundType(0);
                    messageWindow.opacity = 255;
                }
            }
        };
    
        // 既存の WindowLayer の render メソッドを保持
        const _WindowLayer_render = WindowLayer.prototype.render;
    
        WindowLayer.prototype.render = function(renderer) {
            if (!this.visible) {
                return;
            }
    
            const graphics = new PIXI.Graphics();
            const gl = renderer.gl;
            const nameBoxWindows = [];
            const otherWindows = [];
            this.children.forEach(child => {
                if (child instanceof Window_NameBox) {
                    nameBoxWindows.push(child);
                } else {
                    otherWindows.push(child);
                }
            });
    
            const children = otherWindows.concat(nameBoxWindows);
            renderer.framebuffer.forceStencil();
            graphics.transform = this.transform;
            renderer.batch.flush();
            gl.enable(gl.STENCIL_TEST);
    
            for (const win of children) {
                if (win._isWindow && win.visible && win.openness > 0) {
                    //console.log("Rendering window:", win.constructor.name, win);
                    gl.stencilFunc(gl.EQUAL, 0, ~0);
                    gl.stencilOp(gl.KEEP, gl.KEEP, gl.KEEP);
                    win.render(renderer);
                    renderer.batch.flush();
                    graphics.clear();
    
                    //win.drawShape(graphics);
                    gl.stencilFunc(gl.ALWAYS, 1, ~0);
                    gl.stencilOp(gl.REPLACE, gl.REPLACE, gl.REPLACE);
                    gl.blendFunc(gl.ZERO, gl.ONE);
                    graphics.render(renderer);
                    renderer.batch.flush();
                    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
                }
            }
    
            gl.disable(gl.STENCIL_TEST);
            gl.clear(gl.STENCIL_BUFFER_BIT);
            gl.clearStencil(0);
            renderer.batch.flush();
    
            for (const child of this.children) {
                if (!child._isWindow && child.visible) {
                    //console.log("Rendering child:", child.constructor.name, child);
                    child.render(renderer);
                }
            }
    
            renderer.batch.flush();
        };
    })();
    

//=============================================================================
// 追加機能：ゲーム途中でメッセージウィンドウ設定（背景画像/高さ/テキスト開始位置）を変更
//=============================================================================
(function() {
    // --- Game_System に設定を保持（セーブに含まれる） ---
    const DEFAULT_CFG = {
        backgroundFile: "custom_window", // img/system/
        backgroundVisible: true,
        height: 300,
        // 本文開始位置
        textStartX: TEXT_START_X_DEFAULT,
        textStartY: TEXT_START_Y_DEFAULT,
        // 各要素の座標（補正なし：そのまま使用）
        bgX: BG_X,
        bgY: BG_Y,
        iconBaseX: ICON_BASE_X,
        iconBaseY: ICON_BASE_Y,
        nameWindowX: NAME_WINDOW_X,
        nameWindowY: NAME_WINDOW_Y
    };

    Game_System.prototype.dbGetMessageWindowRuntimeConfig = function() {
        if (!this._dbMessageWindowRuntimeConfig) {
            this._dbMessageWindowRuntimeConfig = Object.assign({}, DEFAULT_CFG);
        }
        return this._dbMessageWindowRuntimeConfig;
    };

    Game_System.prototype.dbResetMessageWindowRuntimeConfig = function() {
        this._dbMessageWindowRuntimeConfig = Object.assign({}, DEFAULT_CFG);
    };

    // --- 背景ファイル名の取得（既存 ClearBackgroundPlugin からも使う） ---
    window.ClearBackgroundPlugin = window.ClearBackgroundPlugin || {};

    ClearBackgroundPlugin.dbGetCurrentBackgroundFile = function() {
        const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig)
            ? $gameSystem.dbGetMessageWindowRuntimeConfig()
            : DEFAULT_CFG;
        const name = (cfg && typeof cfg.backgroundFile === "string") ? cfg.backgroundFile.trim() : "";
        return name || "custom_window";
    };


    // 現在のメッセージウィンドウに反映する（即時反映）
    
    // --- Apply runtime positions (no "follow offset" correction; use exact coordinates) ---
    // This function must exist because updatePlacement hook calls it.
    function applyOffsets(win) {
        if (!win) return;
        const cfg = ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig)
            ? $gameSystem.dbGetMessageWindowRuntimeConfig()
            : null;

        // Background sprite (inside message window local coords)
        if (win._customBackground && cfg) {
            if (cfg.bgX != null) win._customBackground.x = Number(cfg.bgX);
            if (cfg.bgY != null) win._customBackground.y = Number(cfg.bgY);
        }

        // Custom icon sprites: rely on updateCustomIconPositions which uses iconBaseX/iconBaseY
        if (win.updateCustomIconPositions) {
            try { win.updateCustomIconPositions(); } catch (e) { /* ignore */ }
        }

        // NameBox: its updatePlacement already uses nameWindowX/nameWindowY in this plugin
        if (win._nameBoxWindow && win._nameBoxWindow.updatePlacement) {
            try { win._nameBoxWindow.updatePlacement(); } catch (e) { /* ignore */ }
        }
    }

function applyToCurrentMessageWindow() {
        const scene = SceneManager._scene;
        if (!scene || !scene._messageWindow) return;

        const win = scene._messageWindow;
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();

        // レイアウト変化に追従するため、基準座標を一旦リセット
        win._dbMWBasePos = null;

        // 高さ変更（Rect を更新 → 再配置）
        if (cfg.height != null) {
            const h = Math.max(1, Number(cfg.height));
            if (win.height !== h) {
                win.height = h;
                win._height = h; // 念のため（Window の内部参照がある環境向け）
                if (win._customBackground) {
                    win._customBackground.height = h;
                }
                win.updatePlacement();
            }
        }

        // 背景画像
        if (!win._customBackground) {
            if (win.createCustomBackground) win.createCustomBackground();
        }
        if (win._customBackground) {
            const visible = !!cfg.backgroundVisible;
            const fileName = (cfg.backgroundFile || "").trim();

            if (!visible || fileName === "") {
                win._customBackground.bitmap = new Bitmap(0, 0);
                win._customBackground.visible = false;
            } else {
                win._customBackground.bitmap = ImageManager.loadSystem(fileName);
                win._customBackground.visible = true;
            }
        }

        // アイコン位置など再計算
        if (win.updateCustomIconPositions) win.updateCustomIconPositions();

        // NameBox/ボタン/アイコンをテキスト開始位置に追従させる
        applyOffsets(win);
    }

    // メッセージウィンドウが再配置されたタイミングでも追従させる
    const _dbMW_updatePlacement = Window_Message.prototype.updatePlacement;
    Window_Message.prototype.updatePlacement = function() {
        _dbMW_updatePlacement.call(this);
        applyOffsets(this);
    };

    // NameBox は表示のたびに位置を更新されるので、その後にも補正をかける
    const _dbMW_updateSpeakerName = Window_Message.prototype.updateSpeakerName;
    Window_Message.prototype.updateSpeakerName = function() {
        _dbMW_updateSpeakerName.call(this);

    };

    // --- プラグインコマンド ---
    const PLUGIN_NAME = (document.currentScript && document.currentScript.src)
        ? document.currentScript.src.split("/").pop().replace(/\.js$/i, "")
        : "MessageWindowCustomize";

    PluginManager.registerCommand(PLUGIN_NAME, "SetMessageWindowBackground", args => {
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();
        const fileName = String(args.fileName || "").trim();
        const visible = String(args.visible || "true") === "true";

        cfg.backgroundFile = fileName;       // "" なら消す
        cfg.backgroundVisible = visible;

        applyToCurrentMessageWindow();
    });

    PluginManager.registerCommand(PLUGIN_NAME, "SetMessageWindowHeight", args => {
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();
        const h = Number(args.height || 300);
        cfg.height = Math.max(1, h);

        applyToCurrentMessageWindow();
    });

    PluginManager.registerCommand(PLUGIN_NAME, "SetMessageTextOffset", args => {
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();
        cfg.textStartX = Number(args.startX || TEXT_START_X_DEFAULT);
        cfg.textStartY = Number(args.startY || TEXT_START_Y_DEFAULT);

        // 文章表示中に即座に取り直すのは難しいので、次ページ以降に反映されます。
        // ただし、反映しておくために一応再配置だけ行います。
        applyToCurrentMessageWindow();
    });

    
    // --- Position commands (no correction; use given values as-is) ---
    PluginManager.registerCommand(PLUGIN_NAME, "SetMessageWindowBgPos", args => {
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();
        cfg.bgX = (args.x !== undefined) ? Number(args.x) : (cfg.bgX != null ? Number(cfg.bgX) : 0);
        cfg.bgY = (args.y !== undefined) ? Number(args.y) : (cfg.bgY != null ? Number(cfg.bgY) : 0);
        applyToCurrentMessageWindow();
    });

    PluginManager.registerCommand(PLUGIN_NAME, "SetMessageWindowIconPos", args => {
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();
        cfg.iconBaseX = (args.x !== undefined) ? Number(args.x) : (cfg.iconBaseX != null ? Number(cfg.iconBaseX) : 0);
        cfg.iconBaseY = (args.y !== undefined) ? Number(args.y) : (cfg.iconBaseY != null ? Number(cfg.iconBaseY) : 0);
        applyToCurrentMessageWindow();
    });

    PluginManager.registerCommand(PLUGIN_NAME, "SetNameWindowPos", args => {
        const cfg = $gameSystem.dbGetMessageWindowRuntimeConfig();
        cfg.nameWindowX = (args.x !== undefined) ? Number(args.x) : (cfg.nameWindowX != null ? Number(cfg.nameWindowX) : 0);
        cfg.nameWindowY = (args.y !== undefined) ? Number(args.y) : (cfg.nameWindowY != null ? Number(cfg.nameWindowY) : 0);
        applyToCurrentMessageWindow();
    });

PluginManager.registerCommand(PLUGIN_NAME, "ApplyMessageWindowConfig", () => {
        applyToCurrentMessageWindow();
    });

    PluginManager.registerCommand(PLUGIN_NAME, "ResetMessageWindowConfig", () => {
        $gameSystem.dbResetMessageWindowRuntimeConfig();
        applyToCurrentMessageWindow();
    });
})();

//=============================================================================
// [DB FIX] Force apply runtime XY positions every frame (no correction)
// 目的：他プラグイン（MessageSkip / MPP_ChoiceEX 等）が updatePlacement 後に座標を書き換えても、
//       最終的に指定した生のXYが必ず反映されるようにする
//=============================================================================
(() => {
    function dbGetCfg() {
        if ($gameSystem && $gameSystem.dbGetMessageWindowRuntimeConfig) {
            return $gameSystem.dbGetMessageWindowRuntimeConfig();
        }
        return null;
    }

    function dbApplyPositions(win) {
        if (!win) return;
        const cfg = dbGetCfg();
        if (!cfg) return;

        // 背景（メッセージウィンドウ内ローカル座標）
        if (win._customBackground) {
            win._customBackground.x = Number(cfg.bgX ?? 0);
            win._customBackground.y = Number(cfg.bgY ?? 0);
        }

        // アイコン（メッセージウィンドウ内ローカル座標）
        if (typeof win.updateCustomIconPositions === "function") {
            win.updateCustomIconPositions();
        }

        // 名前ウィンドウ（画面座標）
        if (win._nameBoxWindow) {
            win._nameBoxWindow.x = Number(cfg.nameWindowX ?? 0);
            win._nameBoxWindow.y = Number(cfg.nameWindowY ?? 0);
        }
    }

    const _DB_Window_Message_update = Window_Message.prototype.update;
    Window_Message.prototype.update = function() {
        _DB_Window_Message_update.call(this);
        // 可視状態に関わらず位置は毎フレーム確定させる（他プラグイン上書き対策）
        dbApplyPositions(this);
    };

    // NameBox 側でも保険（他プラグインが updatePlacement で動かすケース対策）
    const _DB_Window_NameBox_update = Window_NameBox.prototype.update;
    Window_NameBox.prototype.update = function() {
        _DB_Window_NameBox_update.call(this);
        const mw = this._messageWindow;
        if (mw) {
            dbApplyPositions(mw);
        }
    };
})();
;
