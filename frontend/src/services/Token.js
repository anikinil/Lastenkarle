import { getCookie } from "./Cookies";

export const getToken = () => {
    return getCookie('token');
};

export const tokenExpired = () => {
    const token = getCookie('token');
    return (token == undefined)
};