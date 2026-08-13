//=============================================================================
// LatinNameInput.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc Thay thế bàn phím tiếng Nhật bằng Bàn phím Latinh.
 * @author Localizer
 *
 * @help LatinNameInput.js
 */

(() => {
    Window_NameInput.prototype.table = function() {
        return [Window_NameInput.LATIN1, Window_NameInput.LATIN2];
    };
})();
