import React, { useContext } from "react";
import UserListItemAdmin from "./listItemVersions/UserListItemAdmin";
import { useTranslation } from "react-i18next";
import { AuthContext } from "../../../AuthProvider";
import { Roles } from "../../../constants/Roles";


const UserListItem = ({ user }) => {

    const { t } = useTranslation();

    const { userRoles } = useContext(AuthContext);

    return (
        <>
            {userRoles.includes(Roles.ADMINISTRATOR) ?
                <UserListItemAdmin user={user} key={user.name} /> : null}
        </>
    )
}

export default UserListItem;