const sessionDurationHours = 3; // 3 hours

// Function to get the value of a specified cookie by its name
export const getCookie = (name) => {
    // Split the document.cookie string into individual cookies and find the one that starts with the specified name
    const cookies = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));

    // If the cookie is found, split it by '=' and return the value part, otherwise return null
    return cookies ? cookies.split('=')[1] : null;
};

// Function to delete a specified cookie by its name
export const deleteCookie = (name) => {
    // Set the cookie with the specified name to expire in the past, effectively deleting it
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
};

// Set a cookie with a specified label and value
export const setCookie = (label, value) => {
    const expirationTime = new Date();
    expirationTime.setHours(expirationTime.getHours() + sessionDurationHours);
    document.cookie = `${label}=${value}; expires=${expirationTime.toUTCString()}; path=/`;
};