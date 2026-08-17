//=============================================================================
// FixAudioEncoding.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Supports Japanese, English Romaji (Kimochi build), and Mojibake audio filenames seamlessly.
 * @author Antigravity
 * @help
 * Automatically resolves audio loading for:
 * 1. Original Japanese filenames
 * 2. Romaji filenames (Kimochi EN translation build)
 * 3. Mojibake unzipped filenames
 */

(() => {
    const fs = (typeof require === 'function') ? require('fs') : null;
    const path = (typeof require === 'function') ? require('path') : null;

    const AUDIO_MAP = {
    "ガーデン・シティ_2": [
        "gaaden_shitei_2",
        "K[fEVeB_2",
        "ƒK[ƒfƒ“EƒVƒeƒB_2",
        "garden_city_2"
    ],
    "ドラマティック・シティ": [
        "doramateikku_shitei",
        "h}eBbNEVeB",
        "ƒhƒ‰ƒ}ƒeƒBƒbƒNEƒVƒeƒB",
        "dramatic_city"
    ],
    "今日は、気ままなカフェ巡り。": [
        "konnichiha_kimamanakafemeguri",
        "ACJtFB",
        "¡“ú‚ÍA‹C‚Ü‚Ü‚ÈƒJƒtƒF„‚èB",
        "cafe_meguri"
    ],
    "優しい心、温かい日": [
        "yasashiikokoro_atatakainichi",
        "DSA",
        "—D‚µ‚¢SA‰·‚©‚¢“ú",
        "warm_day"
    ],
    "夏が呼んでいる": [
        "natsugayondeiru",
        "ĂĂł",
        "‰Ä‚ªŒÄ‚ñ‚Å‚¢‚é",
        "summer_calling"
    ],
    "夢見る世界(Dreaming_world)": [
        "yumemirusekai_dreaming_world",
        "E(Dreaming_world)",
        "–²Œ©‚é¢ŠE(Dreaming_world)",
        "Dreaming_world"
    ],
    "奈落への巡行": [
        "narakuhenojunkou",
        "s",
        "“Þ—Ž‚Ö‚Ì„s",
        "naraku"
    ],
    "月曜日の庭": [
        "getsuyoubinoniwa",
        "j",
        "ŒŽ—j“ú‚Ì’ë",
        "monday_garden"
    ],
    "波に揺られる": [
        "naminiyurareru",
        "gh",
        "”g‚É—h‚ç‚ê‚é",
        "swaying_waves"
    ],
    "狼達の行軍": [
        "ookamitoorunokougun",
        "TBsR",
        "˜T’B‚ÌsŒR",
        "wolf_march"
    ],
    "秘境の地": [
        "hikyounochi",
        "n",
        "”é‹«‚Ì’n",
        "hidden_land"
    ],
    "霧の中へ": [
        "kirinonakahe",
        "–¶‚Ì’†‚Ö",
        "into_the_fog"
    ],
    "静かな余韻(Quiet_suggestiveness)": [
        "shizukanayoin_quiet_suggestiveness",
        "]C(Quiet_suggestiveness)",
        "Ã‚©‚È—]‰C(Quiet_suggestiveness)",
        "Quiet_suggestiveness"
    ],
    "Lazy_Midnight(深夜にまったり)": [
        "lazy_midnight_shinyanimattari",
        "Lazy_Midnight([)",
        "Lazy_Midnight([–é‚É‚Ü‚Á‚½‚è)",
        "Lazy_Midnight"
    ],
    "Midnight_Isolation_編集済み": [
        "midnight_isolation_henshuusumi",
        "Midnight_Isolation_W",
        "Midnight_Isolation_•ÒWÏ‚Ý",
        "Midnight_Isolation"
    ],
    "ぬるぐちゃ001": [
        "nurugucha001",
        "001",
        "‚Ê‚é‚®‚¿‚á001"
    ],
    "ぬるぐちゃ003": [
        "nurugucha003",
        "003",
        "‚Ê‚é‚®‚¿‚á003"
    ],
    "パイズリ": [
        "paizuri",
        "pCY",
        "ƒpƒCƒYƒŠ"
    ],
    "パイズリ2": [
        "paizuri2",
        "pCY2",
        "ƒpƒCƒYƒŠ2"
    ],
    "パイズリカウベル入り": [
        "paizurikauberuiri",
        "pCYJEx",
        "ƒpƒCƒYƒŠƒJƒEƒxƒ‹“ü‚è"
    ],
    "パイズリカウベル入り2": [
        "paizurikauberuiri2",
        "pCYJEx2",
        "ƒpƒCƒYƒŠƒJƒEƒxƒ‹“ü‚è2"
    ],
    "ピストン ウェット": [
        "pisuton_wetto",
        "pisuton wetto",
        "sXg EFbg",
        "ƒsƒXƒgƒ“ ƒEƒFƒbƒg"
    ],
    "フェラＳＥ（中）長": [
        "feraSE_chuu_chou",
        "feraSE_chuu",
        "tFrdij",
        "ƒtƒFƒ‰‚r‚di’†j’·"
    ],
    "フェラＳＥ（強）長": [
        "feraSE_kyou_chou",
        "feraSE_kyou",
        "tFrdij",
        "ƒtƒFƒ‰‚r‚di‹­j’·"
    ],
    "手コキ３（低速～中速）": [
        "tekoki3_teisoku_chuusoku",
        "tekoki3",
        "RLRi`j",
        "ŽèƒRƒL‚Ri’á‘¬`’†‘¬j"
    ],
    "手コキ５（中速）": [
        "tekoki5_chuusoku",
        "tekoki5",
        "RLTij",
        "ŽèƒRƒL‚Ti’†‘¬j"
    ],
    "手コキ６（中速～高速）": [
        "tekoki6_chuusoku_kousoku",
        "tekoki6",
        "RLUi`j",
        "ŽèƒRƒL‚Ui’†‘¬`‚‘¬j"
    ],
    "1.ハードピストン（低速）": [
        "1.haadopisuton_teisoku",
        "1.haadopisuton",
        "1.n[hsXgij",
        "1.ƒn[ƒhƒsƒXƒgƒ“i’á‘¬j"
    ],
    "2.ハードピストン（低速～中速）08倍速": [
        "2.haadopisuton_teisoku_chuusoku_08baisoku",
        "2.haadopisuton",
        "2.n[hsXgi`j08{",
        "2.ƒn[ƒhƒsƒXƒgƒ“i’á‘¬`’†‘¬j08”{‘¬"
    ],
    "3.ハードピストン（中速）": [
        "3.haadopisuton_chuusoku",
        "3.haadopisuton",
        "3.n[hsXgij",
        "3.ƒn[ƒhƒsƒXƒgƒ“i’†‘¬j"
    ]
};

    // Cache of available audio filenames per folder
    const audioCache = {};

    function scanAudioDir(folder) {
        if (!fs || !path) return;
        try {
            const basePath = path.dirname(process.mainModule.filename);
            const dirPath = path.join(basePath, 'audio', folder);
            if (fs.existsSync(dirPath)) {
                audioCache[folder] = fs.readdirSync(dirPath);
            }
        } catch (e) {
            console.warn('[FixAudioEncoding] Scan error for folder ' + folder, e);
        }
    }

    ['bgm', 'bgs', 'me', 'se'].forEach(scanAudioDir);

    function findActualAudioName(folder, reqName) {
        if (!fs || !path) return reqName;
        if (!audioCache[folder]) scanAudioDir(folder);
        const files = audioCache[folder];
        if (!files || files.length === 0) return reqName;

        const reqOgg = (reqName + '.ogg').toLowerCase();
        
        // 1. Direct match (case-insensitive)
        const direct = files.find(f => f.toLowerCase() === reqOgg);
        if (direct) return direct.slice(0, -4);

        // 2. Check predefined alias table
        const aliases = AUDIO_MAP[reqName];
        if (aliases) {
            for (const alias of aliases) {
                const aliasOgg = (alias + '.ogg').toLowerCase();
                const matched = files.find(f => f.toLowerCase() === aliasOgg || f.toLowerCase().includes(alias.toLowerCase()));
                if (matched) return matched.slice(0, -4);
            }
        }

        // 3. Reverse check (if reqName is an alias, find Japanese or other alias)
        for (const [jpName, aliasList] of Object.entries(AUDIO_MAP)) {
            if (aliasList.some(a => a.toLowerCase() === reqName.toLowerCase())) {
                const jpMatch = files.find(f => f.toLowerCase() === (jpName + '.ogg').toLowerCase());
                if (jpMatch) return jpMatch.slice(0, -4);
                for (const otherAlias of aliasList) {
                    const otherMatch = files.find(f => f.toLowerCase() === (otherAlias + '.ogg').toLowerCase() || f.toLowerCase().includes(otherAlias.toLowerCase()));
                    if (otherMatch) return otherMatch.slice(0, -4);
                }
            }
        }

        // 4. Fuzzy fallback (e.g. matching numbers or words like '_2')
        if (reqName.includes('_2')) {
            const match2 = files.find(f => f.toLowerCase().includes('_2.ogg'));
            if (match2) return match2.slice(0, -4);
        }

        return reqName;
    }

    const _AudioManager_createBuffer = AudioManager.createBuffer;
    AudioManager.createBuffer = function(folder, name) {
        const actualName = findActualAudioName(folder, name);
        return _AudioManager_createBuffer.call(this, folder, actualName);
    };

    const _WebAudio_prototype_load = WebAudio.prototype._load;
    WebAudio.prototype._load = function(url) {
        this._reqUrl = url;
        _WebAudio_prototype_load.call(this, url);
    };

    const _WebAudio_prototype_onError = WebAudio.prototype._onError;
    WebAudio.prototype._onError = function() {
        if (fs && path && this._reqUrl && !this._retryFallback) {
            this._retryFallback = true;
            try {
                const decoded = decodeURIComponent(this._reqUrl);
                const parts = decoded.split('/');
                const folder = parts[parts.length - 2];
                const baseName = parts[parts.length - 1].replace(/\.ogg$/i, '');
                const found = findActualAudioName(folder, baseName);
                if (found && found !== baseName) {
                    const newUrl = (parts.slice(0, parts.length - 1).join('/') + '/' + encodeURIComponent(found) + '.ogg').replace(/\\/g, '/');
                    _WebAudio_prototype_load.call(this, newUrl);
                    return;
                }
            } catch (err) {
                console.warn('[FixAudioEncoding] Fallback error', err);
            }
        }
        _WebAudio_prototype_onError.call(this);
    };
})();
