function stringToHex(str) {
    var val = "";
    for (var i = 0; i < str.length; i++) {
        if (val == "") val = str.charCodeAt(i).toString(16); else val += str.charCodeAt(i).toString(16);
    }
    return val;
}

function YunSuoAutoJump() {
    var width = 1536;
    var height = 864;
    var screendate = width + "," + height;
    var curlocation = window.location.href;
    if (-1 == curlocation.indexOf("security_verify_")) {
        document.cookie = "srcurl=" + stringToHex(window.location.href) + ";path=/;";
    }
    self.location = "/a/zcwj/?security_verify_data=" + stringToHex(screendate);
}

var cookie_custom = {
    hasItem: function (sKey) {
        return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
    }, removeItem: function (sKey, sPath) {
        if (!sKey || !this.hasItem(sKey)) {
            return false;
        }
        document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sPath ? "; path=" + sPath : "");
        return true;
    }
};

function YunSuoAutoJump() {
    self.location = "http://www.satcm.gov.cn/a/zcwj/";
}