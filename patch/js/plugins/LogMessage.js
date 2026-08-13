/*---------------------------------------------------------------------------*
 * 2022/12/11 kido
 * https://kido0617.github.io/
 *---------------------------------------------------------------------------*/

/*:
 * @plugindesc ログメッセージプラグイン（縁取り対応版）
 * @target MZ
 * @base PluginCommonBase
 * @orderAfter PluginCommonBase
 * @author kido0617
 * @help
 *
 * 機能は各プラグインコマンドを参照。
 * 最初に初期化コマンドから表示位置とサイズを指定し実行します。
 * その後はメッセージ追加もコマンドからテキストを追加します。
 * 初期化したマップでのみ有効。マップ遷移したら自動的に消えます。
 *
 * @command init
 * @text 初期化
 * @desc 座標とサイズを指定
 *
 * @arg x
 * @text x
 * @type number
 *
 * @arg y
 * @text y
 * @type number
 *
 * @arg width
 * @text width
 * @type number
 *
 * @arg height
 * @text height
 * @type number
 *
 * @command add
 * @text メッセージ追加
 * @desc
 *
 * @arg text
 * @text テキスト
 * @desc 制御文字も使えます
 *
 * @command hide
 * @text 非表示
 * @desc 一時的に非表示にします
 *
 * @command show
 * @text 表示
 * @desc 非表示したものを表示します
 *
 * @command clear
 * @text ログを消去
 * @desc 表示しているログを消します
 *
 * @command remove
 * @text ウィンドウ除去
 * @desc 完全に消えます。再度初期化してください
 *
 * @command setOutline
 * @text 縁取り設定
 * @desc ログ文字の縁の太さ/色を変更します（必要なら既存ログも再描画）
 *
 * @arg width
 * @text 縁の太さ
 * @type number
 * @default 4
 *
 * @arg color
 * @text 縁の色
 * @type string
 * @default rgba(0,0,0,0.6)
 *
 * @arg refresh
 * @text 既存ログを再描画
 * @type boolean
 * @default false
 *
 *
 * @param lineHeight
 * @text 1行の高さ
 * @desc 基本的に フォントサイズ+α です。
 * @type number
 * @default 36
 *
 * @param fontSize
 * @text フォントサイズ
 * @desc フォントサイズです
 * @type number
 * @default 28
 *
 * @param iconSize
 * @text アイコンサイズ
 * @desc アイコンサイズです
 * @type number
 * @default 32
 *
 * @param scrollSpeed
 * @text スクロールスピード
 * @desc コメントが上にスクロールするスピード[pixel/frame]
 * @type number
 * @default 4
 *
 * @param indent
 * @text インデント
 * @desc テキストの左インデント（px）
 * @type number
 * @default 0
 *
 * @param outlineWidth
 * @text 縁の太さ
 * @desc 文字の縁の太さです（0で縁なし）
 * @type number
 * @default 4
 *
 * @param outlineColor
 * @text 縁の色
 * @desc 文字の縁の色です（例: rgba(0,0,0,0.6) / #000000）
 * @type string
 * @default rgba(0,0,0,0.6)
 */

/* Patched: persist LogMessage across Scene recreation (SaveWindow/TextLog) */

