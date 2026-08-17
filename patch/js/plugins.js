var $plugins =
[
  {
    "name": "PluginCommonBase",
    "status": true,
    "description": "Thư viện cơ bản Nukazuke",
    "parameters": {}
  },
  {
    "name": "DevToolsManage",
    "status": true,
    "description": "Hiển thị hội thoại tự động dạng Baloon",
    "parameters": {
      "StartupDevTool": "false",
      "ShortcutList": "[\"{\\\"Command\\\":\\\"ToggleRapid\\\",\\\"HotKey\\\":\\\"F10\\\",\\\"Alt\\\":\\\"false\\\",\\\"Ctrl\\\":\\\"false\\\"}\"]",
      "ShowFPS": "OFF",
      "CutTitle": "0",
      "RapidStart": "false",
      "RapidSpeed": "2",
      "SlowSpeed": "2",
      "InvalidMessageSkip": "false",
      "MenuBarVisible": "true",
      "ClickMenu": "1",
      "OutputStartupInfo": "true",
      "StartupOnTop": "false",
      "UseReloadData": "true",
      "UseBreakPoint": "false"
    }
  },
  {
    "name": "MakeScreenCapture",
    "status": true,
    "description": "Thay đổi hình nền cửa sổ hội thoại",
    "parameters": {
      "FileName": "image_%1_%2",
      "LocationText": "captures",
      "FileFormat": "png",
      "Quality": "9",
      "Signature": "{}",
      "Interval": "0",
      "SoundEffect": "{}",
      "OpenDirectory": "true",
      "Trimming": "{}"
    }
  },
  {
    "name": "PictureSpine",
    "status": true,
    "description": "Cố định chiều rộng phông chữ biểu tượng",
    "parameters": {
      "json file": "[\"UI 戦闘\",\"漫符\",\"ヒットエフェクト\",\"スキル情報\",\"スチル2\",\"拘束演出\",\"スチル9\",\"立ち絵_サキュバス\",\"スチル8\",\"スチル4-1\",\"スチル4-2\",\"スチル15\",\"立ち絵_セラ\",\"UI ホーム画面\",\"スチル10\",\"スチル5\",\"スチル14\",\"スチル7\",\"スチル7_カットイン\",\"スチル11\",\"スチル12\",\"クリック誘導_スチル7\",\"立ち絵_セラ正面\",\"スチル16\",\"スチル6\",\"スチル1\",\"ピンクもや\",\"スチル3\",\"スチル13\",\"まばたき\",\"治療25_キス\",\"UI 編成\",\"UI 回想\",\"UI ショップ\",\"UI アフターケアリスト\",\"アフターケア0\",\"スチル17\",\"UI アフターケア\",\"アフターケア1\",\"サブタイトル\",\"アフターケア4\",\"アフターケア8\",\"アフターケア2\",\"アフターケア3\",\"アフターケア5\",\"アフターケア6\",\"アフターケア7\"]",
      "disable auto loading": "false"
    }
  },
  {
    "name": "PicturePointColor",
    "status": true,
    "description": "Tạo các nút ảo",
    "parameters": {}
  },
  {
    "name": "DTextPicture",
    "status": true,
    "description": "Plugin hỗ trợ thiết bị di động",
    "parameters": {
      "frameWindowSkin": "",
      "frameWindowPadding": "18",
      "padCharacter": "0",
      "prefixText": "",
      "widthVariable": "0",
      "heightVariable": "0"
    }
  },
  {
    "name": "ExtraGauge",
    "status": true,
    "description": "Plugin thông số hình ảnh tùy chỉnh",
    "parameters": {
      "GaugeList": "[\"{\\\"SceneName\\\":\\\"Scene_Map\\\",\\\"Id\\\":\\\"照れゲージ\\\",\\\"SwitchId\\\":\\\"42\\\",\\\"OpacityVariable\\\":\\\"0\\\",\\\"Layout\\\":\\\"{\\\\\\\"x\\\\\\\":\\\\\\\"654\\\\\\\",\\\\\\\"y\\\\\\\":\\\\\\\"44\\\\\\\",\\\\\\\"originX\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"originY\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"linkCharacter\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"realTime\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"width\\\\\\\":\\\\\\\"170\\\\\\\",\\\\\\\"height\\\\\\\":\\\\\\\"40\\\\\\\",\\\\\\\"GaugeX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeEndX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeHeight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Vertical\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"Mirror\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ParentWindow\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"CurrentMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"42\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"MaxMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"80\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"100\\\\\\\"}\\\",\\\"Detail\\\":\\\"{\\\\\\\"RisingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"FallingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"GaugeImage\\\\\\\":\\\\\\\"システム/照れゲージ1\\\\\\\",\\\\\\\"GaugeBackHidden\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"ScaleAutoAdjust\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"GaugeColorPreset\\\\\\\":\\\\\\\"hp\\\\\\\",\\\\\\\"GaugeColorLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"BackColor\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Label\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"LabelY\\\\\\\":\\\\\\\"3\\\\\\\",\\\\\\\"IconIndex\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"LabelFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"DrawValue\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ValueFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"ValueFormat\\\\\\\":\\\\\\\"%1/%2\\\\\\\",\\\\\\\"ValuePadZeroDigit\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"ValueAlign\\\\\\\":\\\\\\\"right\\\\\\\",\\\\\\\"FlashIfFull\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"FullSwitchId\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"LowerPicture\\\":\\\"{\\\\\\\"FileName\\\\\\\":\\\\\\\"システム/照れゲージ2\\\\\\\",\\\\\\\"OffsetX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"OffsetY\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"UpperPicture\\\":\\\"\\\",\\\"Battler\\\":\\\"\\\"}\",\"{\\\"SceneName\\\":\\\"Scene_Map\\\",\\\"Id\\\":\\\"射精ゲージ\\\",\\\"SwitchId\\\":\\\"43\\\",\\\"OpacityVariable\\\":\\\"0\\\",\\\"Layout\\\":\\\"{\\\\\\\"x\\\\\\\":\\\\\\\"654\\\\\\\",\\\\\\\"y\\\\\\\":\\\\\\\"696\\\\\\\",\\\\\\\"originX\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"originY\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"linkCharacter\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"realTime\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"width\\\\\\\":\\\\\\\"170\\\\\\\",\\\\\\\"height\\\\\\\":\\\\\\\"40\\\\\\\",\\\\\\\"GaugeX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeEndX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeHeight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Vertical\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"Mirror\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ParentWindow\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"CurrentMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"43\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"MaxMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"72\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"Detail\\\":\\\"{\\\\\\\"RisingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"FallingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"GaugeImage\\\\\\\":\\\\\\\"システム/射精ゲージ1\\\\\\\",\\\\\\\"GaugeBackHidden\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"ScaleAutoAdjust\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"GaugeColorPreset\\\\\\\":\\\\\\\"hp\\\\\\\",\\\\\\\"GaugeColorLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"BackColor\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Label\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"LabelY\\\\\\\":\\\\\\\"3\\\\\\\",\\\\\\\"IconIndex\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"LabelFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"DrawValue\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ValueFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"ValueFormat\\\\\\\":\\\\\\\"%1/%2\\\\\\\",\\\\\\\"ValuePadZeroDigit\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"ValueAlign\\\\\\\":\\\\\\\"right\\\\\\\",\\\\\\\"FlashIfFull\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"FullSwitchId\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"LowerPicture\\\":\\\"{\\\\\\\"FileName\\\\\\\":\\\\\\\"システム/射精ゲージ2\\\\\\\",\\\\\\\"OffsetX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"OffsetY\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"UpperPicture\\\":\\\"\\\",\\\"Battler\\\":\\\"\\\"}\",\"{\\\"SceneName\\\":\\\"Scene_Map\\\",\\\"Id\\\":\\\"照れゲージ\\\",\\\"SwitchId\\\":\\\"52\\\",\\\"OpacityVariable\\\":\\\"0\\\",\\\"Layout\\\":\\\"{\\\\\\\"x\\\\\\\":\\\\\\\"154\\\\\\\",\\\\\\\"y\\\\\\\":\\\\\\\"44\\\\\\\",\\\\\\\"originX\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"originY\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"linkCharacter\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"realTime\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"width\\\\\\\":\\\\\\\"170\\\\\\\",\\\\\\\"height\\\\\\\":\\\\\\\"40\\\\\\\",\\\\\\\"GaugeX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeEndX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeHeight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Vertical\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"Mirror\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ParentWindow\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"CurrentMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"42\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"MaxMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"80\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"100\\\\\\\"}\\\",\\\"Detail\\\":\\\"{\\\\\\\"RisingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"FallingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"GaugeImage\\\\\\\":\\\\\\\"システム/照れゲージ1\\\\\\\",\\\\\\\"GaugeBackHidden\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"ScaleAutoAdjust\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"GaugeColorPreset\\\\\\\":\\\\\\\"hp\\\\\\\",\\\\\\\"GaugeColorLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"BackColor\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Label\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"LabelY\\\\\\\":\\\\\\\"3\\\\\\\",\\\\\\\"IconIndex\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"LabelFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"DrawValue\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ValueFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"ValueFormat\\\\\\\":\\\\\\\"%1/%2\\\\\\\",\\\\\\\"ValuePadZeroDigit\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"ValueAlign\\\\\\\":\\\\\\\"right\\\\\\\",\\\\\\\"FlashIfFull\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"FullSwitchId\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"LowerPicture\\\":\\\"{\\\\\\\"FileName\\\\\\\":\\\\\\\"システム/照れゲージ2\\\\\\\",\\\\\\\"OffsetX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"OffsetY\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"UpperPicture\\\":\\\"\\\",\\\"Battler\\\":\\\"\\\"}\",\"{\\\"SceneName\\\":\\\"Scene_Map\\\",\\\"Id\\\":\\\"射精ゲージ\\\",\\\"SwitchId\\\":\\\"53\\\",\\\"OpacityVariable\\\":\\\"0\\\",\\\"Layout\\\":\\\"{\\\\\\\"x\\\\\\\":\\\\\\\"484\\\\\\\",\\\\\\\"y\\\\\\\":\\\\\\\"696\\\\\\\",\\\\\\\"originX\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"originY\\\\\\\":\\\\\\\"center\\\\\\\",\\\\\\\"linkCharacter\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"realTime\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"width\\\\\\\":\\\\\\\"170\\\\\\\",\\\\\\\"height\\\\\\\":\\\\\\\"40\\\\\\\",\\\\\\\"GaugeX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeEndX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeHeight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Vertical\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"Mirror\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ParentWindow\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"CurrentMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"43\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"MaxMethod\\\":\\\"{\\\\\\\"VariableId\\\\\\\":\\\\\\\"72\\\\\\\",\\\\\\\"Script\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"FixedValue\\\\\\\":\\\\\\\"\\\\\\\"}\\\",\\\"Detail\\\":\\\"{\\\\\\\"RisingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"FallingSmoothness\\\\\\\":\\\\\\\"30\\\\\\\",\\\\\\\"GaugeImage\\\\\\\":\\\\\\\"システム/射精ゲージ1\\\\\\\",\\\\\\\"GaugeBackHidden\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"ScaleAutoAdjust\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"GaugeColorPreset\\\\\\\":\\\\\\\"hp\\\\\\\",\\\\\\\"GaugeColorLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullLeft\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"GaugeColorFullRight\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"BackColor\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"Label\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"LabelY\\\\\\\":\\\\\\\"3\\\\\\\",\\\\\\\"IconIndex\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"LabelFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"DrawValue\\\\\\\":\\\\\\\"false\\\\\\\",\\\\\\\"ValueFont\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"ValueFormat\\\\\\\":\\\\\\\"%1/%2\\\\\\\",\\\\\\\"ValuePadZeroDigit\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"ValueAlign\\\\\\\":\\\\\\\"right\\\\\\\",\\\\\\\"FlashIfFull\\\\\\\":\\\\\\\"true\\\\\\\",\\\\\\\"FullSwitchId\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"LowerPicture\\\":\\\"{\\\\\\\"FileName\\\\\\\":\\\\\\\"システム/射精ゲージ2\\\\\\\",\\\\\\\"OffsetX\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"OffsetY\\\\\\\":\\\\\\\"0\\\\\\\"}\\\",\\\"UpperPicture\\\":\\\"\\\",\\\"Battler\\\":\\\"\\\"}\"]",
      "Priority": "2"
    }
  },
  {
    "name": "VariableLimitation",
    "status": true,
    "description": "Cài đặt giới hạn giá trị biến số",
    "parameters": {
      "list": "[\"{\\\"variableId\\\":\\\"44\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"99\\\"}\",\"{\\\"variableId\\\":\\\"49\\\",\\\"min\\\":\\\"-5\\\",\\\"max\\\":\\\"0\\\"}\",\"{\\\"variableId\\\":\\\"50\\\",\\\"min\\\":\\\"-5\\\",\\\"max\\\":\\\"0\\\"}\",\"{\\\"variableId\\\":\\\"51\\\",\\\"min\\\":\\\"-5\\\",\\\"max\\\":\\\"0\\\"}\",\"{\\\"variableId\\\":\\\"52\\\",\\\"min\\\":\\\"-5\\\",\\\"max\\\":\\\"0\\\"}\",\"{\\\"variableId\\\":\\\"56\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"99\\\"}\",\"{\\\"variableId\\\":\\\"57\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"99\\\"}\",\"{\\\"variableId\\\":\\\"58\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"99\\\"}\",\"{\\\"variableId\\\":\\\"42\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"999\\\"}\",\"{\\\"variableId\\\":\\\"43\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"999\\\"}\",\"{\\\"variableId\\\":\\\"75\\\",\\\"min\\\":\\\"1\\\",\\\"max\\\":\\\"46\\\"}\",\"{\\\"variableId\\\":\\\"10\\\",\\\"min\\\":\\\"0\\\",\\\"max\\\":\\\"9999999\\\"}\",\"{\\\"variableId\\\":\\\"72\\\",\\\"min\\\":\\\"100\\\",\\\"max\\\":\\\"999\\\"}\"]"
    }
  },
  {
    "name": "LL_OutlineColorAuto",
    "status": true,
    "description": "Tự động điều chỉnh màu viền chữ",
    "parameters": {
      "brightEvaluation": "60",
      "outlineColorBlack": "rgba(0, 0, 0, 0)",
      "outlineColorWhite": "rgba(255, 255, 255, 0)",
      "outlineWidth": "0"
    }
  },
  {
    "name": "EventCommandByCode",
    "status": true,
    "description": "Thực thi lệnh sự kiện theo mã tham số",
    "parameters": {}
  },
  {
    "name": "SU_FadeSpine",
    "status": true,
    "description": "Áp dụng hiệu ứng Fade cho màu sắc mô hình Spine",
    "parameters": {
      "FrameCount": "24"
    }
  },
  {
    "name": "LogMessage",
    "status": true,
    "description": "Plugin hiển thị tin nhắn Log (Hỗ trợ viền chữ)",
    "parameters": {
      "lineHeight": "23",
      "fontSize": "15",
      "iconSize": "15",
      "scrollSpeed": "4",
      "indent": "0",
      "outlineWidth": "4",
      "outlineColor": "rgba(46,68,109,0.6)"
    }
  },
  {
    "name": "FloatVariables",
    "status": true,
    "description": "Plugin tính toán số thập phân cho biến số",
    "parameters": {
      "FloatVariableStart": "61",
      "FloatVariableEnd": "62"
    }
  },
  {
    "name": "MNKR_HzRandomListMZ",
    "status": true,
    "description": "Tạo danh sách giá trị ngẫu nhiên không trùng lặp",
    "parameters": {}
  },
  {
    "name": "SimpleVoice",
    "status": true,
    "description": "Plugin lồng tiếng đơn giản",
    "parameters": {
      "optionName": "Âm lượng giọng nói",
      "optionValue": "100"
    }
  },
  {
    "name": "SaveWindow",
    "status": true,
    "description": "MessageWindowCustomize",
    "parameters": {
      "backSpriteOffSwiche": "0",
      "iconYOffset": "0",
      "bgX": "-4",
      "bgY": "0",
      "iconBaseX": "700",
      "iconBaseY": "215",
      "nameWindowX": "55",
      "nameWindowY": "490",
      "textStartXDefault": "236",
      "textStartYDefault": "92"
    }
  },
  {
    "name": "SimpleVoiceMessageAdvanceStop",
    "status": true,
    "description": "Plugin dừng voice SimpleVoice khi chuyển câu/chuyển map v1.5.0",
    "parameters": {}
  },
  {
    "name": "MessageSkip",
    "status": true,
    "description": "Plugin bỏ qua (Skip) tin nhắn",
    "parameters": {
      "Phím Bỏ qua (Skip)": "control",
      "Phím Tự động (Auto)": "shift",
      "Công tắc Bỏ qua": "0",
      "Công tắc Tự động": "0",
      "Biểu tượng Bỏ qua": "0",
      "Biểu tượng Tự động": "0",
      "Tọa độ X biểu tượng": "0",
      "Tọa độ Y biểu tượng": "0",
      "Nhấn giữ để Bỏ qua": "true",
      "Không áp dụng nhấn giữ cho hình ảnh": "false",
      "Số frame chờ Tự động": "50 + textSize * 5",
      "ID công tắc hủy khi hoàn thành": "0",
      "Hình ảnh Bỏ qua": "",
      "Hình ảnh Bỏ quaX": "500",
      "Hình ảnh Bỏ quaY": "0",
      "Hình ảnh Tự động": "",
      "Hình ảnh Tự độngX": "750",
      "Hình ảnh Tự độngY": "0",
      "Hình ảnh Công tắc": "",
      "Hình ảnh Công tắcトリガー": "0",
      "Hình ảnh Công tắcX": "750",
      "Hình ảnh Công tắcY": "0",
      "Gốc tọa độ nút": "0",
      "ID công tắc hiển thị nút": "0",
      "Loại tọa độ hình ảnh": "relative",
      "Công tắc Vô hiệu hóa": "0",
      "skipWait": "false",
      "SkipKey": "control",
      "AutoKey": "shift",
      "Phím Bỏ qua": "control",
      "Phím Tự động": "shift",
      "スキップキー": "control",
      "オートキー": "shift",
      "スキップスイッチ": "0",
      "SkipSwitchId": "0",
      "オートスイッチ": "0",
      "AutoSwitchIId": "0",
      "スキップアイコン": "0",
      "SkipIcon": "0",
      "オートアイコン": "0",
      "AutoIcon": "0",
      "アイコンX": "0",
      "IconX": "0",
      "アイコンY": "0",
      "IconY": "0",
      "押し続けスキップ": "true",
      "PressingSkip": "true",
      "ピクチャは押し続け対象外": "false",
      "PictureOutOfPressing": "false",
      "オート待機フレーム": "50 + textSize * 5",
      "AutoWaitFrame": "50 + textSize * 5",
      "終了解除スイッチID": "0",
      "ResetOnEndSwitch": "0",
      "スキップピクチャ": "",
      "SkipPicture": "",
      "スキップピクチャX": "500",
      "SkipPictureX": "500",
      "スキップピクチャY": "0",
      "SkipPictureY": "0",
      "オートピクチャ": "",
      "AutoPicture": "",
      "オートピクチャX": "750",
      "AutoPictureX": "750",
      "オートピクチャY": "0",
      "AutoPictureY": "0",
      "スイッチピクチャ": "",
      "SwitchPicture": "",
      "スイッチピクチャトリガー": "0",
      "SwitchPictureTrigger": "0",
      "スイッチピクチャX": "750",
      "SwitchPictureX": "750",
      "スイッチピクチャY": "0",
      "SwitchPictureY": "0",
      "ボタン原点": "0",
      "PictureAnchor": "0",
      "ボタン表示スイッチID": "0",
      "PictureSwitchId": "0",
      "ピクチャ座標タイプ": "relative",
      "PicturePosType": "relative",
      "無効化スイッチ": "0",
      "InvalidSwitchId": "0"
    }
  },
  {
    "name": "MessageSkipVoiceEndWait",
    "status": true,
    "description": "Plugin chờ tự động chuyển sau voice cho MessageSkip/SimpleVoice v1.0.0",
    "parameters": {
      "WaitFrame": "30"
    }
  },
  {
    "name": "DarkPlasma_TextLog",
    "status": true,
    "description": "Hiển thị nhật ký tin nhắn (Backlog)",
    "parameters": {
      "disableLoggingSwitch": "0",
      "openLogKeys": "[\"tab\"]",
      "disableLogWindowSwitch": "0",
      "lineSpacing": "0",
      "messageSpacing": "0",
      "logSplitter": "-------------------------------------------------------",
      "autoSplit": "true",
      "choiceFormat": "Lựa chọn: {choice}",
      "choiceColor": "17",
      "choiceCancelText": "Hủy bỏ",
      "smoothBackFromLog": "true",
      "backgroundImage": "",
      "showLogWindowFrame": "true",
      "escapeCharacterCodes": "[]",
      "scrollSpeed": "1",
      "scrollSpeedHigh": "10",
      "maxLogMessages": "200"
    }
  },
  {
    "name": "Text2Frame",
    "status": true,
    "description": "テキストファイル(.txtファイルなど)から「文章の表示」イベントコマンドに簡単に変換するための、Hiển thị hội thoại tự động dạng Baloonです。ツクールMV・MZの両方に対応しています。",
    "parameters": {
      "Default Window Position": "Dưới",
      "Default Background": "Cửa sổ",
      "Default Scenario Folder": "text",
      "Default Scenario File": "message.txt",
      "Default Common Event ID": "1",
      "Default MapID": "1",
      "Default EventID": "2",
      "Default PageID": "1",
      "IsOverwrite": "false",
      "Comment Out Char": "%",
      "IsDebug": "false",
      "DisplayMsg": "true",
      "DisplayWarning": "true"
    }
  },
  {
    "name": "LL_GalgeChoiceWindow",
    "status": true,
    "description": "Plugin cửa sổ lựa chọn phong cách Novel Game",
    "parameters": {}
  },
  {
    "name": "MPP_ChoiceEX",
    "status": true,
    "description": "Mở rộng tính năng cho cửa sổ lựa chọn.",
    "parameters": {
      "Max Page Row": "6",
      "Disabled Position": "none",
      "Choice Help Commands": "[\"ChoiceHelp\",\"<ChoiceHelp>\",\"選択肢ヘルプ\",\"<選択肢ヘルプ>\"]"
    }
  },
  {
    "name": "MessageWindowKeep",
    "status": true,
    "description": "Plugin duy trì cửa sổ tin nhắn",
    "parameters": {
      "keepSwitch": "999"
    }
  },
  {
    "name": "MessageWindowHidden",
    "status": true,
    "description": "Plugin ẩn tạm thời cửa sổ tin nhắn",
    "parameters": {
      "triggerButton": "[\"右クリック\"]",
      "triggerSwitch": "0",
      "syncSwitch": "false",
      "linkPictureNumbers": "[]",
      "linkShowPictureNumbers": "[]",
      "disableLinkSwitchId": "0",
      "disableSwitchId": "0",
      "disableInBattle": "false",
      "disableInChoice": "true",
      "restoreByDecision": "false"
    }
  },
  {
    "name": "CustomizeConfigItem",
    "status": true,
    "description": "Plugin tạo mục cài đặt tùy chỉnh trong Tùy chọn",
    "parameters": {
      "NumberOptions": "[\"{\\\"Name\\\": \\\"Giảm ST Nhận Vào\\\", \\\"DefaultValue\\\": \\\"0\\\", \\\"VariableID\\\": \\\"15\\\", \\\"HiddenFlag\\\": \\\"false\\\", \\\"Script\\\": \\\"\\\", \\\"NumberMin\\\": \\\"0\\\", \\\"NumberMax\\\": \\\"100\\\", \\\"NumberStep\\\": \\\"25\\\", \\\"Unit\\\": \\\"%\\\", \\\"AddPosition\\\": \\\"\\\", \\\"PaddingTop\\\": \\\"0\\\"}\", \"{\\\"Name\\\": \\\"Tăng ST Gây Ra\\\", \\\"DefaultValue\\\": \\\"0\\\", \\\"VariableID\\\": \\\"16\\\", \\\"HiddenFlag\\\": \\\"false\\\", \\\"Script\\\": \\\"\\\", \\\"NumberMin\\\": \\\"0\\\", \\\"NumberMax\\\": \\\"100\\\", \\\"NumberStep\\\": \\\"25\\\", \\\"Unit\\\": \\\"%\\\", \\\"AddPosition\\\": \\\"\\\", \\\"PaddingTop\\\": \\\"0\\\"}\"]",
      "StringOptions": "",
      "SwitchOptions": "[\"{\\\"Name\\\": \\\"x2 EXP Nhận Được\\\", \\\"DefaultValue\\\": \\\"false\\\", \\\"SwitchID\\\": \\\"36\\\", \\\"OnText\\\": \\\"\\\", \\\"OffText\\\": \\\"\\\", \\\"HiddenFlag\\\": \\\"false\\\", \\\"Script\\\": \\\"\\\", \\\"AddPosition\\\": \\\"\\\", \\\"PaddingTop\\\": \\\"0\\\"}\", \"{\\\"Name\\\": \\\"x2 Tiền Nhận Được\\\", \\\"DefaultValue\\\": \\\"false\\\", \\\"SwitchID\\\": \\\"37\\\", \\\"OnText\\\": \\\"\\\", \\\"OffText\\\": \\\"\\\", \\\"HiddenFlag\\\": \\\"false\\\", \\\"Script\\\": \\\"\\\", \\\"AddPosition\\\": \\\"\\\", \\\"PaddingTop\\\": \\\"0\\\"}\"]",
      "VolumeOptions": "",
      "CustomOrder": "[\"NumberOptions\",\"StringOptions\",\"SwitchOptions\",\"VolumeOptions\"]"
    }
  },
  {
    "name": "CustomizeConfigDefault",
    "status": true,
    "description": "Plugin cài đặt giá trị mặc định cho Option",
    "parameters": {
      "AlwaysDash": "false",
      "CommandRemember": "false",
      "TouchUi": "false",
      "BgmVolume": "100",
      "BgsVolume": "100",
      "MeVolume": "100",
      "SeVolume": "100",
      "EraseAlwaysDash": "true",
      "EraseCommandRemember": "true",
      "EraseTouchUi": "true",
      "EraseBgmVolume": "false",
      "EraseBgsVolume": "false",
      "EraseMeVolume": "true",
      "EraseSeVolume": "false"
    }
  },
  {
    "name": "NRP_OptionCustomize",
    "status": true,
    "description": "v1.001 Tùy chỉnh giao diện menu Cài đặt Options",
    "parameters": {
      "SeparateList": "[\"{\\\"SeparateText\\\": \\\"\\\\\\\\I[253]\\\\\\\\c[1]Tùy Chỉnh\\\", \\\"Position\\\": \\\"0\\\"}\", \"{\\\"SeparateText\\\": \\\"\\\\\\\\I[254]\\\\\\\\c[2]Tùy Chọn Gian Lận\\\", \\\"Position\\\": \\\"5\\\"}\"]",
      "SeparateCenter": "true",
      "MaxVisibleCommands": "",
      "WindowWidth": "",
      "WindowBackgroundType": "0",
      "VolumeOffset": "5.00",
      "MagnifiedVolume": ""
    }
  },
  {
    "name": "FontLoad",
    "status": true,
    "description": "Plugin nạp Phông chữ (Font)",
    "parameters": {
      "fontList": "[\"{\\\"name\\\":\\\"noto sans bold\\\",\\\"fileName\\\":\\\"NotoSansJP-Bold.ttf\\\"}\",\"{\\\"name\\\":\\\"noto sans medium\\\",\\\"fileName\\\":\\\"NotoSansJP-Medium.ttf\\\"}\"]"
    }
  },
  {
    "name": "MOG_TitleCommands",
    "status": true,
    "description": "(v1.3) Hiển thị lệnh menu Tiêu đề bằng Hình ảnh",
    "parameters": {
      "-> Main <<<<<<<<<<<<<<<<<<<<<<<": "",
      "Animation Mode": "0",
      "Left & Right Input": "true",
      "Shake Duration": "30",
      "Slide X-Axis": "0",
      "Slide Y-Axis": "0",
      "-> Cursor <<<<<<<<<<<<<<<<<<<<<<<": "",
      "Cursor X-Axis": "0",
      "Cursor Y-Axis": "0",
      "Cursor Visible": "false",
      "Cursor Wave Animation": "false",
      "Cursor Rotation Animation": "false",
      "Cursor Rotation Speed": "0.05",
      "-> Commands <<<<<<<<<<<<<<<<<<<<<<<": "",
      "Command Pos 1": "741,406",
      "Command Pos 2": "732,498",
      "Command Pos 3": "722,606",
      "Command Pos 4": "690,440",
      "Command Pos 5": "345,498",
      "Command Pos 6": "345,530",
      "Command Pos 7": "0,192",
      "Command Pos 8": "0,224",
      "Command Pos 9": "0,256",
      "Command Pos 10": "0,288"
    }
  },
  {
    "name": "MOG_TitleCommands_AlphaHit.js",
    "status": true,
    "description": "Loại bỏ vùng trong suốt khỏi khu vực nhấp chuột menu Tiêu đề MOG_TitleCommands",
    "parameters": {
      "AlphaThreshold": "0"
    }
  },
  {
    "name": "LatinNameInput",
    "status": true,
    "description": "Bàn phím nhập tên Latinh",
    "parameters": {}
  },
  {
    "name": "AutoWordWrap",
    "status": true,
    "description": "Tự động xuống dòng hội thoại tiếng Việt",
    "parameters": {}
  }
];
