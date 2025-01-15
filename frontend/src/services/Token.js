import { getCookie } from "./Cookies";

// TODO use everywhere where getCookie('token') is used
export const getToken = () => {
    return getCookie('token');
};

export const tokenExpired = () => {
    const token = getCookie('token');
    return (token == undefined)
};