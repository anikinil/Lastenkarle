import React from "react";

// Function to get a cookie value by name
const getCookie = (name) => {
    const cookies = document.cookie
      .split("; ")
      .find((row) => row.startsWith(`${name}=`));
   
    return cookies ? cookies.split("=")[1] : null;
   };
   
// Example: Get the value of the 'username' cookie
const username = getCookie("username");


const Home = () => {
    return (
        <>
            <h1>Homepage</h1>
            <p>You are {username ? username : "unknown" }.</p>
        </>
    );
};

export default Home;