function capitalize(str) {
    if (!str) return '';
    return str[0].toUpperCase() + str.slice(1);
}

function setUserData(user_name, role_name) {
    $('#user-name').html(user_name);
    $('#role-name').html(user_name);
}

async function getMe() {
    const token = getAuthToken();
    if (token) {
        try {
            const response = await $.ajax({
                type: 'GET',
                url: '/api/users/me',
                contentType: 'application/json',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            setUserData(response.user_name, capitalize(response.role.role_name));
        }
        catch (xhr) {
            show_errors(xhr.responseJSON.detail);
            setUserData('Вы не авторизованы!', 'Вы не авторизованы!');
        }
    }
    else {
        setUserData('Вы не авторизованы!', 'Вы не авторизованы!');
    }

}

$(function () {
    getMe();
});