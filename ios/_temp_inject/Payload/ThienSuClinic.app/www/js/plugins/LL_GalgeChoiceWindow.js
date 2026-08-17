//=============================================================================
// RPGツクールMZ - LL_GalgeChoiceWindow.js v2.0.1
//-----------------------------------------------------------------------------
// ルルの教会 (Lulu's Church)
// https://nine-yusha.com/
//
// URL below for license details.
// https://nine-yusha.com/plugin/
//=============================================================================

/*:
 * @target MZ
 * @plugindesc ノベルゲーム風選択肢ウィンドウプラグイン
 * @author ルルの教会
 * @url https://nine-yusha.com/plugin-galgechoicewindow/
 *
 * @help LL_GalgeChoiceWindow.js
 *
 * ノベルゲーム風の選択肢ウィンドウを表示します。
 * 独自のウィンドウ画像、ボタン画像を設定することもできます。
 * (画像はimg/systemフォルダに配置してください)
 *
 * プラグインコマンド:
 *   選択肢の表示: 選択肢を表示し、結果を変数で受け取ります。
 *
 * 利用規約:
 *   ・著作権表記は必要ございません。
 *   ・利用するにあたり報告の必要は特にございません。
 *   ・商用・非商用問いません。
 *   ・R18作品にも使用制限はありません。
 *   ・ゲームに合わせて自由に改変していただいて問題ございません。
 *   ・プラグイン素材としての再配布（改変後含む）は禁止させていただきます。
 *
 * 作者: ルルの教会
 * 作成日: 2022/12/9
 *
 * @command showChoice
 * @text 選択肢の表示
 * @desc 選択肢を表示し、結果を変数で受け取ります。
 *
 * @arg messageText
 * @text 質問メッセージ
 * @desc 質問メッセージです。 (2行以内推奨)
 * \V[n]、\N[n]、\P[n]、\Gの制御文字が使用できます。
 * @type multiline_string
 *
 * @arg choices
 * @text 選択肢リスト
 * @desc 選択肢として表示する文字列のリストです。
 * @default []
 * @type struct<choices>[]
 *
 * @arg maxCols
 * @text 選択肢列数
 * @desc 選択肢を何列で表示するかの設定です。
 * @default 1
 * @min 1
 * @max 20
 * @type number
 *
 * @arg variableNumber
 * @text 結果受け取り変数
 * @desc 選択結果を受け取る変数IDを指定します。
 * @type variable
 *
 * @arg cancelType
 * @text キャンセル許可
 * @desc キャンセルされた場合は-1が変数に代入されます。
 * @default true
 * @type boolean
 *
 * @arg iniPosition
 * @text 初期カーソル位置
 * @desc カーソルの初期位置です。(0にすると選択なし)
 * 数値を入力するか変数で指定することもできます。
 * @default 1
 * @type combo
 * @option $gameVariables.value(1)   // 変数ID:1の値
 * @option 0
 * @option 1
 * @option 2
 * @option 3
 * @option 4
 * @option 5
 * @option 6
 *
 * @arg windowWidth
 * @text ウィンドウ幅
 * @desc 選択肢ウィンドウの幅です。
 * 背景画像を使用する場合は横幅を調整してください。
 * @default 480
 * @min 0
 * @max 9999
 * @type number
 *
 * @arg windowBgImage
 * @text ウィンドウ画像
 * @desc ウィンドウ画像を使用する場合は画像を選択してください。
 * 標準のウィンドウ枠は非表示になります。
 * @dir img/system
 * @type file
 * @require 1
 *
 * @arg buttonBgImage
 * @text ボタン画像
 * @desc ボタン画像を使用する場合は画像を選択してください。
 * @dir img/system
 * @type file
 * @require 1
 *
 * @arg buttonFocusImage
 * @text ボタン画像(選択時)
 * @desc フォーカス時のボタン画像を選択してください。
 * ベースとなるボタン画像と大きさを必ず統一してください。
 * @dir img/system
 * @type file
 * @require 1
 *
 * @arg buttonImageAdjustX
 * @text ボタン画像X座標
 * @desc ボタン画像の表示位置(X)の調整値です。(初期値: 0)
 * ＋で右へ、－で左へ調整します。
 * @default 0
 * @min -9999
 * @max 9999
 * @type number
 *
 * @arg buttonImageAdjustY
 * @text ボタン画像Y座標
 * @desc ボタン画像の表示位置(Y)の調整値です。(初期値: 0)
 * ＋で下へ、－で上へ調整します。
 * @default 0
 * @min -9999
 * @max 9999
 * @type number
 *
 * @arg itemHeightAdjust
 * @text 選択肢項目高さ
 * @desc 選択肢項目の高さの調整値です。(初期値: 8)
 * 画像が重なってしまう場合はこの数値を大きくしてください。
 * @default 8
 * @min -9999
 * @max 9999
 * @type number
 */

