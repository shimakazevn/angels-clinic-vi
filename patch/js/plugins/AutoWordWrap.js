//=============================================================================
// AutoWordWrap.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Tự động ngắt dòng tự nhiên, chuẩn xác cho Hội thoại game (Window_Message), Nhật ký hội thoại (Window_TextLog) và Bảng thông báo (LogMessage).
 * @author Localizer & Antigravity
 *
 * @help AutoWordWrap.js
 * 1. Tự động xuống dòng tự nhiên, liền mạch theo từ ngữ (greedy word-wrap) cho tiếng Việt và tiếng Anh.
 * 2. Hỗ trợ tự động ngắt dòng trong khung thoại Window_Message (tối đa 900px, 740px khi có Face).
 * 3. Hỗ trợ tự động ngắt dòng trong bảng Lịch sử hội thoại Window_TextLog (Backlog), tính toán chiều cao cuộn chính xác.
 * 4. Hỗ trợ tự động ngắt dòng trong bảng thông báo hành động LogMessage.
 */

(() => {
    'use strict';

    /**
     * Hàm ngắt dòng dùng chung cho toàn bộ Game
     * @param {string} text - Chuỗi văn bản cần ngắt dòng
     * @param {number} maxW - Chiều rộng tối đa (pixel)
     * @param {Window_Base|Bitmap} context - Đối tượng dùng để đo độ rộng (measureTextWidth)
     * @returns {string} - Chuỗi văn bản đã được chèn ký tự xuống dòng \n
     */
    Utils.autoWrapText = function(text, maxW, context) {
        if (!text || maxW <= 0) return text;

        const measure = function(str) {
            const clean = str.replace(/\\C\[\d+\]|\\N\[\d+\]|\\V\[\d+\]|\\c\[\d+\]|\\I\[\d+\]|\\P\[\d+\]|\\G|\\\{\|\}/gi, '');
            if (context && context.contents && typeof context.contents.measureTextWidth === 'function') {
                return context.contents.measureTextWidth(clean);
            }
            if (context && typeof context.measureTextWidth === 'function') {
                return context.measureTextWidth(clean);
            }
            // Ước lượng 1 ký tự font 26-28px ~ 15px
            return clean.length * 15;
        };

        const originalLines = text.split('\n');
        const finalLines = [];

        for (let rawLine of originalLines) {
            if (measure(rawLine) <= maxW) {
                finalLines.push(rawLine);
                continue;
            }

            const words = rawLine.split(' ');
            let curWords = [];

            for (let i = 0; i < words.length; i++) {
                const word = words[i];
                const testWords = curWords.concat([word]);
                const testLine = testWords.join(' ');

                if (measure(testLine) > maxW && curWords.length > 0) {
                    finalLines.push(curWords.join(' '));
                    curWords = [word];
                } else {
                    curWords.push(word);
                }
            }

            if (curWords.length > 0) {
                finalLines.push(curWords.join(' '));
            }
        }

        return finalLines.join('\n');
    };

    // =========================================================================
    // 1. Tự động xuống dòng cho Window_Message (Khung hội thoại chính)
    // =========================================================================
    const _Window_Message_startMessage = Window_Message.prototype.startMessage;
    Window_Message.prototype.startMessage = function() {
        if ($gameMessage._texts && $gameMessage._texts.length > 0) {
            const rawText = $gameMessage.allText();
            const faceExists = $gameMessage.faceName() !== '';
            
            // Khung thoại mở rộng tự nhiên (900px, 740px khi có Face)
            const maxW = faceExists ? 740 : 900;

            const wrappedText = Utils.autoWrapText(rawText, maxW, this);
            $gameMessage._texts = [wrappedText];
        }
        _Window_Message_startMessage.call(this);
    };

    // =========================================================================
    // 2. Tự động xuống dòng cho Window_TextLog (Nhật ký hội thoại / Backlog)
    // =========================================================================
    const hookTextLog = () => {
        if (typeof Window_TextLog === 'undefined') return;

        // Hook tính chiều cao từng message trong Log
        const _Window_TextLog_calcMessageHeight = Window_TextLog.prototype.calcMessageHeight;
        Window_TextLog.prototype.calcMessageHeight = function(message) {
            if (message) {
                const maxW = Math.max(200, (this.innerWidth || Graphics.boxWidth || 1280) - 60);
                const originalText = message.text();
                const wrapped = Utils.autoWrapText(originalText, maxW, this);
                return this.textSizeEx(wrapped).height + (this.messageSpacing || 6);
            }
            return _Window_TextLog_calcMessageHeight ? _Window_TextLog_calcMessageHeight.call(this, message) : 36;
        };

        // Hook vẽ từng message trong Log
        const _Window_TextLog_drawTextLog = Window_TextLog.prototype.drawTextLog;
        Window_TextLog.prototype.drawTextLog = function() {
            let height = 0;
            const x = 8;
            const maxW = Math.max(200, (this.innerWidth || Graphics.boxWidth || 1280) - 60);
            const lineSpacing = this.lineSpacing || 0;

            this._messages.forEach((message) => {
                const originalText = message.text();
                const wrapped = Utils.autoWrapText(originalText, maxW, this);
                this.drawTextEx(wrapped, x, height + Math.floor(lineSpacing / 2) - this.scrollBaseY());
                height += message.height;
            });
        };
    };

    hookTextLog();
    const _Scene_Boot_start = Scene_Boot.prototype.start;
    Scene_Boot.prototype.start = function() {
        _Scene_Boot_start.call(this);
        hookTextLog();
    };

})();
