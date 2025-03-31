import React from 'react';

import { useContext } from "react";
import { Roles } from "../../../constants/Roles";
import { AuthContext } from '../../../AuthProvider';
import BookingPageAdmin from '../components/BookingPageAdmin';
import BookingPageManager from '../components/BookingPageManager';
import PageNotFound from "../../../pages/PageNotFound";

const BookingPage = () => {
        
    const { userRoles } = useContext(AuthContext);

    console.log("userRoles", userRoles);    

    return (
        <>
            {userRoles.includes(Roles.MANAGER) || userRoles.includes(Roles.VERIFIED) ?
                <BookingPageManager />
                :
                <>
                    {userRoles.includes(Roles.ADMIN) ?
                        <BookingPageAdmin />
                        :
                        <PageNotFound />
                    }
                </>
            }
        </>
    );
}

export default BookingPage;