/*~struct~choices:
 *
 * @param label
 * @text 選択肢文字列
 * @desc 選択肢として表示する文字列です。
 * \V[n]、\N[n]、\P[n]、\Gの制御文字が使用できます。
 * @type string
 *
 * @param switchId
 * @text スイッチID
 * @desc スイッチON時のみ選択肢を表示したい場合に設定します。
 * 通常は「なし」のままで問題ありません。
 * @type switch
 *
 * @param resultNumber
 * @text 結果返却値
 * @desc この選択肢が選ばれた時に変数に入力する値を指定できます。
 * 「0」にすると自動で選択肢番号が返却されます。
 * @default 0
 * @min 0
 * @max 99999999
 * @type number
 */

(() => {
    "use strict";
    const pluginName = "LL_GalgeChoiceWindow";

    const parameters = PluginManager.parameters(pluginName);

    // Padding
    const gcwWindowPadding = 32;
    // キャンセル許可時のタッチUI戻るボタンの表示
    const gcwCancelButtonEnabled = false;
    // フェードイン効果フレーム
    const gcwFadeInFrame = 32;

    // 設定保存用変数定義
    let messageTextLists = [];
    let choiceLists = [];
    let maxCols = 1;
    let variableNumber = 0;
    let cancelType = true;
    let iniPosition = 1;
    let gcwWindowWidth = 480;
    let backgroundImage = "";
    let gcwButtonImage = "";
    let gcwButtonFocusImage = "";
    let gcwButtonAdjustX = 0;
    let gcwButtonAdjustY = 0;
    let gcwItemHeightAdjust = 8;

    PluginManager.registerCommand(pluginName, "showChoice", function(args) {
        // 設定を取得
        const messageText = String(args.messageText).split("\n");
        const choices = JSON.parse(args.choices || "null");
        maxCols = Number(args.maxCols || 1);
        variableNumber = Number(args.variableNumber);
        cancelType = String(args.cancelType) === "true" ? true : false;
        iniPosition = eval(args.iniPosition);
        gcwWindowWidth = Number(args.windowWidth || 480);
        backgroundImage = String(args.windowBgImage || "");
        gcwButtonImage = String(args.buttonBgImage || "");
        gcwButtonFocusImage = String(args.buttonFocusImage || "");
        gcwButtonAdjustX = Number(args.buttonImageAdjustX || 0);
        gcwButtonAdjustY = Number(args.buttonImageAdjustY || 0);
        gcwItemHeightAdjust = Number(args.itemHeightAdjust || 8);

        messageTextLists = [];
        if (messageText != "") {
            messageText.forEach((elm) => {
                messageTextLists.push(String(elm));
            });
        }

        // 選択肢を定義
        choiceLists = [];
        if (choices) {
            choices.forEach((elm) => {
                if (Number(JSON.parse(elm).switchId) === 0 || $gameSwitches.value(Number(JSON.parse(elm).switchId))) {
                    choiceLists.push(JSON.parse(elm));
                }
            });
        }

        // 選択肢が空の場合、終了
        if (choiceLists.length == 0) {
            console.log(pluginName + ": Không có lựa chọn hợp lệ nên lệnh đã bị bỏ qua");
            return;
        }

        if (!$gameMessage.isBusy()) {
            $gameMessage.setGalgeChoices(choiceLists);
            this.setWaitMode('message');
        }
    });


    //-----------------------------------------------------------------------------
    // Game_Message
    //

    const _Game_Message_clear = Game_Message.prototype.clear;
    Game_Message.prototype.clear = function() {
        _Game_Message_clear.apply(this, arguments);

        this._galgeChoices = [];
    };

    Game_Message.prototype.galgeChoices = function() {
        return this._galgeChoices;
    };

    Game_Message.prototype.isGalgeChoice = function() {
        return this._galgeChoices.length > 0;
    };

    Game_Message.prototype.setGalgeChoices = function(choices) {
        this._galgeChoices = choices;
    };

    const _Game_Message_isBusy = Game_Message.prototype.isBusy;
    Game_Message.prototype.isBusy = function() {
        return (
            _Game_Message_isBusy.apply(this, arguments) ||
            this.isGalgeChoice()
        );
    };


    //-----------------------------------------------------------------------------
    // Scene_Message
    //

    const _Scene_Message_createAllWindows = Scene_Message.prototype.createAllWindows;
    Scene_Message.prototype.createAllWindows = function() {
        this.createGalgeChoiceListWindow();
        _Scene_Message_createAllWindows.apply(this, arguments);
    };

    Scene_Message.prototype.createGalgeChoiceListWindow = function() {
        this._galgeChoiceListWindow = new Window_GalgeChoiceList();
        this.addWindow(this._galgeChoiceListWindow);
    };

    const _Scene_Message_associateWindows = Scene_Message.prototype.associateWindows;
    Scene_Message.prototype.associateWindows = function() {
        _Scene_Message_associateWindows.apply(this, arguments);

        const messageWindow = this._messageWindow;
        messageWindow.setGalgeChoiceListWindow(this._galgeChoiceListWindow);
        if (this._galgeChoiceListWindow) this._galgeChoiceListWindow.setMessageWindow(messageWindow);
    };


    //-----------------------------------------------------------------------------
    // Window_Message
    //

    const _Window_Message_initMembers = Window_Message.prototype.initMembers;
    Window_Message.prototype.initMembers = function() {
        _Window_Message_initMembers.apply(this, arguments);

        this._galgeChoiceListWindow = null;
    };

    const _Window_Message_startInput = Window_Message.prototype.startInput;
    Window_Message.prototype.startInput = function() {
        if ($gameMessage.isGalgeChoice()) {
            this._galgeChoiceListWindow.start();
            return true;
        }

        return _Window_Message_startInput.apply(this, arguments);
    };

    Window_Message.prototype.setGalgeChoiceListWindow = function(galgeChoiceListWindow) {
        this._galgeChoiceListWindow = galgeChoiceListWindow;
    };

    const _Window_Message_isAnySubWindowActive = Window_Message.prototype.isAnySubWindowActive;
    Window_Message.prototype.isAnySubWindowActive = function() {
        if (this._galgeChoiceListWindow) {
            return (
                _Window_Message_isAnySubWindowActive.apply(this, arguments) ||
                this._galgeChoiceListWindow.active
            );
        }

        return _Window_Message_isAnySubWindowActive.apply(this, arguments);
    };

    //-----------------------------------------------------------------------------
    // Window_GalgeChoiceList
    //
    // ノベルゲーム風選択肢ウィンドウを定義します。

    function Window_GalgeChoiceList() {
        this.initialize(...arguments);
    }

    Window_GalgeChoiceList.prototype = Object.create(Window_Command.prototype);
    Window_GalgeChoiceList.prototype.constructor = Window_GalgeChoiceList;

    Window_GalgeChoiceList.prototype.initialize = function() {
        Window_Command.prototype.initialize.call(this, new Rectangle());
        this.createCancelButton();
        this.openness = 0;
        this.deactivate();
        this._background = 0;
        this._canRepeat = false;
        // フォーカスアニメーション判定
        this._originalCursorSpriteFade = true;
    };

    Window_GalgeChoiceList.prototype.setMessageWindow = function(messageWindow) {
        this._messageWindow = messageWindow;
    };

    Window_GalgeChoiceList.prototype.createCancelButton = function() {
        if (ConfigManager.touchUI) {
            this._cancelButton = new Sprite_Button("cancel");
            this._cancelButton.visible = false;
            this.addChild(this._cancelButton);
        }
    };

    Window_GalgeChoiceList.prototype.start = function() {
        this.updatePlacement();
        this.createCancelButton();
        this.placeCancelButton();
        this.createContents();
        this.refresh();
        this.setQuestionText();
        this.setSymbol();
        this.createOriginalBackground();
        this.open();
        this.activate();
    };

    const _Window_GalgeChoiceList_refresh = Window_GalgeChoiceList.prototype.refresh;
    Window_GalgeChoiceList.prototype.refresh = function() {
        this.removeChild(this._bgSprite);
        this._bgSprite = null;
        this.removeChild(this._bgDummy);
        this._bgDummy = null;
        this.removeChild(this._originalCursorSprite);
        this._originalCursorSprite = null;
        this.removeChild(this._originalButtonSprite);
        this._originalButtonSprite = null;

        // ウィンドウ枠、カーソルを初期化
        this.setCursorRect(0, 0, 0, 0);
        this.opacity = 255;

        _Window_GalgeChoiceList_refresh.apply(this, arguments);
    };

    Window_GalgeChoiceList.prototype.updatePlacement = function() {
        const wh = this.calcWindowHeight();
        const ww = gcwWindowWidth;
        const wx = (Graphics.boxWidth - ww) / 2;
        const wy = (Graphics.boxHeight - wh) / 2;

        this.width = ww;
        this.height = wh;
        this.x = wx;
        this.y = wy;
    };

    Window_GalgeChoiceList.prototype.calcWindowHeight = function() {
        // ウィンドウの高さを計算
        const itemCols = Math.ceil(choiceLists.length / maxCols);
        let height = this.lineHeight() * messageTextLists.length;
        if (messageTextLists.length > 0) height += gcwWindowPadding;
        height += (this.itemHeight()) * itemCols;
        height += gcwWindowPadding * 2;  // padding
        return height;
    };

    Window_GalgeChoiceList.prototype.createCancelButton = function() {
        if (ConfigManager.touchUI) {
            this._cancelButton = new Sprite_Button("cancel");
            this._cancelButton.visible = false;
            this.addChild(this._cancelButton);
        }
    };

    Window_GalgeChoiceList.prototype.createOriginalBackground = function() {
        if (backgroundImage != "") {
            this._bgSprite = new Sprite();
            this._bgSprite.bitmap = ImageManager.loadSystem(backgroundImage);
            this._bgSprite.bitmap.addLoadListener(function() {
                this._bgSprite.x = this.width / 2 - this._bgSprite.width / 2;
                this._bgSprite.y = this.height / 2 - this._bgSprite.height / 2;
            }.bind(this));
            this._bgSprite.opacity = 0;
            this.addChildToBack(this._bgSprite);
            // ウィンドウ枠を消去
            this.opacity = 0;
        }
    };

    Window_GalgeChoiceList.prototype.drawAllItems = function() {
        this.createOriginalCursor();
        this.createOriginalButton();
        Window_Selectable.prototype.drawAllItems.call(this);
    };

    Window_GalgeChoiceList.prototype.createOriginalCursor = function() {
        if (gcwButtonFocusImage != "") {
            this._originalCursorSprite = null;
            this._originalCursorSprite = new Sprite();
            this._originalCursorSprite.bitmap = ImageManager.loadSystem(gcwButtonFocusImage);
            this._originalCursorSprite.opacity = 128;
            this._originalCursorSprite.visible = true;
            this.addChildToBack(this._originalCursorSprite);
        }
    };

    Window_GalgeChoiceList.prototype.createOriginalButton = function() {
        if (gcwButtonImage != "") {
            this._originalButtonSprite = null;
            this._originalButtonSprite = new Sprite();
            this._originalButtonSprite.visible = false;
            this.addChildToBack(this._originalButtonSprite);
        }
    };

    Window_GalgeChoiceList.prototype.drawBackgroundRect = function(rect) {
        const c1 = ColorManager.itemBackColor1();
        const c2 = ColorManager.itemBackColor2();
        const x = rect.x;
        const y = rect.y;
        const w = rect.width;
        const h = rect.height;
        if (gcwButtonImage != "") {
            const originalButtonSprite = new Sprite();
            originalButtonSprite.bitmap = ImageManager.loadSystem(gcwButtonImage);
            originalButtonSprite.x = x + gcwButtonAdjustX + gcwWindowPadding;
            originalButtonSprite.y = y + gcwButtonAdjustY + gcwWindowPadding;
            this._originalButtonSprite.addChild(originalButtonSprite);
        } else {
            this.contentsBack.gradientFillRect(x, y, w, h, c1, c2, true);
            this.contentsBack.strokeRect(x, y, w, h, c1);
        }
    };

    Window_GalgeChoiceList.prototype.refreshCursor = function() {
        if (this._cursorAll) {
            this.refreshCursorForAll();
        } else if (this.index() >= 0) {
            const rect = this.itemRect(this.index());
            if (gcwButtonFocusImage != "") {
                if (this._originalCursorSprite) {
                    this._originalCursorSprite.x = rect.x + gcwButtonAdjustX + gcwWindowPadding;
                    this._originalCursorSprite.y = rect.y + gcwButtonAdjustY + gcwWindowPadding;
                }
            } else {
                this.setCursorRect(rect.x, rect.y, rect.width, rect.height);
            }
        } else {
            this.setCursorRect(0, 0, 0, 0);
        }
    };

    Window_GalgeChoiceList.prototype.refreshCursorForAll = function() {
        const maxItems = this.maxItems();
        if (maxItems > 0) {
            const rect = this.itemRect(0);
            rect.enlarge(this.itemRect(maxItems - 1));
            if (gcwButtonFocusImage != "") {
                if (this._originalCursorSprite) {
                    this._originalCursorSprite.x = rect.x + gcwButtonAdjustX;
                    this._originalCursorSprite.y = rect.y + gcwButtonAdjustY;
                }
            } else {
                this.setCursorRect(rect.x, rect.y, rect.width, rect.height);
            }
        } else {
            this.setCursorRect(0, 0, 0, 0);
        }
    };

    Window_GalgeChoiceList.prototype.update = function() {
        Window_Command.prototype.update.call(this);
        this.updateCancelButton();
        this.updateOriginalButton();
        this.updateOriginalCursorButton();
        if (this._bgSprite) this._bgSprite.opacity = this.openness;
    };

    Window_GalgeChoiceList.prototype.updateOriginalButton = function() {
        if (this._originalButtonSprite) {
            if (this.isOpen()) {
                this._originalButtonSprite.visible = true;
            } else {
                this._originalButtonSprite.visible = false;
            }
        }
    };

    Window_GalgeChoiceList.prototype.updateOriginalCursorButton = function() {
        if (this._originalCursorSprite) {
            if (this.isOpen() && this._index > -1) {
                this._originalCursorSprite.visible = true;
                if (this._originalCursorSprite.opacity >= 255) this._originalCursorSpriteFade = false;
                if (this._originalCursorSprite.opacity <= 128) this._originalCursorSpriteFade = true;
                this._originalCursorSprite.opacity += this._originalCursorSpriteFade ? 6 : -6;
            } else {
                this._originalCursorSprite.visible = false;
            }
        }
    };

    Window_GalgeChoiceList.prototype.updateOpen = function() {
        if (this._opening) {
            this.openness += gcwFadeInFrame;
            if (this.isOpen()) {
                this._opening = false;
            }
        }
    };

    Window_GalgeChoiceList.prototype.updateCancelButton = function() {
        if (this._cancelButton) {
            this._cancelButton.visible = this.needsCancelButton() && this.isOpen() && gcwCancelButtonEnabled;
        }
    };

    Window_GalgeChoiceList.prototype.needsCancelButton = function() {
        return cancelType;
    };

    Window_GalgeChoiceList.prototype.placeCancelButton = function() {
        if (this._cancelButton) {
            const spacing = 8;
            const button = this._cancelButton;
            const right = this.x + this.width;
            if (right < Graphics.boxWidth - button.width + spacing) {
                button.x = this.width + spacing;
            } else {
                button.x = -button.width - spacing;
            }
            button.y = this.height / 2 - button.height / 2;
        }
    };

    Window_GalgeChoiceList.prototype.maxCols = function() {
        return maxCols;
    };

    Window_GalgeChoiceList.prototype.setQuestionText = function() {
        messageTextLists.forEach((text, index) => {
            this.drawText(this.convertEscapeCharacters(text), 0, this.lineHeight() * index, this.innerWidth, "center");
        }, this);
    };

    Window_GalgeChoiceList.prototype.makeCommandList = function() {
        choiceLists.forEach(function(elm, index) {
            this.addCommand(String(elm.label), Number(elm.resultNumber || 0) !== 0 ? Number(elm.resultNumber) : index + 1);
        }, this);
    };

    Window_GalgeChoiceList.prototype.updatePadding = function() {
        this.padding = gcwWindowPadding;
    };

    Window_GalgeChoiceList.prototype.scrollBaseY = function(index) {
        let margin = this.lineHeight() * messageTextLists.length;
        if (messageTextLists.length > 0) margin += gcwWindowPadding;
        return this._scrollBaseY - margin;
    };

    Window_GalgeChoiceList.prototype.setSymbol = function() {
        if (iniPosition > 0) {
            this.selectSymbol(iniPosition);
        } else {
            this.deselect();
        }
    };

    Window_GalgeChoiceList.prototype.itemHeight = function() {
        return Window_Scrollable.prototype.itemHeight.call(this) + gcwItemHeightAdjust;
    };

    Window_GalgeChoiceList.prototype.drawItem = function(index) {
        const rect = this.itemLineRect(index);
        const align = this.itemTextAlign();
        this.resetTextColor();
        this.changePaintOpacity(this.isCommandEnabled(index));
        this.drawText(this.convertEscapeCharacters(this.commandName(index)), rect.x, rect.y, rect.width, align);
    };

    Window_GalgeChoiceList.prototype.isCancelEnabled = function() {
        return cancelType;
    };

    Window_GalgeChoiceList.prototype.isOkTriggered = function() {
        return Input.isTriggered('ok');
    };

    Window_GalgeChoiceList.prototype.callOkHandler = function() {
        $gameVariables.setValue(variableNumber, this.currentSymbol());
        this._messageWindow.terminateMessage();
        this.close();
    };

    Window_GalgeChoiceList.prototype.callCancelHandler = function() {
        $gameVariables.setValue(variableNumber, -1);
        this._messageWindow.terminateMessage();
        this.close();
    };
})();
