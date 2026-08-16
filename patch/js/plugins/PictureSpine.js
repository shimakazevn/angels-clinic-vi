//==============================================================================
// PictureSpine.js ver.1.21
//==============================================================================

/*:
 * @plugindesc Spineアニメーションプラグイン
 * @author 奏ねこま（おとぶきねこま）
 * @url http://makonet.sakura.ne.jp/rpg_tkool
 * @target MZ
 * 
 * @param json file
 * @type string[]
 * @default []
 * @desc Spineファイル(*.json)
 *
 * @param disable auto loading
 * @type boolean
 * @default false
 * @desc Spineの自動読み込みを無効にする
 *
 * @help
 * 本プラグインの利用方法については下記マニュアルをご参照ください。
 * http://makonet.sakura.ne.jp/rpg_tkool/MVMZ/PictureSpine/document.html
 * 
 * ------------------------------------------------------------------------------
 *   本プラグインの利用はRPGツクール/RPG Makerの正規ユーザーに限られます。
 *   商用、非商用、有償、無償、一般向け、成人向けを問わず利用可能です。
 *   ご利用の際に連絡や報告は必要ありません。また、製作者名の記載等も不要です。
 *   プラグインを導入した作品に同梱する形以外での再配布、転載はご遠慮ください。
 *   本プラグインにより生じたいかなる問題についても一切の責任を負いかねます。
 * ------------------------------------------------------------------------------
 *                                              Copylight (c) 2023 Nekoma Otobuki
 *                                         http://makonet.sakura.ne.jp/rpg_tkool/
 *                                             https://twitter.com/maconetto_labo
 */

