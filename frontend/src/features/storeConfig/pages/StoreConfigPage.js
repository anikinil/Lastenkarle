import React from "react";
import { useEffect, useState, useContext } from "react";
import { Roles } from "../../../constants/Roles";
import StoreConfigAdmin from "../components/StoreConfigAdmin";
import StoreConfigManager from "../components/StoreConfigManager";
import { AuthContext } from '../../../AuthProvider';


const StoreConfigPage = () => {

    const [isAdmin, setIsAdmin] = useState('rendering');

    const { userRoles } = useContext(AuthContext);

    useEffect(() => {
        if (userRoles.includes(Roles.ADMINISTRATOR)) {
            setIsAdmin(true)
        } else {
            setIsAdmin(false)
        }
    }, [])

    return (
        <>
            {isAdmin ?
                <StoreConfigAdmin />
                :
                <StoreConfigManager />
            }
        </>
    );
}

export default StoreConfigPage;