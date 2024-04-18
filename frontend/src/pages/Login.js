import React, { useState } from "react";


const Login = () => {

    const [username, setUsername] = useState("");
    
    const setUsernameCookie = () => {
        var days = 1
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + days);
        document.cookie = `${"username"}=${username}; expires=${expirationDate.toUTCString()}; path=/`;
    };

    return (
        <>
            <h1>Login</h1>
            <input type="text" value={username} onChange={e => setUsername(e.target.value)}></input>
            <button onClick={() => setUsernameCookie()}>Submit</button>
        </>
    );
};
  
export default Login;