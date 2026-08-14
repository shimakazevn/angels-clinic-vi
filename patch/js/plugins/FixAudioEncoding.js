//=============================================================================
// FixAudioEncoding.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Fixes audio loading errors when game is unzipped with non-Japanese codepages (Shift-JIS Mojibake Fallback).
 * @author Antigravity
 * @help
 * Automatically resolves audio loading for corrupted or mojibake filenames.
 */

(() => {
    const fs = (typeof require === 'function') ? require('fs') : null;
    const path = (typeof require === 'function') ? require('path') : null;

    // Cache of discovered audio filenames
    const audioCache = {};

    function scanAudioDir(folder) {
        if (!fs || !path) return;
        const dirPath = path.join(path.dirname(process.mainModule.filename), 'audio', folder);
        if (!fs.existsSync(dirPath)) return;
        try {
            const files = fs.readdirSync(dirPath);
            audioCache[folder] = files;
        } catch (e) {
            console.warn('Could not read audio dir:', dirPath, e);
        }
    }

    // Pre-scan all audio folders
    ['bgm', 'bgs', 'me', 'se'].forEach(scanAudioDir);

    const _AudioManager_createBuffer = AudioManager.createBuffer;
    AudioManager.createBuffer = function(folder, name) {
        let finalName = name;
        if (fs && path && audioCache[folder]) {
            const ext = this.audioFileExt();
            const targetFile = name + ext;
            const files = audioCache[folder];

            // 1. Direct match
            if (!files.includes(targetFile)) {
                // 2. Try to find matching file by length, partial characters or suffix
                let matched = null;
                
                // Exact suffix / number match (e.g. _2.ogg, (Dreaming_world).ogg, (Quiet_suggestiveness).ogg)
                for (const f of files) {
                    if (name.includes('_2') && f.includes('_2.ogg')) {
                        matched = f.slice(0, -ext.length);
                        break;
                    }
                    if (name.includes('Dreaming_world') && f.includes('Dreaming_world')) {
                        matched = f.slice(0, -ext.length);
                        break;
                    }
                    if (name.includes('Quiet_suggestiveness') && f.includes('Quiet_suggestiveness')) {
                        matched = f.slice(0, -ext.length);
                        break;
                    }
                    if (name.includes('深夜にまったり') && f.includes('深夜にまったり')) {
                        matched = f.slice(0, -ext.length);
                        break;
                    }
                    if (name.includes('編集済み') && (f.includes('編集済み') || f.includes('Midnight_Isolation'))) {
                        matched = f.slice(0, -ext.length);
                        break;
                    }
                }

                if (matched) {
                    finalName = matched;
                }
            }
        }
        return _AudioManager_createBuffer.call(this, folder, finalName);
    };

    // Retry fallback on WebAudio error
    const _WebAudio_prototype_load = WebAudio.prototype._load;
    WebAudio.prototype._load = function(url) {
        this._originalUrl = url;
        _WebAudio_prototype_load.call(this, url);
    };

    const _WebAudio_prototype_onError = WebAudio.prototype._onError;
    WebAudio.prototype._onError = function() {
        // If node environment and file exists with alternate encoding, retry
        if (fs && path && this._originalUrl && !this._retriedAlternate) {
            this._retriedAlternate = true;
            try {
                // Try decoding URL
                const decodedPath = decodeURIComponent(this._originalUrl);
                const fullPath = path.join(path.dirname(process.mainModule.filename), decodedPath);
                const dir = path.dirname(fullPath);
                const baseName = path.basename(fullPath);
                
                if (fs.existsSync(dir)) {
                    const allFiles = fs.readdirSync(dir);
                    // If there is only one or matching ogg file
                    const candidates = allFiles.filter(f => f.toLowerCase().endsWith('.ogg'));
                    if (candidates.length > 0) {
                        // Find best candidate
                        let best = candidates[0];
                        if (baseName.includes('_2')) {
                            const c2 = candidates.find(f => f.includes('_2'));
                            if (c2) best = c2;
                        }
                        const newUrl = path.join(path.dirname(this._originalUrl), encodeURIComponent(best)).replace(/\\/g, '/');
                        _WebAudio_prototype_load.call(this, newUrl);
                        return;
                    }
                }
            } catch (err) {
                console.warn('Audio fallback error:', err);
            }
        }
        _WebAudio_prototype_onError.call(this);
    };
})();
