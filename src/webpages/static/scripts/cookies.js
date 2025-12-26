/**
 * Gets cookie by name
 * @param name
 * @returns {string}
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

/**
 * Creates new cookie
 * @param name
 * @param value
 * @param cookieExpireDays set zero or less than zero value for endless cookie
 */
function setCookie(name, value, cookieExpireDays) {
    let cookieExpireDate = new Date();
    cookieExpireDate.setDate(cookieExpireDate.getDate() + cookieExpireDays);
    let cookie =
        name + "=" + value + ";" +
        "SameSite=Strict;" +
        "Path=/";

    if (cookieExpireDays > 0) {
        cookie += "expires=" + cookieExpireDate.toUTCString() + ";"
    }
    document.cookie = cookie;
    console.log(document.cookie);
}

/**
 * Removes cookie by its name
 * @param name
 */
function removeCookie(name) {
    let date = new Date();
    date.setDate(date.getDate() - 1);
    document.cookie =
        name + ";" +
        "expires=" + date;
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