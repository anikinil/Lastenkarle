import React from "react";
import { useEffect, useState } from "react";
import { Roles } from "../../../constants/Roles";
import { ERR_FETCHING_USER_FLAGS } from "../../../constants/ErrorMessages";
import { USER_DATA } from "../../../constants/URIs/UserURIs";
import StoreConfigAdmin from "../components/StoreConfigAdmin";
import StoreConfigManager from "../components/StoreConfigManager";
import { getCookie } from "../../../services/Cookies";

const StoreConfigPage = () => {

    const [isAdmin, setIsAdmin] = useState('rendering');

    const fetchUserRoles = () => {
        const token = getCookie('token');
        if (token !== 'undefined' && token !== null) {
            fetch(USER_DATA, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    const userRoles = data.user_flags.map(element => element.flag)
                    setIsAdmin(userRoles.includes(Roles.ADMINISTRATOR))
                })
                .catch(error => {
                    console.error(ERR_FETCHING_USER_FLAGS, error);
                });
        } else {
            setIsAdmin(false)
        }
    }

    useEffect(() => {
        fetchUserRoles();
    }, [])

    return (
        <>
            {/* {isAdmin == 'rendering' ?
                <div>Loading...</div>
                :
                <> */}
                    {isAdmin ?
                        <StoreConfigAdmin />
                        :
                        <StoreConfigManager />
                    }
                {/* </>

            } */}
        </>
    );
}

export default StoreConfigPage;