/**
 * Gets cookie by name
 * @param name
 * @returns {string}
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
    return null;
}


/**
 * Creates new cookie
 * @param name
 * @param value
 * @param cookieExpireDays set zero or less than zero value for endless cookie
 */
function setCookie(name, value, cookieExpireDays = 0) {
    let cookie = name + "=" + encodeURIComponent(value) + "; Path=/; SameSite=Strict";

    if (location.protocol === "https:")
        cookie += "; Secure";

    if (cookieExpireDays > 0) {
        const date = new Date();
        date.setDate(date.getDate() + cookieExpireDays);
        cookie += "; expires=" + date.toUTCString();
    }

    document.cookie = cookie;
}


/**
 * Removes cookie by its name
 * @param name
 */
function removeCookie(name) {
    document.cookie = name + "=; Path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Strict" + (location.protocol === "https:" ? "; Secure" : "");
}



function setAuthToken(value, cookieExpireDays) {
    setCookie("auth-token", value, cookieExpireDays);
}

function removeAuthToken() {
    removeCookie("auth-token");
}

function getAuthToken() {
    return getCookie("auth-token");
}