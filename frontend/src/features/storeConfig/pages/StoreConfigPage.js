import React from "react";
import { useEffect, useState, useContext } from "react";
import { Roles } from "../../../constants/Roles";
import StoreConfigAdmin from "../components/StoreConfigAdmin";
import StoreConfigManager from "../components/StoreConfigManager";
import { AuthContext } from '../../../AuthProvider';
import PageNotFound from "../../../pages/PageNotFound";


const StoreConfigPage = () => {

    const { userRoles } = useContext(AuthContext);

    return (
        <>
            {userRoles.includes(Roles.ADMINISTRATOR) ?
                <StoreConfigAdmin />
                :
                <>
                    {userRoles.includes(Roles.MANAGER) ?
                        <StoreConfigManager />
                        :
                        <PageNotFound />
                    }
                </>
            }
        </>
    );
}

export default StoreConfigPage;