!function() {
    'use strict';

    let $p = function parse(param) {
        try {
            param = JSON.parse(param);
        }
        catch (e) {}
        if (Array.isArray(param)) {
            param = param.map(value => parse(value));
        } else if (typeof param == 'object') {
            for (let key in param) {
                param[key] = parse(param[key]);
            }
        }
        return param;
    }({
        ...PluginManager.parameters('PictureSpine'),
        'spine data': {}
    });

    function load() {
        let loader = new (PIXI.Loader || PIXI.loaders.Loader)();
        for (let file of $p['json file']) {
            let name = String(file).replace(/\.json$/i, '');
            if (!$p['disable auto loading']) {
                $p['spine data'][name] = null;
                loader.add(name, `img/spines/${name}.json`);
            } else {
                $p['spine data'][name] = {};
            }
        }
        loader.load((loader, resource) => {
            for (let name in $p['spine data']) {
                if (resource[name]) {
                    $p['spine data'][name] = resource[name].spineData;
                }
            }
        });
    }

    if (!PIXI.spine) {
        let js = null;
        for (let element of document.getElementsByTagName('script')) {
            if (element.src.match('pixi-spine.js')) {
                js = element;
            }
        }
        if (!js) {
            js = document.createElement('script');
            js.type = 'text/javascript';
            js.src  = 'js/libs/pixi-spine.js';
            document.body.appendChild(js);
        }
        js.addEventListener('load', load);
    } else {
        load();
    }

    class MosaicFilter extends PIXI.Filter {
        constructor(size = 10) {
            let vertex   = 'attribute vec2 aVertexPosition;attribute vec2 aTextureCoord;uniform mat3 projectionMatrix;varying vec2 vTextureCoord;void main(void){gl_Position=vec4((projectionMatrix*vec3(aVertexPosition,1.0)).xy,0.0,1.0);vTextureCoord=aTextureCoord;}';
            let fragment = 'precision mediump float;varying vec2 vTextureCoord;uniform vec2 size;uniform sampler2D uSampler;uniform vec4 filterArea;vec2 mapCoord(vec2 coord){coord*=filterArea.xy;coord+=filterArea.zw;return coord;}vec2 unmapCoord(vec2 coord){coord-=filterArea.zw;coord/=filterArea.xy;return coord;}vec2 pixelate(vec2 coord, vec2 size){return floor(coord / size) * size;}void main(void){vec2 coord=mapCoord(vTextureCoord);coord=pixelate(coord, size);coord=unmapCoord(coord);gl_FragColor=texture2D(uSampler, coord);}';
            super(vertex, fragment);
            this.uniforms.size = [size, size];
        }
    }

    function convars(obj) {
        if (typeof obj == 'string') {
            let _obj = obj.replace(/\\v\[(\d+)\]/gi, (match, p1) => {
                return $gameVariables.value(Number(p1));
            });
            obj = _obj != obj ? convars(_obj) : _obj;
        } else if (obj instanceof Array) {
            obj = obj.map(value => convars(value));
        } else if (typeof obj == 'object') {
            obj = {...obj};
            for (let key in obj) {
                obj[key] = convars(obj[key]);
            }
        }
        return obj;
    }

    //==============================================================================
    // JsonEx
    //==============================================================================

    (___decode => {
        JsonEx._decode = function(value, circular, registry) {
            let decode = ___decode.apply(this, arguments);
            if (decode instanceof Game_Spine) {
                if ('_visible' in decode == false) {
                    decode._visible = true;
                }
                if ('_bone' in decode == false) {
                    decode._bone = {};
                }
                if ('_callback' in decode == false) {
                    decode._callback = {};
                }
                if (decode._skin instanceof Array == false) {
                    decode._skin = [decode._skin];
                }
            }
            return decode;
        };
    })(JsonEx._decode);

    //==============================================================================
    // AudioManager
    //==============================================================================

    AudioManager._subFolder = '';

    (__createBuffer => {
        AudioManager.createBuffer = function(folder, name) {
            folder += this._subFolder.replace(/^\/?(?=.)/, '/');
            this._subFolder = '';
            return __createBuffer.call(this, folder, name);
        };
    })(AudioManager.createBuffer);

    //==============================================================================
    // Game_Screen
    //==============================================================================

    Game_Screen.prototype.spine = function(id) {
        let picture = this.picture(id);
        if (!picture._spine) {
            picture._spine = new Game_Spine();
        }
        return picture._spine;
    };

    //==============================================================================
    // Game_Picture
    //==============================================================================

    (__initialize => {
        Game_Picture.prototype.initialize = function() {
            __initialize.apply(this, arguments);
            this._spine = null;
        };
    })(Game_Picture.prototype.initialize);

    (__erase => {
        Game_Picture.prototype.erase = function() {
            __erase.apply(this, arguments);
            this._spine = null;
        };
    })(Game_Picture.prototype.erase);

    //==============================================================================
    // Sprite_Picture
    //==============================================================================

    (__initialize => {
        Sprite_Picture.prototype.initialize = function(pictureId) {
            __initialize.apply(this, arguments);
            this.addChild(new Sprite_Spine(pictureId))
        };
    })(Sprite_Picture.prototype.initialize);

    //==============================================================================
    // Game_Spine
    //==============================================================================

    class Game_Spine {
        constructor() {
            this.init();
        }

        static spineData() {
            return $p['spine data'];
        }

        static fullName(name = '') {
            for (let key in this.spineData()) {
                if (key.match(`(?:^|/)${name}$`)) {
                    return key;
                }
            }
            return '';
        }

        static loadSkeleton(name) {
            let fullName = this.fullName(name);
            let data = $p['spine data'][fullName];
            if (!data || 'animations' in data) return;
            $p['spine data'][fullName] = null;
            let loader = new (PIXI.Loader || PIXI.loaders.Loader)();
            loader.add(fullName, `img/spines/${fullName}.json`);
            loader.load((loader, resource) => {
                $p['spine data'][fullName] = resource[fullName].spineData;
            });
        }

        get skeleton() { return this._skeleton; }
        get skin() { return this._skin; }
        get track() { return this._track; }
        get timeScale() { return this._timeScale; }
        get alpha() { return this._alpha; }
        get mix() { return this._mix; }
        get color() { return this._color; }
        get mosaic() { return this._mosaic; }
        get offset() { return this._offset; }
        get scale() { return this._scale; }
        get visible() { return this._visible; }
        get bone() { return this._bone; }
        get callback() { return this._callback; }
        get playData() { return this._playData; }

        init() {
            this._skeleton  = '';
            this._skin      = [];
            this._track     = {};
            this._timeScale = 1.0;
            this._alpha     = {};
            this._mix       = {};
            this._color     = {};
            this._mosaic    = {};
            this._offset    = { x: 0, y: 0 };
            this._scale     = { x: 1.0, y: 1.0 };
            this._visible   = true;
            this._bone      = {};
            this._callback  = {};
            this._playData  = [];
        }

        setSkeleton(name = '') {
            name = convars(name);
            this.init();
            this._skeleton = name + `_${Date.now()}`;
            return this;
        }

        setSkin(...args) {
            args = convars(args);
            this._skin = args;
            return this;
        }

        setAnimation(id, animations, ...args) {
            [id, animations, args] = convars([id, animations, args]);
            this._track = {...this._track};
            let list, order, continuance, interrupt;
            if (typeof animations == 'string') {
                list        = [animations];
                order       = 'sequential';
                continuance = args[0] || 'continue';
                interrupt   = typeof args[1] == 'boolean' ? args[1] : args[1] == 'true';
            } else {
                list        = animations;
                order       = args[0] || 'sequential';
                continuance = args[1] || 'continue';
                interrupt   = typeof args[2] == 'boolean' ? args[2] : args[2] == 'true';
            }
            this._track[id] = { list: [], order: order, continuance: continuance, interrupt: interrupt };
            list.forEach(animation => {
                let [name, options] = `${animation}/`.split(/ *\/ *(?=(?:times|timeScale|alpha|$))/i);
                let times           = 1;
                let timeScale       = 1.0;
                let alpha           = 1.0;
                for (let option of options.replace(/ +/, '').split(/,/)) {
                    if (option.match(/^times=(\d+)$/i)) {
                        times = Number(RegExp.$1);
                    }
                    if (option.match(/^timeScale=(\d+\.?\d*)$/i)) {
                        timeScale = Number(RegExp.$1);
                    }
                    if (option.match(/^alpha=(\d+\.?\d*)$/i)) {
                        alpha = Number(RegExp.$1);
                    }
                }
                this._track[id].list.push({ name: name, times: times, timeScale: timeScale, alpha: alpha });
            });
            return this;
        }

        setTimeScale(value) {
            value = convars(value);
            this._timeScale = Number(value);
            return this;
        }

        setAlpha(id, value, overwrite = false) {
            [id, value, overwrite] = convars([id, value, overwrite]);
            this._alpha = {...this._alpha};
            this._alpha[id] = {
                value: Number(value),
                overwrite: typeof overwrite == 'boolean' ? overwrite : overwrite == 'true'
            };
            return this;
        }

        setMix(...args) {
            args = convars(args);
            this._mix = {...this._mix};
            let from, to, duration;
            if (args.length == 1) {
                from     = '/default';
                to       = '';
                duration = Number(args[0]);
            } else {
                from     = args[0];
                to       = args[1];
                duration = args.length > 2 ? Number(args[2]) : null;
            }
            if (duration !== null) {
                this._mix[`${from}/${to}`] = duration;
            } else {
                delete this._mix[`${from}/${to}`];
            }
            return this;
        }

        setColor(...args) {
            args = convars(args);
            this._color = {...this._color};
            let image, r, g, b, a;
            if (args.length == 4) {
                image = '/default/';
                r     = Number(args[0]);
                g     = Number(args[1]);
                b     = Number(args[2]);
                a     = Number(args[3]);
            } else {
                image = args[0];
                r     = Number(args[1]);
                g     = Number(args[2]);
                b     = Number(args[3]);
                a     = Number(args[4]);
            }
            if (r != 1 || g != 1 || b != 1 || a != 1) {
                this._color[image] = [r, g, b, a];
            } else {
                delete this._color[image];
            }
            return this;
        }

        setMosaic(...args) {
            args = convars(args);
            this._mosaic = {...this._mosaic};
            let image, size;
            if (args.length == 1) {
                image = '/default/';
                size  = Number(args[0]);
            } else {
                image = args[0];
                size  = Number(args[1]);
            }
            if (size > 1) {
                this._mosaic[image] = size;
            } else {
                delete this._mosaic[image];
            }
            return this;
        }

        setOffset(x, y) {
            [x, y] = convars([x, y]);
            this._offset = { x: Number(x), y: Number(y) };
            return this;
        }

        setScale(x, y) {
            [x, y] = convars([x, y]);
            this._scale = { x: Number(x), y: Number(y) };
            return this;
        }

        setVisible(visible) {
            this._visible = !!convars(visible);
            return this;
        }

        setBone(boneName, x, y, rotation, duration = 1, screen = true) {
            [boneName, x, y, rotation, duration, screen] = convars([boneName, x, y, rotation, duration, screen]);
            this._bone = {...this._bone};
            this._bone[boneName] = {
                x: Number(x),
                y: Number(y),
                rotation: Number(rotation),
                duration: Number(duration) || 1,
                screen: typeof screen == 'boolean' ? screen : screen == 'true'
            };
            return this;
        }

        getBoneData(boneName, screen = true) {
            [boneName, screen] = convars([boneName, screen]);
            if (typeof screen == 'string') {
                screen = screen == 'true';
            }
            return this.executeCallback('getBoneData', boneName, screen);
        }

        getAttachmentData(slotName, screen = true) {
            [slotName, screen] = convars([slotName, screen]);
            if (typeof screen == 'string') {
                screen = screen == 'true';
            }
            return this.executeCallback('getAttachmentData', slotName, screen);
        }

        hitTest(x, y, screen = true) {
            [x, y, screen] = convars([x, y, screen]);
            if (typeof screen == 'string') {
                screen = screen == 'true';
            }
            return this.executeCallback('hitTest', Number(x), Number(y), screen);
        }

        executeCallback(symbol, ...args) {
            return (callback => {
                return callback(...args);
            })(this._callback[symbol] || new Function())
        }

        setPlayData(entry) {
            let id = entry.trackIndex;
            if (!this._playData[id]) {
                this._playData[id] = [];
            }
            this._playData[id].push({
                name:        entry.animation.name,
                loop:        entry.loop,
                mixDuration: entry.mixDuration,
                timeScale:   entry.timeScale,
                alpha:       entry.alpha,
                trackTime:   0,
                state:       'ready'
            });
            for (let i = 0; i < this._playData[id].length - 1; i++) {
                this._playData[id][i].loop = false;
            }
        }

        updatePlayData(entry, reason) {
            let playData = this._playData[entry.trackIndex];
            if (!playData) return;
            let trackTime = entry.trackTime;
            let index = -1;
            let state;
            switch (reason) {
                case 'start':
                    index     = playData.findIndex(data => data.state == 'ready');
                    trackTime = 0;
                    state     = 'play';
                    break;
                case 'interrupt':
                    index = playData.findIndex(data => ['play', 'repeat'].includes(data.state));
                    state = 'suspend';
                    break;
                case 'complete':
                    index = playData.findIndex(data => ['play', 'suspend'].includes(data.state));
                    if (index >= 0) {
                        if (playData[index].state == 'play') {
                            if (index == playData.length - 1) {
                                state = entry.loop ? 'repeat' : 'done';
                            } else {
                                index = -1;
                            }
                        } else {
                            state = 'done';
                        }
                    }
                    break;
                case 'update':
                    index = playData.findIndex(data => ['play', 'repeat'].includes(data.state));
                    if (index >= 0) {
                        state = playData[index].state;
                    }
                    break;
            }
            if (index >= 0) {
                playData[index].mixDuration = entry.mixDuration;
                playData[index].trackTime   = trackTime;
                playData[index].state       = state;
                if (index > 0 && ['suspend', 'done', 'repeat'].includes(state)) {
                    playData.splice(0, index);
                }
            }
        }
    }

    window.Game_Spine = Game_Spine;

    //==============================================================================
    // Sprite_Spine
    //==============================================================================

    class Sprite_Spine extends Sprite {
        constructor(...args) {
            super();
            this._pictureId  = typeof args[0] == 'number' ? args[0] : 0;
            this._spine      = args[0] instanceof Game_Spine ? args[0] : null;
            this._animationNames = [];
            this._skinNames      = [];
            this._isRestore  = false;
            this._isPostCall = false;
            this.init();
        }

        init() {
            this.removeChild(this._data);
            this._data      = null;
            this._skeleton  = '';
            this._skin      = [];
            this._track     = {};
            this._timeScale = 1.0;
            this._alpha     = {};
            this._mix       = {};
            this._color     = {};
            this._mosaic    = {};
            this._offset    = null;
            this._scale     = null;
            this._bone      = null;
            this._postCall  = [];
        }

        spine() {
            if (this._spine) {
                return this._spine;
            }
            let picture = $gameScreen.picture(this._pictureId);
            return picture ? picture._spine : null;
        }

        createNames() {
            function generate(source) {
                return source.sort((a, b) => {
                    let la = (a.name.match(/\//g) || []).length;
                    let lb = (b.name.match(/\//g) || []).length;
                    return la - lb;
                }).map(element => element.name);
            }
            this._animationNames = generate(this._data.spineData.animations);
            this._skinNames = generate(this._data.spineData.skins);
        }

        update() {
            let spine = this.spine();
            this.updateSkeleton(spine);
            if (this._data) {
                this.updateSkin(spine);
                this.updateTimeScale(spine);
                this.updateMix(spine);
                this.updateColor(spine);
                this.updateMosaic(spine);
                this.updateOffset(spine);
                this.updateScale(spine);
                this.updateVisible(spine);
                if (this._isRestore) {
                    this.restoreAnimation(spine);
                } else {
                    this.updateAnimation(spine);
                }
                this.updateAlpha(spine);
                this.updateBone(spine);
                this.executePostCall();
                for (let entry of this._data.state.tracks) {
                    this.updatePlayData(entry, 'update');
                }
            }
        }

        updateSkeleton(spine) {
            if (spine) {
                if (spine.skeleton != this._skeleton) {
                    this.init();
                    let skeleton = spine.skeleton.replace(/_\d+$/, '');
                    if (skeleton) {
                        let fullName = Game_Spine.fullName(skeleton);
                        let data = Game_Spine.spineData()[fullName];
                        if (data) {
                            if ('animations' in data) {
                                this._data = new PIXI.spine.Spine(data);
                                this._data.destroy = function() {};
                                this._data.state.addListener({
                                    start: this.onStart.bind(this),
                                    interrupt: this.onInterrupt.bind(this),
                                    // end:       this.onEnd.bind(this),
                                    // dispose:   this.onDispose.bind(this),
                                    complete: this.onComplete.bind(this),
                                    event: this.onEvent.bind(this)
                                });
                                this.addChild(this._data);
                                if (spine.playData.length > 0) {
                                    this._isRestore = true;
                                }
                                this.registerCallback(spine);
                                this.createNames();
                            } else {
                                Game_Spine.loadSkeleton(skeleton);
                            }
                        } else if (fullName in Game_Spine.spineData() == false) {
                            throw Error(`'${skeleton}' is unknown model.`);
                        }
                    }
                    if (!skeleton || this._data) {
                        this._skeleton = spine.skeleton;
                    }
                }
            } else if (this._skeleton) {
                this.init();
            }
        }

        updateSkin(spine) {
            if (spine.skin == this._skin) return;
            this._skin = spine.skin;
            let Skin = (PIXI.spine.core || PIXI.spine).Skin || this._data.spineData.skins[0].constructor;
            let skin = new Skin(' ');
            for (let name of this._skin) {
                if (name) {
                    name = this._skinNames.find(skinName => {
                        return skinName.match(`(?:^|/)${name}$`);
                    }) || name;
                    skin.addSkin(this._data.skeleton.data.findSkin(name));
                }
            }
            this._data.skeleton.setSkin(skin);
            this._data.skeleton.setSlotsToSetupPose();
        }

        updateTimeScale(spine) {
            if (spine.timeScale == this._timeScale) return;
            this._timeScale = spine.timeScale;
            this._data.state.timeScale = this._timeScale;
        }

        updateAlpha(spine) {
            this._alpha = spine.alpha;
            this._data.state.tracks.forEach((entry, id) => {
                let alpha = this._alpha[id];
                if (alpha && entry) {
                    let value     = alpha.value;
                    let overwrite = alpha.overwrite;
                    entry.alpha = overwrite ? value : entry.plainAlpha * value;
                }
            });
        }

        updateMix(spine) {
            if (spine.mix == this._mix) return;
            for (let key in spine.mix) {
                if (spine.mix[key] != this._mix[key]) {
                    let duration = spine.mix[key];
                    if (key == '/default/') {
                        this._data.stateData.defaultMix = duration;
                    } else {
                        let [from, to] = key.split('/');
                        this._data.stateData.setMix(from, to, duration);
                    }
                }
            }
            for (let key in this._mix) {
                if (key in spine.mix == false) {
                    let [from, to] = key.split('/');
                    delete this._data.stateData.animationToMixTime[`${from}.${to}`];
                }
            }
            this._mix = spine.mix;
        }

        updateColor(spine) {
            if (spine.color == this._color) return;
            let retry = false;
            for (let image in spine.color) {
                if (spine.color[image] != this._color[image]) {
                    let color  = spine.color[image];
                    let filter = new PIXI.filters.ColorMatrixFilter();
                    filter.matrix = [
                        color[0], 0, 0, 0, 0,
                        0, color[1], 0, 0, 0,
                        0, 0, color[2], 0, 0,
                        0, 0, 0, color[3], 0
                    ];
                    let sprites = (image == '/default/') ? [this._data] : this.getSpineSprites(image);
                    for (let sprite of sprites) {
                        let filters = (sprite.filters || []).filter(filter => {
                            return filter instanceof PIXI.filters.ColorMatrixFilter == false;
                        });
                        filters.push(filter);
                        sprite.filters = filters;
                    }
                    if (image != '/default/') {
                        let count = this.getAttachments(image, 'MeshAttachment').length
                            + this.getAttachments(image, 'RegionAttachment').length;
                        if (sprites.length < count) {
                            retry = true;
                        }
                    }
                }
            }
            for (let image in this._color) {
                if (image in spine.color == false) {
                    let sprites = (image == '/default/') ? [this._data] : this.getSpineSprites(image);
                    for (let sprite of sprites) {
                        let filters = (sprite.filters || []).filter(filter => {
                            return filter instanceof PIXI.filters.ColorMatrixFilter == false;
                        });
                        sprite.filters = filters.length > 0 ? filters : null;
                    }
                }
            }
            if (!retry) {
                this._color = spine.color;
            } else {
                setTimeout(this.updateColor.bind(this, spine));
            }
        }

        updateMosaic(spine) {
            if (spine.mosaic == this._mosaic) return;
            let retry = false;
            for (let image in spine.mosaic) {
                if (spine.mosaic[image] != this._mosaic[image]) {
                    let size   = spine.mosaic[image];
                    let filter = new MosaicFilter(size);
                    let sprites = (image == '/default/') ? [this._data] : this.getSpineSprites(image);
                    for (let sprite of sprites) {
                        let filters = (sprite.filters || []).filter(filter => {
                            return filter instanceof MosaicFilter == false;
                        });
                        filters.push(filter);
                        sprite.filters = filters;
                    }
                    if (image != '/default/') {
                        let count = this.getAttachments(image, 'MeshAttachment').length
                            + this.getAttachments(image, 'RegionAttachment').length;
                        if (sprites.length < count) {
                            retry = true;
                        }
                    }
                }
            }
            for (let image in this._mosaic) {
                if (image in spine.mosaic == false) {
                    let sprites = (image == '/default/') ? [this._data] : this.getSpineSprites(image);
                    for (let sprite of sprites) {
                        let filters = (sprite.filters || []).filter(filter => {
                            return filter instanceof MosaicFilter == false;
                        });
                        sprite.filters = filters.length > 0 ? filters : null;
                    }
                }
            }
            if (!retry) {
                this._mosaic = spine.mosaic;
            } else {
                setTimeout(this.updateMosaic.bind(this, spine));
            }
        }

        updateOffset(spine) {
            if (spine.offset == this._offset) return;
            this._offset = spine.offset;
            this.x = this._offset.x;
            this.y = this._offset.y;
        }

        updateScale(spine) {
            if (spine.scale == this._scale) return;
            this._scale = spine.scale;
            this.scale.x = this._scale.x;
            this.scale.y = this._scale.y;
        }

        updateVisible(spine) {
            this.visible = spine.visible;
        }

        updateBone(spine) {
            if (spine.bone != this._bone) {
                this._bone = spine.bone;
            }
            for (let name in this._bone) {
                let bone = this._data.skeleton.findBone(name);
                if (!bone) continue;
                let _bone = { x: bone.worldX, y: bone.worldY, rotation: bone.rotation };
                let bone_p = this._bone[name];
                if ('x' in bone_p == false) {
                    bone_p.x = _bone.x;
                }
                if ('y' in bone_p == false) {
                    bone_p.y = _bone.y;
                }
                if ('rotation' in bone_p == false) {
                    bone_p.rotation = _bone.rotation;
                }
                if (bone_p.screen) {
                    [bone_p.x, bone_p.y] = this.computeLocalVertices([bone_p.x, bone_p.y]);
                }
                let duration = bone_p.duration || 1;
                let dx = (bone_p.x - _bone.x) / duration;
                let dy = (bone_p.y - _bone.y) / duration;
                let dr = (bone_p.rotation - _bone.rotation) / duration;
                let local = bone.worldToLocal({ x: bone.worldX + dx, y: bone.worldY + dy });
                bone.x += local.x;
                bone.y += local.y;
                bone.rotation += dr;
                bone_p.duration--;
                if (bone_p.duration <= 0) {
                    delete this._bone[name];
                }
            }
        }

        updateAnimation(spine) {
            if (spine.track == this._track) return;
            for (let id in spine.track) {
                if (spine.track[id] != this._track[id]) {
                    let track = spine.track[id];
                    let list  = [];
                    let loop  = track.continuance != 'none';
                    let state = this._data.state;
                    for (let animation of track.list) {
                        for (let j = 0; j < animation.times; j++) {
                            list.push(animation);
                        }
                    }
                    if (track.order == 'shuffle') {
                        let _list = [...list];
                        list = [];
                        while (_list.length > 0) {
                            let index = Math.floor(Math.random() * _list.length);
                            list.push(_list.splice(index, 1)[0]);
                        }
                    } else if (track.order == 'random') {
                        let index = Math.floor(Math.random() * list.length);
                        list = [list[index]];
                    }
                    let entry = this._data.state.getCurrent(id);
                    list.forEach((animation, index) => {
                        let name = this._animationNames.find(animationName => {
                            return animationName.match(`(?:^|/)${animation.name}$`);
                        });
                        // Fallback for _残りX (e.g. _残り6 -> fallback to _残り5, _残り4, ...)
                        if (!name && /_残り\d+$/.test(animation.name)) {
                            for (let r = 5; r >= 1; r--) {
                                let fallbackCandidate = animation.name.replace(/_残り\d+$/, `_残り${r}`);
                                name = this._animationNames.find(animationName => {
                                    return animationName.match(`(?:^|/)${fallbackCandidate}$`);
                                });
                                if (name) break;
                            }
                        }
                        if (!name && state && state.data && state.data.skeletonData) {
                            if (state.data.skeletonData.findAnimation(animation.name)) {
                                name = animation.name;
                            }
                        }
                        if (!name) {
                            console.warn("[PictureSpine] Animation not found in skeleton, safely skipped:", animation.name);
                            return;
                        }
                        let _loop = index < list.length - 1 ? false : loop;
                        try {
                            if (index == 0 && track.interrupt) {
                                entry = state.setAnimation(id, name, _loop);
                            } else {
                                entry = state.addAnimation(id, name, _loop, 0);
                            }
                            if (entry) {
                                entry.timeScale  = animation.timeScale;
                                entry.alpha      = animation.alpha;
                                entry.plainAlpha = animation.alpha;
                                spine.setPlayData(entry);
                            }
                        } catch (e) {
                            console.warn("[PictureSpine] setAnimation error safely caught:", e);
                        }
                    });
                }
            }
            this._track = spine.track;
        }

        restoreAnimation(spine) {
            let timeScale          = this._data.state.timeScale;
            let animationToMixTime = this._data.stateData.animationToMixTime;
            let defaultMix         = this._data.stateData.defaultMix;
            this._data.state.timeScale              = 0;
            this._data.stateData.animationToMixTime = {};
            this._data.stateData.defaultMix         = 0;
            let lastTimeScale = {};
            for (let playData of spine.playData.filter(Boolean)) {
                let id = spine.playData.indexOf(playData)
                for (let data of playData) {
                    let entry;
                    switch (data.state) {
                        case 'suspend':
                        case 'done':
                            entry = this._data.state.setAnimation(id, data.name, false);
                            entry.alpha      = data.alpha;
                            entry.plainAlpha = data.alpha;
                            while (entry.trackTime < data.trackTime) {
                                this._data.state.timeScale = Math.min(data.trackTime - entry.trackTime, 0.01);
                                this._data.update(1);
                            }
                            break;
                        case 'play':
                        case 'repeat':
                            let _foundAnim = this._data.spineData.animations.find(animation => animation.name == data.name);
                            if (!_foundAnim) {
                                console.warn("[PictureSpine] restoreAnimation: animation not found:", data.name);
                                break;
                            }
                            data.trackTime %= _foundAnim.duration;
                            this._data.stateData.defaultMix = data.mixDuration;
                            entry = this._data.state.setAnimation(id, data.name, data.loop);
                            entry.alpha      = data.alpha;
                            entry.plainAlpha = data.alpha;
                            while (entry.trackTime < data.trackTime) {
                                this._data.state.timeScale = Math.min(data.trackTime - entry.trackTime, 0.01);
                                this._data.update(1);
                            }
                            entry.timeScale = 0;
                            lastTimeScale[id] = data.timeScale;
                            break;
                        default:
                            this._data.stateData.defaultMix = data.mixDuration;
                            entry = this._data.state.addAnimation(id, data.name, data.loop, 0);
                            entry.timeScale  = data.timeScale;
                            entry.alpha      = data.alpha;
                            entry.plainAlpha = data.alpha;
                            break;
                    }
                }
            }
            for (let id in lastTimeScale) {
                this._data.state.tracks[Number(id)].timeScale = lastTimeScale[id];
            }
            this._data.state.timeScale              = timeScale;
            this._data.stateData.animationToMixTime = animationToMixTime;
            this._data.stateData.defaultMix         = defaultMix;
            this._track = spine.track;
            this._isRestore = false;
        }

        updatePlayData(entry, reason) {
            let spine = this.spine();
            if (!entry || !spine) return;
            spine.updatePlayData(entry, reason);
        }

        registerCallback(spine) {
            spine.callback['getBoneData']       = this.getBoneData.bind(this);
            spine.callback['getAttachmentData'] = this.getAttachmentData.bind(this);
            spine.callback['hitTest']           = this.hitTest.bind(this);
        }

        getAttachments(name, type) {
            let attachments = [];
            if (this._data) {
                for (let slot of this._data.skeleton.slots) {
                    let attachment = slot.attachment;
                    if (attachment && (!type || attachment.constructor.name == type)) {
                        if (attachment.name == name) {
                            attachments.push(attachment);
                        }
                    }
                }
            }
            return attachments;
        }

        getSpineSprites(name) {
            let sprites = [];
            if (this._data) {
                for (let child1 of this._data.children) {
                    for (let child2 of child1.children) {
                        if (child2.region && child2.region.name == name) {
                            sprites.push(child2);
                        }
                    }
                }
            }
            return sprites;
        }

        getBoneData(boneName, screen = true) {
            let bone = this._data.skeleton.findBone(boneName);
            if (!bone) return null;
            let data = {
                x: bone.worldX,
                y: bone.worldY,
                rotation: bone.rotation
            };
            if (screen) {
                [data.x, data.y] = this.computeScreenVertices([data.x, data.y]);
            }
            return data;
        }

        getAttachmentData(slotName, screen = true) {
            let slot = this._data.skeleton.findSlot(slotName);
            if (!slot) return null;
            let attachment = slot.getAttachment();
            if (!attachment) return null;
            let attachmentType = attachment.constructor.name;
            let data = {};
            if (attachmentType.match(/^VertexAttachment/)) {
                if (attachment.vertices) {
                    let vertices = [];
                    attachment.computeWorldVertices(slot, 0, attachment.worldVerticesLength, vertices, 0, 2);
                    if (screen) {
                        this.computeScreenVertices(vertices);
                    }
                    data.vertices = vertices;
                }
            }
            if (attachmentType.match(/^ClippingAttachment/)) {
                data.endSlotName = attachment.endSlot.name;
            }
            if (attachmentType.match(/^PathAttachment/)) {
                data.lengths       = attachment.lengths;
                data.closed        = attachment.closed;
                data.constantSpeed = attachment.constantSpeed;
            }
            if (attachmentType.match(/^PointAttachment/)) {
                let position = attachment.computeWorldPosition(slot.bone, {});
                let rotation = attachment.computeWorldRotation(slot.bone);
                if (screen) {
                    [position.x, position.y] = this.computeScreenVertices([position.x, position.y]);
                }
                data.x        = position.x;
                data.y        = position.y;
                data.rotation = rotation;
            }
            return { slotName: slotName, attachmentName: attachment.name, data: data };
        }

        hitTest(x, y, screen = true) {
            let SkeletonBounds = (PIXI.spine.core || PIXI.spine).SkeletonBounds;
            let hits = [];
            let bounds = new SkeletonBounds();
            bounds.update(this._data.skeleton, true);
            let polygons = bounds.polygons;
            for (let i = 0; i < polygons.length; i++) {
                let polygon = polygons[i];
                if (screen) {
                    this.computeScreenVertices(polygon);
                }
                if (bounds.containsPointPolygon(polygon, x, y)) {
                    let attachment = bounds.boundingBoxes[i];
                    let slot = this._data.skeleton.slots.find(slot => slot.attachment == attachment);
                    hits.push({
                        slotName: slot.data.name,
                        attachmentName: attachment.name,
                        data: {
                            vertices: polygon
                        }
                    });
                }
            }
            return hits;
        }

        computeScreenVertices(vertices) {
            let parent = this;
            while (parent) {
                for (let i = 0; i < vertices.length; i += 2) {
                    let [x, y] = [vertices[i], vertices[i + 1]];
                    x *= parent.scale.x;
                    y *= parent.scale.y;
                    [x, y] = [
                        Math.cos(parent.rotation) * x - Math.sin(parent.rotation) * y,
                        Math.sin(parent.rotation) * x + Math.cos(parent.rotation) * y
                    ];
                    x += parent.x;
                    y += parent.y;
                    [vertices[i], vertices[i + 1]] = [x, y];
                }
                parent = parent.parent;
            }
            return vertices;
        }

        computeLocalVertices(vertices) {
            !function calc(parent) {
                if (parent.parent) {
                    calc(parent.parent);
                }
                for (let i = 0; i < vertices.length; i += 2) {
                    let [x, y] = [vertices[i], vertices[i + 1]];
                    x -= parent.x;
                    y -= parent.y;
                    [x, y] = [
                        Math.cos(-parent.rotation) * x - Math.sin(-parent.rotation) * y,
                        Math.sin(-parent.rotation) * x + Math.cos(-parent.rotation) * y
                    ];
                    x /= parent.scale.x;
                    y /= parent.scale.y;
                    [vertices[i], vertices[i + 1]] = [x, y];
                }
            }(this);
            return vertices;
        }

        reservePostCall(callback) {
            this._postCall.push(callback);
        }

        executePostCall() {
            this._isPostCall = true;
            while (this._postCall[0]) {
                let callback = this._postCall.shift();
                callback();
            }
            this._isPostCall = false;
        }

        onStart(entry) {
            if (this._isRestore) return;
            if (entry.trackTime == 0 && !this._isPostCall) {
                this.reservePostCall(this.onStart.bind(this, entry));
                return;
            }
            this.updatePlayData(entry, 'start');
            if (!entry.next) {
                let spine = this.spine();
                let index = entry.trackIndex;
                if (spine && spine.track[index]) {
                    if (spine.track[index] == this._track[index]) {
                        if (this._track[index].continuance == 'reset') {
                            spine.track[index].interrupt = false;
                            this._track = {...this._track};
                            this._track[index] = null;
                        }
                    }
                }
            }
        }

        onInterrupt(entry) {
            if (this._isRestore) return;
            if (entry.trackTime == 0 && !this._isPostCall) {
                this.reservePostCall(this.onInterrupt.bind(this, entry));
                return;
            }
            this.updatePlayData(entry, 'interrupt');
        }

        onEnd(entry) {
        }

        onDispose(entry) {
        }

        onComplete(entry) {
            if (this._isRestore) return;
            if (entry.trackTime == 0 && !this._isPostCall) {
                this.reservePostCall(this.onComplete.bind(this, entry));
                return;
            }
            this.updatePlayData(entry, 'complete');
        }

        onEvent(entry, event) {
            if (this._isRestore) return;
            let audioPath = event.data.audioPath;
            let audioData = event.data.audioData;
            if (audioPath) {
                if (!audioData) {
                    let values         = audioPath.replace(/\.[^.]+$/, '').split(/\/(?=[^/]+$)/);
                    let [folder, file] = values.length > 1 ? [...values] : ['', ...values];
                    let stringValue    = event.data.stringValue;
                    let volume         = event.data.volume * 100;
                    let balance        = event.data.balance * 100;
                    let volumeId, balanceId;
                    for (let value of stringValue.replace(/ +/, '').split(/,/)) {
                        if (value.match(/^volume:(\d+)$/i)) {
                            volumeId = Number(RegExp.$1);
                        }
                        if (value.match(/^balance:(\d+)$/i)) {
                            balanceId = Number(RegExp.$1);
                        }
                    }
                    audioData = event.data.audioData = { folder: folder, file: file, volume: volume, volumeId: volumeId, balance: balance, balanceId: balanceId };
                }
                let folder    = audioData.folder;
                let file      = audioData.file;
                let volumeId  = audioData.volumeId;
                let balanceId = audioData.balanceId;
                let volume    = volumeId ? $gameVariables.value(volumeId) : audioData.volume;
                let balance   = balanceId ? $gameVariables.value(balanceId) : audioData.balance;
                AudioManager._subFolder = folder;
                AudioManager.playSe({ name: file, volume: volume, pitch: 100, pan: balance });
            }
            let switches = event.switches;
            if (switches == null) {
                switches = {};
                let stringValue = event.stringValue;
                for (let value of stringValue.replace(/ +/, '').split(/,/)) {
                    if (value.match(/^([!~]?)switch:(\d+)$/i)) {
                        let type = RegExp.$1.replace('!', 'off').replace('~', 'reverse') || 'on';
                        switches[RegExp.$2] = type;
                    }
                }
                event.switches = switches;
            }
            for (let id in switches) {
                let type = switches[id];
                let value = type == 'on' ? true : type == 'off' ? false : !$gameSwitches.value(id);
                $gameSwitches.setValue(id, value);
            }
        }
    }

    window.Sprite_Spine = Sprite_Spine;
}();
