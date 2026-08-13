//=============================================================================
// AutoWordWrap.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Tự động xuống dòng hội thoại cho tiếng Việt / tiếng Anh trong RPG Maker MZ.
 * @author Localizer
 *
 * @help AutoWordWrap.js
 * Tự động ngắt dòng khi câu thoại vượt quá chiều rộng khung hội thoại Window_Message.
 */

(() => {
    const _Window_Message_startMessage = Window_Message.prototype.startMessage;
    Window_Message.prototype.startMessage = function() {
        if ($gameMessage._texts && $gameMessage._texts.length > 0) {
            const rawText = $gameMessage.allText();
            const wrappedText = this.autoWrapText(rawText);
            $gameMessage._texts = [wrappedText];
        }
        _Window_Message_startMessage.call(this);
    };

    Window_Message.prototype.autoWrapText = function(text) {
        if (!text) return text;

        const faceExists = $gameMessage.faceName() !== '';
        const faceWidth = ImageManager.faceWidth || 144;
        const margin = faceExists ? faceWidth + 16 : 12;
        const windowW = this.innerWidth || (Graphics.boxWidth ? Graphics.boxWidth - 36 : 780);
        const maxW = Math.min(windowW - margin - 15, faceExists ? 640 : 765);

        const lines = text.split('\n');
        const wrappedLines = [];

        for (let line of lines) {
            const cleanLine = line.replace(/\\C\[\d+\]|\\N\[\d+\]|\\V\[\d+\]|\\c\[\d+\]|\\I\[\d+\]|\\P\[\d+\]|\\\{\|\}/gi, '');
            const lineW = this.contents ? this.contents.measureTextWidth(cleanLine) : cleanLine.length * 15;

            if (lineW <= maxW) {
                wrappedLines.push(line);
                continue;
            }

            const words = line.split(' ');
            let curWords = [];

            for (let i = 0; i < words.length; i++) {
                const word = words[i];
                const testWords = curWords.concat([word]);
                const testLineClean = testWords.join(' ').replace(/\\C\[\d+\]|\\N\[\d+\]|\\V\[\d+\]|\\c\[\d+\]|\\I\[\d+\]|\\P\[\d+\]|\\\{\|\}/gi, '');
                const testW = this.contents ? this.contents.measureTextWidth(testLineClean) : testLineClean.length * 15;

                if (testW > maxW && curWords.length > 0) {
                    // Punctuation-aware smart break: Look for comma/punctuation from right to left
                    let splitIdx = -1;
                    for (let idx = curWords.length - 1; idx >= 0; idx--) {
                        const cand = curWords[idx].replace(/\\C\[\d+\]|\\N\[\d+\]|\\V\[\d+\]|\\c\[\d+\]|\\I\[\d+\]/gi, '');
                        const partialClean = curWords.slice(0, idx + 1).join(' ').replace(/\\C\[\d+\]|\\N\[\d+\]|\\V\[\d+\]|\\c\[\d+\]|\\I\[\d+\]/gi, '');
                        const partialW = this.contents ? this.contents.measureTextWidth(partialClean) : partialClean.length * 15;

                        // Only break at punctuation if line has reached at least 50% of maxW
                        if (partialW >= maxW * 0.50) {
                            if (/[,;—.\!?]$/.test(cand)) {
                                splitIdx = idx;
                                break;
                            }
                        }
                    }

                    if (splitIdx !== -1) {
                        wrappedLines.push(curWords.slice(0, splitIdx + 1).join(' '));
                        curWords = curWords.slice(splitIdx + 1).concat([word]);
                    } else {
                        wrappedLines.push(curWords.join(' '));
                        curWords = [word];
                    }
                } else {
                    curWords.push(word);
                }
            }

            if (curWords.length > 0) {
                wrappedLines.push(curWords.join(' '));
            }
        }

        return wrappedLines.join('\n');
    };
})();