(() => {
  const script = document.currentScript;
  const param = PluginManagerEx.createParameter(script);

  // --- global state key (stored in $gameTemp) ---
  const STATE_KEY = "_dbLogMessageState";

  function state() {
    if (!$gameTemp) return null;
    if (!$gameTemp[STATE_KEY]) $gameTemp[STATE_KEY] = null;
    return $gameTemp[STATE_KEY];
  }
  function setState(s) {
    $gameTemp[STATE_KEY] = s;
  }

  function ensureState() {
    let s = state();
    if (!s) {
      s = {
        inited: false,
        x: 0, y: 0, width: 0, height: 0,
        visible: true,
        logs: [],
        // outline
        outlineWidth: Number(param.outlineWidth ?? 4),
        outlineColor: String(param.outlineColor ?? "rgba(0,0,0,0.6)"),
        // runtime
        container: null,
        attachedSceneId: null,
        needReattach: false,
        lastRenderedCount: 0,
      };
      setState(s);
    }
    return s;
  }

  function currentScene() {
    return SceneManager._scene;
  }

  function currentOutlineWidth() {
    const s = state();
    if (s && s.inited && s.outlineWidth != null) return Number(s.outlineWidth);
    return Number(param.outlineWidth ?? 4);
  }

  function currentOutlineColor() {
    const s = state();
    if (s && s.inited && s.outlineColor != null) return String(s.outlineColor);
    return String(param.outlineColor ?? "rgba(0,0,0,0.6)");
  }

  // Find spriteset map safely
  function findSpritesetMap(scene) {
    if (!scene || !scene.children) return null;
    for (let i = 0; i < scene.children.length; i++) {
      const c = scene.children[i];
      if (c && c.constructor && c.constructor.name === "Spriteset_Map") return c;
    }
    return null;
  }

  function ensureContainer() {
    const s = ensureState();
    if (!s.inited) return null;
    if (s.container && !s.container._destroyed) return s.container;

    s.container = new LogMessageContainer(s.x, s.y, s.width, s.height);
    s.container.visible = !!s.visible;
    s.lastRenderedCount = 0;

    // render existing logs (rebuild)
    for (let i = 0; i < s.logs.length; i++) {
      s.container._appendText(s.logs[i]);
      s.lastRenderedCount++;
    }
    return s.container;
  }

  // Attach container to current Scene_Map spriteset upper layer
  function tryAttachToMapScene(scene) {
    const s = state();
    if (!s || !s.inited) return false;
    if (!scene || !(scene instanceof Scene_Map)) return false;

    const container = ensureContainer();
    if (!container) return false;

    const ss = findSpritesetMap(scene);
    if (!ss || !ss._baseSprite) {
      // too early; try later
      s.needReattach = true;
      return false;
    }

    // choose a safe parent: Scene window layer (always above pictures)
    const parent = scene._windowLayer || (ss && ss._baseSprite) || null;

    if (!parent) {
      s.needReattach = true;
      return false;
    }

    // If already attached to this parent, ok.
    if (container.parent === parent) {
      s.attachedSceneId = scene._sceneId || scene._mapId || 0;
      s.needReattach = false;
      return true;
    }

    // Detach from old parent if needed
    if (container.parent) {
      try { container.parent.removeChild(container); } catch (e) {}
    }

    // Add (not addChildAt; avoids _parentID null timing issues)
    try {
      parent.addChild(container);
      s.attachedSceneId = scene._sceneId || scene._mapId || 0;
      s.needReattach = false;
      return true;
    } catch (e) {
      // still too early
      s.needReattach = true;
      return false;
    }
  }

  // Flush new logs into container if not rendered yet
  function syncLogsToContainer() {
    const s = state();
    if (!s || !s.inited) return;
    const scene = currentScene();
    if (!scene || !(scene instanceof Scene_Map)) return;

    const container = ensureContainer();
    if (!container) return;

    // ensure attached (if scene recreated)
    if (s.needReattach || container.parent == null) {
      tryAttachToMapScene(scene);
    }

    // append any pending logs
    while (s.lastRenderedCount < s.logs.length) {
      container._appendText(s.logs[s.lastRenderedCount]);
      s.lastRenderedCount++;
    }
    container.visible = !!s.visible;
  }

  // Public getter used by commands (returns container if available on map; else null)
  function getLogMessageWindow() {
    const s = state();
    if (!s || !s.inited) return null;
    const scene = currentScene();
    if (scene instanceof Scene_Map) {
      syncLogsToContainer();
      return s.container;
    }
    return null;
  }

  // ---- Plugin Commands ----
  PluginManagerEx.registerCommand(script, "init", args => {
    const s = ensureState();
    if (s.inited) {
      console.error("Đã khởi tạo init sẵn rồi");
      return;
    }
    s.inited = true;
    s.x = Number(args.x || 0);
    s.y = Number(args.y || 0);
    s.width = Number(args.width || 0);
    s.height = Number(args.height || 0);
    s.visible = true;
    s.logs = [];
    s.container = null;
    s.needReattach = true;
    s.lastRenderedCount = 0;

    // default outline
    s.outlineWidth = Number(param.outlineWidth ?? 4);
    s.outlineColor = String(param.outlineColor ?? "rgba(0,0,0,0.6)");

    // Create now (if on map), otherwise will be created when returning to map.
    if (currentScene() instanceof Scene_Map) {
      ensureContainer();
      // attach safely next update tick
      s.needReattach = true;
    }
  });

  PluginManagerEx.registerCommand(script, "add", args => {
    const s = ensureState();
    if (!s || !s.inited) return;

    const text = String(args.text ?? "");
    // Always keep log text even if not on map scene right now.
    s.logs.push(text);

    // If on map, sync immediately; if not, will appear when back on map.
    if (currentScene() instanceof Scene_Map) {
      syncLogsToContainer();
    }
  });

  PluginManagerEx.registerCommand(script, "hide", () => {
    const s = state();
    if (!s || !s.inited) return;
    s.visible = false;
    if (s.container) s.container.visible = false;
  });

  PluginManagerEx.registerCommand(script, "show", () => {
    const s = state();
    if (!s || !s.inited) return;
    s.visible = true;
    if (currentScene() instanceof Scene_Map) syncLogsToContainer();
    if (s.container) s.container.visible = true;
  });

  PluginManagerEx.registerCommand(script, "clear", () => {
    const s = state();
    if (!s || !s.inited) return;
    s.logs = [];
    s.lastRenderedCount = 0;
    if (s.container) s.container.clear();
  });

  // ★追加：縁取り設定
  PluginManagerEx.registerCommand(script, "setOutline", args => {
    const s = ensureState();
    if (!s || !s.inited) return;

    if (args.width !== undefined && args.width !== null && args.width !== "") {
      s.outlineWidth = Number(args.width);
    }
    if (args.color !== undefined && args.color !== null && args.color !== "") {
      s.outlineColor = String(args.color);
    }

    const refresh = args.refresh === true || args.refresh === "true";

    if (refresh && s.container) {
      s.container.clear();
      s.lastRenderedCount = 0;
      for (let i = 0; i < s.logs.length; i++) {
        s.container._appendText(s.logs[i]);
        s.lastRenderedCount++;
      }
    }
  });

  PluginManagerEx.registerCommand(script, "remove", () => {
    const s = state();
    if (!s) return;
    if (s.container && s.container.parent) {
      try { s.container.parent.removeChild(s.container); } catch (e) {}
    }
    if (s.container) {
      try { s.container.destroy({ children: true }); } catch (e) {}
    }
    setState(null);
  });

  // ---- Scene hooks: keep attached & synced after scene recreation ----
  const _Scene_Map_start = Scene_Map.prototype.start;
  Scene_Map.prototype.start = function() {
    _Scene_Map_start.call(this);
    const s = state();
    if (s && s.inited) {
      // Scene_Map is (re)started by TextLog etc; reattach next update tick.
      s.needReattach = true;
    }
  };

  const _Scene_Map_update = Scene_Map.prototype.update;
  Scene_Map.prototype.update = function() {
    _Scene_Map_update.call(this);
    // after base update, ensure log container attached and synced
    syncLogsToContainer();
  };

  // ---- Container + hidden window ----
  function LogMessageContainer(x, y, width, height) {
    PIXI.Container.call(this);
    this.x = x;
    this.y = y;
    this._width = width;
    this._height = height;
    this._yPos = 0;

    // Mask (must be in display list). Use local coords (0,0) because container already positioned.
    this._maskG = new PIXI.Graphics();
    this._maskG.beginFill(0xffffff);
    this._maskG.drawRect(0, 0, width, height);
    this._maskG.endFill();
    this.addChild(this._maskG);
    this.mask = this._maskG;

    this._hiddenWindow = new Window_Hidden(width);
  }
  LogMessageContainer.prototype = Object.create(PIXI.Container.prototype);
  LogMessageContainer.prototype.constructor = LogMessageContainer;

  LogMessageContainer.prototype.update = function() {
    let moveY = 0;

    // find last visible message sprite (skip mask)
    const msgs = this.children.filter(c => c && c !== this._maskG);
    if (msgs.length > 0) {
      const last = msgs[msgs.length - 1];
      const bottom = (last.y || 0) + (last.height || 0);
      const diff = bottom - this._height;
      if (diff > 0) moveY = diff > param.scrollSpeed ? param.scrollSpeed : diff;
    }

    for (let i = 0; i < this.children.length; i++) {
      const ch = this.children[i];
      if (!ch || ch === this._maskG) continue;
      if (typeof ch.update === "function") ch.update();
      ch.y -= moveY;
    }
    this._yPos -= moveY;

    // remove first message if out of view (skip mask at index 0)
    const firstMsg = this.children.find(c => c && c !== this._maskG);
    if (firstMsg && (firstMsg.y + firstMsg.height) <= 0) {
      try { this.removeChild(firstMsg); } catch (e) {}
    }
  };

  LogMessageContainer.prototype._appendText = function(text) {
    const textSprite = new Sprite();
    textSprite.y = this._yPos;

    const indent = Number(param.indent || 0);

    // アイコン分を「常に」足したいならtrue。不要なら false にする
    const addIconIndentAlways = false;
    const iconIndent = addIconIndentAlways ? (Number(param.iconSize || 0) + 4) : 0;

    const ow = currentOutlineWidth();
    const drawX = indent + iconIndent + Math.ceil(ow / 2);
    const w = Math.max(0, this._width - drawX);

    const lineY = param.lineHeight / 2 - param.fontSize / 2 - 8;

    // フォントサイズと縁取りは Window_Hidden 側で反映
    this._hiddenWindow.drawTextEx(text, drawX, lineY, w);

    textSprite.bitmap = this._hiddenWindow.contents;

    this._hiddenWindow.contents = null;
    this._hiddenWindow.createContents();

    this.addChild(textSprite);
    this._yPos += param.lineHeight;
  };

  LogMessageContainer.prototype.show = function(text) {
    this._appendText(text);
  };

  LogMessageContainer.prototype.clear = function() {
    // keep mask, remove others
    const keep = this._maskG;
    this.removeChildren();
    this.addChild(keep);
    this.mask = keep;
    this._yPos = 0;
  };

  function Window_Hidden() {
    this.initialize.apply(this, arguments);
  }
  Window_Hidden.prototype = Object.create(Window_Base.prototype);
  Window_Hidden.prototype.constructor = Window_Hidden;

  /**
   * A minimal, off-screen Window used only to render text into a Bitmap.
   * It MUST initialize as Window_Base so that `this.contents` setter has a valid _contentsSprite.
   */
  Window_Hidden.prototype.initialize = function(width) {
    this.tmpWidth = width;
    const rect = new Rectangle(0, 0, width, param.lineHeight);
    Window_Base.prototype.initialize.call(this, rect);

    // Make it effectively invisible (but keep internal sprites alive).
    this.opacity = 0;
    this.backOpacity = 0;
    this.contentsOpacity = 255;
    this.padding = 0;
    this.visible = false;

    this.createContents();
  };

  Window_Hidden.prototype.createContents = function() {
    // Create a fresh bitmap each time. Sprites that received the previous bitmap keep it.
    this.contents = new Bitmap(this.tmpWidth, param.lineHeight);
    this.contents.fontSize = param.fontSize;

    // ★追加：縁取り設定
    this.contents.outlineWidth = currentOutlineWidth();
    this.contents.outlineColor = currentOutlineColor();
  };

  // Window_Hidden だけ、フォントリセット後に param.fontSize を強制する
  Window_Hidden.prototype.resetFontSettings = function() {
    Window_Base.prototype.resetFontSettings.call(this);
    if (this.contents) {
      this.contents.fontSize = param.fontSize;

      // ★追加：縁取り設定（drawTextExのたびに反映）
      this.contents.outlineWidth = currentOutlineWidth();
      this.contents.outlineColor = currentOutlineColor();
    }
  };

  // ★追加：\C[x] 等の色変更が走っても縁取りを維持する
  const _Window_Hidden_changeTextColor = Window_Hidden.prototype.changeTextColor;
  Window_Hidden.prototype.changeTextColor = function(color) {
    _Window_Hidden_changeTextColor.call(this, color);
    if (this.contents) {
      this.contents.outlineWidth = currentOutlineWidth();
      this.contents.outlineColor = currentOutlineColor();
    }
  };

  // 念のため processColorChange も押さえる（環境差・他プラグイン対策）
  const _Window_Hidden_processColorChange = Window_Hidden.prototype.processColorChange;
  Window_Hidden.prototype.processColorChange = function(colorIndex) {
    _Window_Hidden_processColorChange.call(this, colorIndex);
    if (this.contents) {
      this.contents.outlineWidth = currentOutlineWidth();
      this.contents.outlineColor = currentOutlineColor();
    }
  };

})();